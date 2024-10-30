const midifile = require("midi-file");
const fs = require("node:fs");

let midisName = ["s_shuji_bgm1", "s_shuji_bgm2", "s_shuji_bgm3", "s_shuji_bgm_end"];
let outputMidiName = "s_shuji_bgm";

let parsedMidis = [];
for (let i = 0; i < midisName.length; i++)
{
    parsedMidis.push(midifile.parseMidi(fs.readFileSync(midisName[i].replace("!", "") + ".mid")));
}
let outputMidi = parsedMidis[0];

if (midisName.length > 1)
{
    for (let i = 1; i < parsedMidis.length; i++)
    {
        outputMidi = mergeMidi(outputMidi, parsedMidis[i]);
    }
}
else
    outputMidi = removeMarkers(outputMidi);
fs.writeFileSync(`${outputMidiName}.mid`, Buffer.from(midifile.writeMidi(outputMidi)));
fs.writeFileSync(`${outputMidiName}.mid.json`, JSON.stringify(outputMidi, null, 4));

function mergeMidi(midiA = {}, midiB = {})
{
    if (midiA.header.ticksPerBeat != midiB.header.ticksPerBeat)
        console.error("OH GOD DIFFERENT BEAT PER TICK");
    let ret = {
        header: {
            format: midiA.header.format,
            numTracks: Math.max(midiA.header.numTracks, midiB.header.numTracks),
            ticksPerBeat: midiA.header.ticksPerBeat,
        },
        tracks: []
    }
    let maxDT = 0;
    let channelDTs = [];
    for (let i = 0; i < ret.header.numTracks; i++)
        channelDTs.push(0);

    for (let i = 0; i < midiA.tracks.length; i++)
    {
        let track = midiA.tracks[i];
        if ((i + 1) > ret.tracks.length)
            ret.tracks.push([]);
        for (let j = 0; j < track.length; j++)
        {
            let event = track[j];
            if (event.type != "endOfTrack" && event.type != "marker")
                ret.tracks[i].push(event);
            channelDTs[i] += event.deltaTime;
        }
        maxDT = Math.max(channelDTs[i], maxDT);
    }
    for (let i = 0; i < midiB.tracks.length; i++)
    {
        let track = midiB.tracks[i];
        if ((i + 1) > ret.tracks.length)
            ret.tracks.push([]);
        let firstEvent = true;
        for (let j = 0; j < track.length; j++)
        {
            let event = track[j];
            if (event.type == "marker")
                continue;
            if (firstEvent)
                event.deltaTime += maxDT - channelDTs[i];
            firstEvent = false;
            ret.tracks[i].push(event);
        }
    }

    return ret;
}
function removeMarkers(midiA = {})
{
    let ret = {
        header: {
            format: midiA.header.format,
            numTracks: midiA.header.numTracks,
            ticksPerBeat: midiA.header.ticksPerBeat,
        },
        tracks: []
    }
    for (let i = 0; i < midiA.tracks.length; i++)
    {
        let track = midiA.tracks[i];
        if ((i + 1) > ret.tracks.length)
            ret.tracks.push([]);
        for (let j = 0; j < track.length; j++)
        {
            let event = track[j];
            if (event.type != "marker")
                ret.tracks[i].push(event);
        }
    }
    return ret;
}