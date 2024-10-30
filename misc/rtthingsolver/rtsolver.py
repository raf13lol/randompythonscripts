import mido, rtconsts, json, os

# this is where most of the actual sample key is from
samplejson = json.loads(rtconsts.samplejson)
samples = samplejson["samples"]

# uhh i mean trailing in front
def trailingZeros(string, length):
    while len(string) < length:
        string = "0" + string
    return string

# use fancy string manip to get this
def getBank(bankIndex):
    string = rtconsts.fullbanklist
    # find the inst bank
    index = string.index(f"inst_bank_{trailingZeros(str(bankIndex), 2)}")
    # do this and that
    return string[index + 20:string.index("};", index)]

# fancy string manip 2: the sequelence
def getBankLength(bankIndex):
    string = rtconsts.fullbanklist
    # find the inst bank
    index = string.index("//", string.index(f"inst_bank_{trailingZeros(str(bankIndex), 2)}") - 36)
    # do this and that
    return int(string[index + 3:string.index("In", index) - 1])

# call me crazy but, Fancy string manip 3: the threequnce
def getInstFromBank(instIndexInBank, bankString):
    # fuck it lol this works
    instIndexInBank -= 1
    string = bankString
    index = 0 

    # uhh yea
    try:
        while instIndexInBank >= 0:
            index = string.index(",", index) + 1
            instIndexInBank -= 1
    except ValueError:
        raise LookupError("inst index doesn't exist in bank maybe?")
    strtoclean = string[index:string.index("}", index + 1)]
    # references to samples via the &Smaple
    if "NULL" in strtoclean:
        strtoclean = "NULL" 
    else:
        ampstersand = strtoclean.index("&")
        strtoclean = strtoclean[ampstersand + 1:strtoclean.index(" ", ampstersand)]

    return strtoclean

# fancy string manip 4: the fourequence
# this gets what the struct has of the instrument shit
def instinfohelper(baseinfo, substr, startoff = 0, endoff = 0, searchthing = ","):
    xindex = baseinfo.index(substr)
    return baseinfo[xindex + len(substr) + startoff:baseinfo.index(searchthing, xindex) + endoff]

# this isn't fancy enough
# gets the sample key from json from the name
def getsamplething(sample):
    samplenum = int(sample.split("_")[1]) - 1
    return samples[samplenum]["pitch"]

# Fancy string manip 5: the fivequence
def getInstInfo(instName):
    # null
    if instName == "NULL":
        return {
            "type": rtconsts.INST_NUL,
            "typeName": "nul",
        }
    
    string = rtconsts.fullinstrumentlist
    index = string.index(instName)
    # get the base info
    # the ";" is added for the items in the struct at the end
    baseinfo = string[string.index("{", index) + 2:string.index("};", index) - 1] + ";"

    # singleinst is PCM / PSG
    singleinst = True
    typ = rtconsts.INST_PCM
    typmatch = instName.split("_")[1].lower()
    match typmatch:
        case "pcm":
            typ = rtconsts.INST_PCM
        case "psg":
            typ = rtconsts.INST_PSG
        case "spl":
            typ = rtconsts.INST_SPL
            singleinst = False
        case "rhy":
            typ = rtconsts.INST_RHY
            singleinst = False


    retinfo = {
        "type": typ,
        "typeName": typmatch
    }

    if singleinst:
        # panning
        retinfo["panning"] = instinfohelper(baseinfo, "/* Panning   */ ")

        # sample
        if typmatch == "pcm":
            retinfo["sample"] = instinfohelper(baseinfo, "/* Sample    */ ", 1, -5)
            retinfo["sampleKey"] = getsamplething(retinfo["sample"])

            # not sure if this is important
            if "PCM_FIXED" in baseinfo:
                retinfo["unpitched"] = "true" # uhhh? 
            else:
                retinfo["unpitched"] = "false"
        else:
            # wave
            retinfo["wave"] = instinfohelper(baseinfo, "/* PSG Wave  */ ")
            # doesn't use preset wave
            if retinfo["wave"] == "NULL":
                # which channel it's on
                retinfo["wave"] = instinfohelper(baseinfo, "/* PSG Chnl  */ ")
                # the info needed
                if retinfo["wave"] == "PSG_NOISE_CHANNEL":
                    retinfo["waveSomething"] = instinfohelper(baseinfo, "/* PSG Noise */ ")
                else:
                    retinfo["waveSomething"] = instinfohelper(baseinfo, "/* PSG Tone  */ ")

        # struct root key or something idk
        retinfo["structKey"] = int(instinfohelper(baseinfo, "/* Key       */ "), 16)
    else:
        # base key of the bank
        retinfo["baseKey"] = int(instinfohelper(baseinfo, "/* Base Key  */ ")) 
        # actual bank lol
        retinfo["bank"] = int(instinfohelper(baseinfo, "/* Sub-Bank  */ ", 0,0, ";").split("_")[2])
        
        # split table find
        if typmatch == "spl":
            retinfo["splitTable"] = instinfohelper(baseinfo, "/* Key Split */ ")

    return retinfo

# put in instIndex and bankIndex -> instInfo
def getIInstInfoBank(instIndex, bankIndex):
    bank = getBank(bankIndex)
    inst = getInstFromBank(instIndex, bank)
    return getInstInfo(inst)

# put in instIndex and bankString -> instInfo
def getIInstInfo(instIndex, bankString):
    inst = getInstFromBank(instIndex, bankString)
    return getInstInfo(inst)

filename = input("file name? (put '!a' for all files) ")

# get the bank from the song headers
def getSongBank(filename):
    filename = filename + "_mid"
    basestr = rtconsts.songheaders
    try:
        index = basestr.index(filename + ",")
        index = basestr.index("/* Bank Number   */ INST_BANK_", index)
    except:
        return -1
    return int(basestr[index + 30:basestr.index(",", index + 30)])

# merge arrays; for the rhythm bank samples needed detection
def mergeArrays(arrayOne, arrayTwo):
    endArray = []
    for thing in arrayOne:
        endArray.append(thing)
    # we need no dupacates soo
    for thing2 in arrayTwo:
        if not thing2 in endArray:
            endArray.append(thing2)
    endArray.sort()
    return endArray

# handles some shit 
# (end of track, abs->rel) (forSaving)
# (rel->abs) (!forSaving)
def prepMidi(midifile, forSaving = False):
    # rel + eot
    if forSaving:
        tracks = midifile.tracks
        newtracks = []
        for i in range(len(tracks)):
            newtracks.append(mido.MidiTrack(
                mido.midifiles.tracks.fix_end_of_track(tracks[i])
            ))
        midifile.tracks = newtracks
        return midifile
    return midifile

#! why did i make everything strings? whatever
# isSubRhythm is accurate btw 
# `key = (isPSG) ? instPSG->key : instPCM->key;`
# ^ used in rhythm tengoku (the decomp says so)
# makes it so the key played is the key of the instrument
# tldr; makes it so the key is the exact same, no pitching; unpitched
def fancyPrint(data, isSubRhythm = False):
    ret = "uhhhh what the fuck is this instrument"
    match data["typeName"]:
        case "rhy":
            ret = f"rhy inst; subbank {data["bank"]}; basekey {data["baseKey"]}"
        case "spl":
            ret = f"spl inst; subbank {data["bank"]}; basekey {data["baseKey"]}; splittable {data["splitTable"]}"
        case "psg":
            psginfo = f"{data["wave"]}"
            if data["wave"][0] == "P":
                psginfo += f"-{data["waveSomething"]}"

            structroot = f"struct root of {data["structKey"]}; no pan"
            if isSubRhythm:
                structroot = f"unpitched inst? pan of {data["panning"]}"

            ret = f"psg inst; {psginfo}; {structroot}"
        # null
        case "nul":
            ret = "NULL instrument... what the fuck?"
        # pcm
        case "pcm":
            pitchedtext = f"root of json {data["sampleKey"]}, struct {data["structKey"]}"

            # why did i do this? why? why? why?
            if data["unpitched"] == "true" or isSubRhythm:
                pitchedtext = "unpitched inst"
            
            # from the game decomp again:
            # if (!isSubRhythm) {
            #   key = noteKey + midiBus->key;
            #   panning = 0;
            # }
            # you see the `panning = 0;` ?
            # the comment above the code says `// Use the built-in key & panning parameters.`
            # sooo
            panstr = "no pan"
            if isSubRhythm:
                # this is accurate
                pannum = data["panning"]
                if pannum == "127":
                    pannum = "0"
                panstr = f"pan of {pannum} ({data["panning"]})"

            ret = f"pcm inst; {data["sample"]}, {pitchedtext}; {panstr}"
    return ret

# big belangrijk
def removeEmpty(array):
    newArray = []
    for i in range(len(array)):
        if len(array[i]) > 0:
            newArray.append(array[i])
    return newArray

def run(filename, internal):
    # finally time to look at the midi
    midifile = mido.MidiFile(filename + ".mid")

    # hey buddy
    midifile = prepMidi(midifile)

    bankindex = getSongBank(internal)
    if bankindex == -1:
        internal = input(f"internal name of {internal}? ")
        bankindex = getSongBank(internal)
        if bankindex == -1:
            print("wow")
            print("")
            return
    bankstr = getBank(bankindex)
    # temp
    stupidnotes2 = []

    splitstuff = []
    donesplit = []

    ogtracklen = len(midifile.tracks)

    print(f"for file {internal}.mid;")
    print("using bank " + str(bankindex) + ";")

    # this isn't gamemaker
    for i in range(129):
        stupidnotes2.append([])

    blankarray = []

    # this still isn't gamemaker
    for i in range(129):
        blankarray.append([])

    outputstrings = []

    #! This is really bad
    #! it creates so many arrays of shit but it's the best solution
    length = len(midifile.tracks)
    for i in range(length):
        # usually just like bpm and time sign, we need to skip it
        if i == 0:
            continue
        trackthing = midifile.tracks[i]

        notedownnotes = False
        notes = blankarray.copy()

        # zo achterlijk
        programtracks = [] 
        programtracksdone = blankarray.copy()
        programnum = -1

        baseprogramnum = -1
        basenum = blankarray.copy()
        prevtimes = []
        deltatime = 0

        instinfos = []

        for asd in range(129):
            programtracks.append(mido.MidiTrack())
            prevtimes.append(0)
            instinfos.append("")

        for j in range(len(trackthing)):
            deltatime += trackthing[j].time
            if trackthing[j].type == "program_change":
                info = getIInstInfo(trackthing[j].program, bankstr)
                endinfo = info
                programnum = trackthing[j].program
                # base should be this
                if baseprogramnum == -1:
                    baseprogramnum = programnum
                    outputstrings.append(f"{i}-{programnum}: {fancyPrint(endinfo)}")

                if programnum != baseprogramnum and not programnum in programtracksdone:
                    programtracksdone.append(programnum)

                instinfos[programnum] = endinfo

                if info["typeName"] == "rhy":
                    notedownnotes = True
                    basenum[programnum] = info["baseKey"]
                else:
                    notedownnotes = False

                # prep for spl later down the line
                if info["typeName"] == "spl" and not programnum in donesplit:
                    splitstuff.append([programnum, info["bank"], info["splitTable"], info["baseKey"]])
                    donesplit.append(programnum)
            # we'll change this at some point
            if trackthing[j].type == "note_on":
                # handle note down notes
                if notedownnotes and not (trackthing[j].note - basenum[programnum]) in notes[programnum]:
                    notes[programnum].append(trackthing[j].note - basenum[programnum])
            # heh... funny... 
            if programnum != -1:
                prevtime = prevtimes[programnum]
                # must be the abs value or else it'll cause a ping pong reaction
                prevtimes[programnum] = deltatime

                trackthing[j].time = deltatime - prevtime
                programtracks[programnum].append(trackthing[j])

        # track sort out
        midifile.tracks[i] = programtracks[baseprogramnum]
        for j in range(len(programtracks)):
            if len(programtracks[i]) > 0 and j != baseprogramnum:
                # one final check
                hasnoteon = False
                for event in programtracks[j]:
                    if event.type == "note_on":
                        hasnoteon = True
                        break
                if hasnoteon:
                    # uhh... "clever" trust me
                    outputstrings.append(f"{len(midifile.tracks)}-{j} (added from {i}): {fancyPrint(getIInstInfo(j, bankstr))}")
                    midifile.tracks.append(programtracks[j])

        # handle empty stuff smartly
        if notedownnotes:
            for i in range(len(blankarray)):
                if len(notes[i]) > 0:
                    stupidnotes2[i].append([notes[i], basenum[i]])

    outputstrings.sort(key= lambda x: int(x.split("-")[0]))

    for string in outputstrings:
        print(string)

    if len(stupidnotes2) > 0:
        print("\nrhy help:\n")

        finalstupidnotes = []

        # merge everything together, remove empty stuff
        for i in range(len(stupidnotes2)):
            if len(stupidnotes2[i]) > 0:
                basenum = stupidnotes2[i][0][1]
                arrays = stupidnotes2[i]
                domergestack = stupidnotes2[i][0][0]

                index = 0
                while index + 1 < len(stupidnotes2[i]):
                    index += 1
                    domergestack = mergeArrays(domergestack, stupidnotes2[i][index][0])

                domergestack.sort()
                finalstupidnotes.append([i, domergestack, basenum])

        # make it look fancy
        for help in finalstupidnotes:
            rhyinst = getIInstInfoBank(help[0], bankindex)
            subbank = getBank(rhyinst["bank"])
            print(f"for program {help[0]};")
            print(f"with bank {rhyinst["bank"]};")
            for note in help[1]:
                inst = getIInstInfo(note, subbank)
                print(f"at {note + help[2]} ({note}), put {fancyPrint(inst, True)}")
            # space between rhy banks
            print("")

    if len(splitstuff) > 0:
        if len(stupidnotes2) == 0:
            print("")
        print("spl help:\n")

        # make it look fancy
        for spl in splitstuff:
            subbank = getBank(spl[1])
            print(f"for program {spl[0]};")
            print(f"with bank {spl[1]};")
            keysplitindex = int(spl[2].split("_")[2]) - 1
            print(f"with keysplit_table_{keysplitindex + 1};\n")

            keysplitstuff = rtconsts.keysplit_table[keysplitindex]

            keysplitstring = rtconsts.generateKeysplitString(keysplitstuff, spl[3])
            # calc shit now.. fuck?
            for note in keysplitstuff[1]:
                inst = getIInstInfo(note, subbank)
                inststr = f"inst{note}"
                replacewith = fancyPrint(inst) + " at the range of"
                keysplitstring = keysplitstring.replace(inststr, replacewith)
            print(keysplitstring)
            # space between spl banks
            print("")

    if len(midifile.tracks) != ogtracklen:
        midifile = prepMidi(midifile, True)
        midifile.save(filename + "_prep.mid")
        print("new file created for project file maker or something; " + filename + "_prep.mid")
    else:
        print("no new file needed")
    print("")

if filename == "!a":
    for file in os.listdir(os.path.dirname(__file__) + "/"):
        if file.endswith(".mid"):
            run(os.path.dirname(__file__) + "/" + file.removesuffix(".mid"), file.removesuffix(".mid"))
else:
    run(os.path.dirname(__file__) + "/" + filename, filename)