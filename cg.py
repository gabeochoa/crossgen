# This Python file uses the following encoding: utf-8
import sys
import json
from random import random, shuffle
from collections import defaultdict


spacechar = u'███'
_end = '_end_'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Trie(object):
    """docstring for Trie"""
    def __init__(self, words):
        super(Trie, self).__init__()
        self.dictionary = dict()
        self._build_tree(words)

    def _get_fully(self, word):
        '''
            car -> {'c': {'a': {'r'}  }   }
        '''
        if len(word) == 0:
            return {_end:_end}
        return {word[0]: self._get_fully(word[1:])}

    def add_trie(self, word):
        spot = self.dictionary
        #apple
        # {'a': {'p':{}, 'b':{} }}
        i = 0
        while i < len(word):
            l = word[i]
            next_d = spot.get(l, {})
            if next_d == {}:
                # nothing there
                spot[l] = self._get_fully(word[i+1:])
                break
            else:
                spot = spot[l]
            i+=1

    def print_all(self, d=None, current=''):
        # if type(d) != dict:
        #     print current
        #     return
        if d is None:
            d = self.dictionary

        for x in d.keys():
            if d[x] == _end:
                print current
                continue
            self._print_all(d[x], current=current+x)

    def find_in(self, word, d=None):
        if d is None:
            d = self.dictionary
        if _end in d and len(word) == 0:
            return True
        if len(word) == 0:
            return False
        if word[0] not in d:
            return False
        return self.find_in(word[1:], d=d[word[0]])

    def _build_tree_from_file(self, fn):
        with open(fn) as f:
            lines = f.readlines()
        self.lines = lines[:100]
        for word in self.lines:
            self.add_trie(word.strip())
        self.seed = self.get_random_word()

    def _build_tree(self, words):
        self.lines = words
        for word in self.lines:
            self.add_trie(word.strip())
        self.seed = self.get_random_word()

    def get_random_word(self):
        return self.lines[int(random()*len(self.lines))].strip()

    def _get_word_from_subset(self, subset):
        output = ""
        x = int(random()*len(subset.keys()))
        while subset[subset.keys()[x]] != _end:
            subset_k = subset.keys()[x]
            output += subset_k
            subset = subset[subset_k]
            x = int(random()*len(subset.keys()))
        return output

    def get_word(self, chars, used=[]):
        # get random letter to branch off of
        orig = chars
        chars = list(chars)
        shuffle(chars)
        i = 0
        rlet = chars[i]
        cont = None
        while cont is None:
        #     print "letter chosen: :", rlet
        #     print "index: ", orig.index(rlet)
            subset = self.dictionary.get(rlet, None)
            if subset is None:
                cont = None
                if i > len(chars):
                    return # ran out of letters to try
                i += 1
                rlet = chars[i]
                continue # retry with a different letter
            else:
                out = rlet + self._get_word_from_subset(subset), orig.index(rlet)
                if out in used:
                    print "word already used"
                    return None
                return out
        return None

class Puzzle():
    def __init__(self, size):
        self.clues_for_word = self._build_clues_dict("clues.txt")
        self.trie = Trie(self.clues_for_word.keys())
        self.seed = self.trie.seed
        self.data = [[spacechar for _ in range(size)] for _ in range(size)]
        self.size = size
        self.empty = size * size
        self.words_used = []

    def _build_clues_dict(self, fn):
        ret = defaultdict(list)
        with open(fn, 'r') as f:
            lines = f.readlines()
        lines = lines[:1000]
        for l in lines:
            clue, word = l.split("\t")[:2]
            ret[word] += [clue]
        return ret

    def draw(self):
        out = ""
        for x in self.data:
            for y in x:
                if y == ' ':
                    out += " "
                else:
                    out += y
            out += '\n'
        print out

    def check_place(self, x, y, word, orient):
        if(orient==1 and x+len(word) <= self.size):
            for i in range(len(word)):
                if self.data[x+i][y] != word[i]:
                    continue
                if self.data[x+i][y] != spacechar:
                    print self.data[x][y+i], word[i]
                    return False
        elif(orient==-1 and y+len(word) <= self.size):
            for i in range(len(word)):
                if self.data[x][y+i] != word[i]:
                    continue
                if self.data[x][y+i] != spacechar:
                    print self.data[x][y+i], word[i]
                    return False
        return True

    def place_word(self, x, y, word, orient):
        try:
            if not self.check_place(x, y, word, orient):
                print "couldnt fit", x, y, word
                return 0, ()
        except:
            return 0, ()

        if(orient==1 and x+len(word) <= self.size):
            for i in range(len(word)):
                let = ' '+word[i]+' '
                if let == self.data[x+i][y]:
                    continue
                self.data[x+i][y] = let
                self.empty -= 1
            # placed word correctly
            self.words_used.append(word)
            return orient, (x, y, word)
        elif(orient==-1 and y+len(word) <= self.size):
            for i in range(len(word)):
                let = ' '+word[i]+' '
                if let == self.data[x][y+i]:
                    continue
                self.data[x][y+i] = let
                self.empty -= 1
            # placed word correctly
            self.words_used.append(word)
            return orient, (x, y, word)

        return 0, ()

    def make(self):
        a = None
        b = None
        prev = None
        orient= None

        while True:
            success, data = self.next(a=a, b=b, prev=prev, orient=orient)
            if success == 0:
                return success, data
            print success, data, self.empty
            a, b, prev = data
            orient = success
            if self.empty < 20:
                return success, data


    def next(self, a=None, b=None, prev=None, orient=None):
        if a is None:
            a = int(random() * self.size)
        if b is None:
            b = int(random() * self.size)
        if prev is None:
            prev = self.seed
        if orient is None:
            orient = 1

        new_orient = orient * -1

        word, pos = self.trie.get_word(prev, self.words_used)
        if orient == 1:
            a += pos
        else:
            b += pos
        print a, b, word, new_orient
        success, data = self.place_word(a, b, word, orient=new_orient)
        if success != 0:
            return success, data
        else:
            print "no success"
            return 0, ()

def main():
    if len(sys.argv) == 1:
        size = 20
    else:
        size = int(sys.argv[1])

    puzz = Puzzle(size)
    puzz.make()
    puzz.draw()

if __name__ == '__main__':
    main()













