# This Python file uses the following encoding: utf-8
import sys
import json
from random import random


spacechar = u'███'
_end = '_end_'

class Trie(object):
    """docstring for Trie"""
    def __init__(self, fn):
        super(Trie, self).__init__()
        self.dictionary = dict()
        self._build_tree(fn)

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

    def _build_tree(self, fn):
        with open(fn) as f:
            lines = f.readlines()
        self.lines = lines[:100]
        for word in self.lines:
            self.add_trie(word.strip())
        self.seed = self.get_random_word()

    def get_random_word(self):
        return self.lines[int(random()*len(self.lines))].strip()

    def get_word(self, chars):
        return self.get_random_word()

class Puzzle():
    def __init__(self, size):
        self.trie = Trie("words_alpha.txt")
        self.seed = self.trie.seed
        self.data = [[spacechar for _ in range(size)] for _ in range(size)]
        self.size = size

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


    def place_word(self, x, y, word, orient):
        if(orient==1 and x+len(word) <= self.size):
            for i in range(len(word)):
                self.data[x+i][y] = ' '+word[i]+' '
            return 1, (x, y, word)
        elif(orient==-1 and y+len(word) <= self.size):
            for i in range(len(word)):
                self.data[x][y+i] = ' '+word[i]+' '
            return -1, (x, y, word)

        print "couldnt fit", x, y, word
        return 0, ()

    def make(self):
        while True:
            success, data = self.next()
            if success != 0:
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

        word = self.trie.get_word(prev)
        success, data = self.place_word(a, b, word, orient=orient)
        if success != 0:
            return success, data
        else:
            return 0, ()

def main():
    if len(sys.argv) == 1:
        size = 20
    else:
        size = int(sys.argv[1])

    puzz = Puzzle(size)
    orient, start = puzz.make()
    print start
    x, y, prev = start
    puzz.next(a=x, b=y, prev=prev, orient=orient*-1)

    puzz.draw()

if __name__ == '__main__':
    main()













