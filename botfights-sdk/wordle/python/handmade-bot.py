# sample-bot.py

# sample bot to play wordle. see wordle.py for how to play.
# 


import random
import pandas as pd

FN_WORDLIST = 'wordlist.txt'


g_wordlist = None
def get_wordlist():
    global g_wordlist
    if None == g_wordlist:
        g_wordlist = []
        for i in open(FN_WORDLIST).readlines():
            i = i[:-1]
            g_wordlist.append(i)
    return g_wordlist


# this has lots of false positives, only pay attention to 3s
#
def could_match(target, guess, feedback):
    for i, ch in enumerate(feedback):
        if '3' == ch:
            if target[i] != guess[i]:
                return False
        else:
            if target[i] == guess[i]:
                return False
            if ch == '2':
                check = False
                for x in range(5):
                    if target[x] == guess[i]:
                        check = True
                if check == False:
                    return False
            else:
                if guess[i] in target and guess.count(guess[i]) == 1:
                    return False
                    



    return True


def play(state):
    # state looks like: "-----:00000,arose:31112,amend:31211"
    possible = get_wordlist()
    letters ='abcdefghijklmnopqrstuvwxyz'
    #These are the least common letter to the most common letters ranked
    #letterdict = {'q': 0, 'x': 1, 'j': 2, 'z': 3, 'v': 4, 'f': 5, 'w': 6, 'k': 7, 'b': 8, 'g': 9, 'h': 10, 'm': 11, 'p': 12, 'c': 13, 'y': 14, 'd': 15, 
    #'u': 16, 'n': 17, 't': 18, 'l': 19, 'i': 20, 'r': 21, 'o': 22, 'a': 23, 'e': 24, 's': 25}
    # this makes the first guess arose which is testing the most common letters in the word list
    if len(state) == 11:
        return 'arose'
    else:        
        for pair in state.split(','):
            guess, feedback = pair.split(':')
            possible = list(filter(lambda x: could_match(x, guess, feedback), possible))
        letterdf = pd.DataFrame({'words':possible})

        for x in letters:
            letterdf.insert(letterdf.columns.shape[0], x, letterdf['words'].str.count(x))
        letterdict = {}
        for x in range(len((letterdf.iloc[:,1:27] > 0).sum().sort_values(ascending=True))):
            letterdict[(letterdf.iloc[:,1:27] > 0).sum().sort_values(ascending=True).index[x]] = x
        commonalitydict = {}
        for word in possible:
            commonalityscore = 0
            #removing duplicate letters
            duplicates = []
            for letter in word:
                if letter not in duplicates:
                    commonalityscore += letterdict[letter]
                duplicates.append(letter)
            commonalitydict[word] = commonalityscore
        possible = []
        for x in commonalitydict:
            if commonalitydict[x] == max(commonalitydict.values()):
                possible.append(x)
        
        return random.choice(possible)

