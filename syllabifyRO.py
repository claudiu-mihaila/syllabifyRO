#!/usr/bin/python
# -*- coding: utf-8  -*-

"""

"""

import operator
import sys
import re
import codecs
import getopt

def syllabify(word):
    global rules

    hyphenated = u""
    for letter in word:
        hyphenated += letter + " "
        
    word = u"." + word + u"."
    hyphenated = u"." + hyphenated[:-1] + u"."
    
    good_rules = []
    good_texts = []
    good_blans = []
    for rule in rules:
        rule_text = ""
        rule_blan = ""
        for l in rule:
            if l not in "1234567890":
                rule_text += l
                rule_blan += l
            else:
                rule_blan += " "
        
        if (rule_text in word):
            good_rules.append(rule)
            good_texts.append(rule_text)
            good_blans.append(rule_blan)
    
    goodies = zip(good_texts, good_blans, good_rules)
    
    parts = []
    parts.append(hyphenated)
    for (t, b, r) in goodies:
        w = hyphenated
        w = w.replace(b, r)
        parts.append(w)
        
    hyphenated = ""
    for i in range(len(parts[0])):
        if (parts[0][i] in "0123456789 "):
            max = parts[0][i]
            for j in parts:
                if (j[i] > max):
                    max = j[i]
            if (max in "13579"):
                hyphenated += "."
        else:
            hyphenated += parts[0][i]

    return hyphenated[1:-1]

def loadDic(file):
    rules = []
    
    print "Loading dictionary..."
    
    file = open(file, 'r')
       
    encoding = file.readline().strip()
    print "Using %s encoding." % encoding
    
    line = file.readline().strip()
    while (line != ''):
        if (line[0] != '%'):
            rule = unicode(line, encoding)
            if (rule != ""):
                rules.append(rule)
        line = file.readline().strip()    
    return rules

def usage():
    print "Usage of script:"
    print sys.argv[0] + " -arg <value> [--opt]"
    print
    print "Arguments:"
    print "-d \t\t specifies the dictionary file"
    print
    print "Options:"
    print "-h \t\t the help menu"

    
try:
    opts, args = getopt.getopt(sys.argv[1:],"hd:")
except getopt.GetoptError:
    usage()
    sys.exit(2)

try:    
    dictFile = ""

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-d"):
            print "Using dictionary in %s." % arg
            dictFile = arg

    if dictFile == "":
        print "invalid arguments, dictionary file must be given."
        sys.exit(1)
        
    rules = loadDic(dictFile)
    
    syllables = syllabify(args[0])
    print syllables    
    
finally:
    sys.exit(0)