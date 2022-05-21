import numpy as np
import pickle
import random

from zxcvbn import zxcvbn

# import models
def tokenization(word):
    tokens = []
    for ch in word:
        tokens.append(ch)
    return tokens

model = pickle.load(open('./backend/rfc.pkl', 'rb'))
vectorizer = pickle.load(open('./backend/vectorizer.pkl', 'rb'))

specialChar = ['!', '"', "'", '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=',
                    '`', '{', '}', '[', ']', '\\', '|', ':', ':', '<', ',', '>', '.', '?', '/']

# get list of english words
file_n = open("./dictionary/nouns.txt", "r")
file_a = open("./dictionary/adjectives.txt", "r")

nouns = [(line.strip()).split() for line in file_n]
adjectives = [(line.strip()).split() for line in file_a]

file_n.close()
file_a.close()

# return json with all information
def power(str):
    json = {}

    # empty input
    if len(str) == 0:
        return ""
    res = zxcvbn(str)
    print(res)

    # get score
    json['score'] = score(str)

    # get buffs
    json['buffs'] = buff(str, res['feedback'], res['sequence'], score(str))

    # get advice
    json['advice'] = advice(str, res['feedback'], res['sequence'])

    # for testing
    json['feedback'] = res['feedback']
    for seq in res['sequence']:
        seq['regex_match'] = ""
    json['sequence'] = res['sequence'][0]

    return json

# get buff
def buff(str, feedback, sequence, cur):
    buffs = {}
    list = []

    # get feedback from zxcvbn
    suggestions = feedback['suggestions']
    warnings = feedback['warning']

    buffFunctions = [
        "plusWord", "plusNum", "grow", "leaf", "remove", "split", "substitution", "clone", "arrow", "emote"
    ]

    for func in buffFunctions:
        buffTuple = globals()[func](str)
        buffedScore = score(buffTuple[1])
        if (buffedScore > cur):
            buffTuple.append(buffedScore - cur)
            list.append(buffTuple)

    # sort by ascending strength
    # list.sort(key = lambda x: x[2], reverse=True)
    random.shuffle(list)
    for i in range(len(list)):
        buffs[i] = list[i]

    return buffs

# add words
def plusWord(pw):
    ind = random.choice([0, 1])
    rand = ""

    # get random noun or adjective
    if ind == 1:
        rand = random.choice(nouns)[0]
    elif ind == 0:
        rand = random.choice(adjectives)[0]

    # add to current word
    buffedStr = pw + "-" + rand

    return ["Word Drop", buffedStr]

# add numbers
def plusNum(pw):
    # get random number
    num = random.randint(100, 999)

    # add to current word
    buffedStr = pw + str(num)

    return ["Number Punch", buffedStr] 

# random capitalization
def grow(pw):
    ind = random.choice([0, 1])
    buffedStr = ""
    
    for i in range(len(pw)):
        if i % 2 == ind:
            buffedStr += pw[i].upper()
        else:
            buffedStr += pw[i]

    return ["GROW", buffedStr] 

# add a leaf
def leaf(pw):
    leaf = random.choice(specialChar)

    ind = random.choice([0, 1])
    if ind == 1:
        buffedStr = leaf + pw
    else:
        buffedStr = pw + leaf

    return ["@Leaf", buffedStr] 

# remove a random character
def remove(pw):
    # random index
    ind = random.randint(0, len(pw) - 1)

    if (len(pw) <= 1):
        buffedStr = pw
    else:
        # remove char at that index
        buffedStr = pw[:ind] + pw[ind + 1:]

    return ["Invisibility Cloak", buffedStr] 

# splits in half
def split(pw):
    # middle index
    mid = int(len(pw) / 2)

    buffedStr = pw[:mid] + '_' + pw[mid:]

    return ["Earthquake", buffedStr] 

# replaces with different characters
def substitution(pw):
    buffedStr = ""
    for i in range(len(pw)):
        ch = pw[i]
        if (ch == 'S' or ch == 's'):
            ch = random.choice(['$', '5'])
        elif (ch == 'I' or ch == 'i'):
            ch = random.choice(['1', '!'])
        elif (ch == 'A' or ch == 'a'):
            ch = '@'
        elif (ch == 'T' or ch == 't'):
            ch = 7
        elif (ch == 'E' or ch == 'e'):
            ch = 3
        elif (ch == 'G' or ch == 'g'):
            ch = random.choice(['6', '9'])
        elif (ch == 'O' or ch == 'o'):
            ch = 0
        elif (ch == 'B' or ch == 'b'):
            ch = 8
        buffedStr += str(ch) 
    
    return ["B33p-B00p", buffedStr]

# doubles the password
def clone(pw):
    buffedStr = pw + ":" + pw
    return ["Shadow Clone", buffedStr]

# adds an arrow
def arrow(pw):
    buffedStr = '-' + pw + '->'
    return ["Cupid's Arrow", buffedStr]

# add an emoticon
def emote(pw):
    faces = [':)', ':D', '^-^', ';)', ':p', ':o', 'O.O', ':3']
    face = random.choice(faces)

    buffedStr = pw + face
    return ["Emote", buffedStr]

# get feedback
def advice(pw, feedback, sequence):
    advice = []

    if (len(pw) < 10):
        advice.append("Hmmmm this password seems a bit too short...")
    if (upperCount(pw) < 3):
        advice.append("CAPITAL LETTERS ARE COOL YOU SHOULD ADD SOME")
    if (specialCount(pw) < 3):
        advice.append("7ry @dd1n6 50m3 $p3c!@l ch@arac73r5")
    if "Avoid sequences." in feedback["suggestions"]:
        advice.append("abcdefg, I spy a sequence 123")
    if "Names and surnames by themselves are easy to guess."  in feedback["warning"]:
        advice.append("Oh, I see someone's name here")
    if "Dates are often easy to guess." in feedback["warning"]:
        advice.append("Is it someone's birthday? I noticed the date you included")

    random.shuffle(advice)

    return advice

# get number of capital letters
def upperCount(pw):
    return sum(map(str.isupper, pw))

# get number of special characters
def specialCount(pw):
    count = 0
    for i in range(len(pw)):
        if pw[i] in specialChar:
            count += 1
    return count

# get score of a string
def score(str):
    # zxcvbn
    res = zxcvbn(str)

    # random forest classifier model
    predict_data = np.array([str])
    prediction = vectorizer.transform(predict_data)

    # return sum
    return res['score'] + int(model.predict(prediction)[0]) 
