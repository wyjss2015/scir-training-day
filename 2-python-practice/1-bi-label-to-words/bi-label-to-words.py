#!/usr/bin/env python
import sys

def read_instance(fp):
    sentence = []
    while True:
        line = fp.readline()
        if not line:
            yield sentence
            break

        line = line.strip()

        if len(line) == 0:
            yield sentence
            sentence = []
        else:
            sentence.append( line.split() )


def bi2words(chars):
    result = []
    tmp = chars[0][0]
    i = 1
    while i < len(chars):
        char = chars[i]
        if char[1] == 'B':
            result.append(tmp)
            tmp = char[0]
        else:
            tmp += char[0]
        i += 1
    result.append(tmp)
    return result


if __name__=="__main__":
    try:
        fpi = open(sys.argv[1], "r")
    except IOError:
        print >> sys.stderr, "failed to open file."
        sys.exit(1)

    try:
        fpo = open(sys.argv[2], "w")
    except IOError:
        print >> sys.stderr, "failed to open file."
        sys.exit(1)

    for sentence in read_instance(fpi):
        result = bi2words(sentence)
        for char in result:
            fpo.write(char+' ')
        fpo.write('\n')
