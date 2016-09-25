#!/usr/bin/env python
import cPickle as pickle
import sys

def max_match_segment(line, dic):
    segments = []
    while len(line) != 0:
        index = len(line)
        while index>0:
            if line[:index] in dic:
                segments.append(line[:index])
                line = line[index:]
                break
            else:
                index -= 1
        if index == 0:
            segments.append(line[0])
            line = line[1:]
    return segments

if __name__=="__main__":

    try:
        fpi=open(sys.argv[1],'r')
    except:
        print >> sys.stderr, "failed to open file"
        sys.exit(1)

    try:
        dic = pickle.load(open(sys.argv[2],'rb'))
    except:
        print >> sys.stderr, "failed to load dict"
        sys.exit(1)

    with open('output','w') as r:
        for line in fpi:
            r.write('\t'.join(max_match_segment(line.strip(), dic))+'\n')
            #max_match_segment(line.strip(),dic)

