import hashlib, binascii
generatestr = input("generate or try guess (g to generate) ")
generate = len(generatestr) > 0 and generatestr[0].lower() == "g"

def runhash(input, hashalgor):
    match hashalgor:
        case 8:
            return ('%08X' % (binascii.crc32(input) & 0xffffffff)).lower()
        case 7:
            return hashlib.blake2s(input).hexdigest()
        case 6:
            return hashlib.sha512(input).hexdigest()
        case 5:
            return hashlib.sha256(input).hexdigest()
        case 4:
            return hashlib.sha1(input).hexdigest()
        case 3:
            return hashlib.sha384(input).hexdigest()
        case 2:
            return hashlib.sha224(input).hexdigest()
        case 1:
            return hashlib.blake2b(input).hexdigest()
        case 0 | _:
            return hashlib.md5(input).hexdigest()

hashcracker = [0]
indexindex = 0

def increasehashcracker(i = 0):
    global hashcracker
    if hashcracker[i] + 1 >= 9:
        hashcracker[i] = 0
        if len(hashcracker) <= (i + 1):
            hashcracker.append(0)
            return
        else:
            increasehashcracker(i + 1)
    else:
        hashcracker[i] += 1



if not generate:
    ins = input("input string? ")
    outs = input("output hash? ").lower()

    while True:
        toworkon = ins
        for hash in hashcracker:
            toworkon = runhash(toworkon.encode("ascii"), hash)
        if toworkon == outs:
            print(f"{indexindex} (l{len(hashcracker)}): {toworkon} vs {outs} is true")
            finalhashalg = "hashalgorder is: "
            for i in range(len(hashcracker)):
                if i != 0:
                    finalhashalg += "->"
                match hashcracker[i]:
                    case 0:
                        finalhashalg += "md5"
                    case 1:
                        finalhashalg += "blake2b"
                    case 2:
                        finalhashalg += "sha224"
                    case 3:
                        finalhashalg += "sha384"
                    case 4:
                        finalhashalg += "sha1"
                    case 5:
                        finalhashalg += "sha256"
                    case 6:
                        finalhashalg += "sha512"
                    case 7:
                        finalhashalg += "blake2s"
                    case 8:
                        finalhashalg += "crc32"
            print(finalhashalg)
            break
        else:
            print(f"{indexindex} (l{len(hashcracker)}): {toworkon} vs {outs} is not true")
        indexindex += 1
        increasehashcracker()
else:
    randomstring = input("input random base string ")

    while True:
        toworkon = randomstring
        for hash in hashcracker:
            toworkon = runhash(toworkon.encode("ascii"), hash)
        print(f"{indexindex} (l{len(hashcracker)}): {toworkon}")
        indexindex += 1
        increasehashcracker()