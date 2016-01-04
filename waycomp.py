# -*- coding: utf-8 -*-

"""
Created on Thu Sep 26 16:55:14 2015

@author: Matthieu Walraet
"""

import board
from random import choice
from math import log10



def randomPlay(b, m1, m2, n):
    """ b a board
        m1 allowed moves for 1 
        m2 allowed moves for 2 
        n number of iteration """
    b.prt()

    for i in range(n):
        c= choice([1,2])
        p = choice(m1 if c==1 else m2)
        
        nB = b.play1safe(c, p)
        if nB:
            b = nB
            b.prt()
            print("            %s"%(i,))            



class waysComp(object):
    
        
    def __init__(self, target, m1=None, m2=None):
        """
        target is target position (a Board)
        m1 allowed moves for 1 
        m2 allowed moves for 2     """
        
        self._memo = dict()  # for memoization       
        t = (target.getPos(), 0)
        self._memo[t] = (0, 1)  # lenght of longest way, number of different ways 
        
        self._m1 = m1
        self._m2 = m2        
        
        if m1 is None:
            self._m1 = target.getStonesOfColor(1)
        else: 
            self._m1 = list(m1)
            
        if m2 is None:
            self._m2 = []
        else:
            self._m2 = list(m2)            
        
    
    def possibleWays(self, b, outs=0):
        """
        b is a starting position  (a Board)
        outs number of move still to be played outside that position

        return a tupple (lenght of longest way, number of different ways)    
        """

        k = (b.getPos(), outs)
        r = self._memo.get( k )
        if r:
            return r
        else:
            longestWays = []
            numberWays = 0
            # 1 moves
            for s1 in self._m1:
                bNext = b.play1safe(1, s1)
                if bNext:
                    l, nb = self.possibleWays(bNext, outs)
                    numberWays += nb
                    longestWays.append(l)
            # 2 moves
            for s2 in self._m2:
                bNext = b.play1safe(2, s2)
                if bNext:
                    l, nb = self.possibleWays(bNext, outs)
                    numberWays += nb
                    longestWays.append(l)   
            # move 1 outside
            if outs:
                l, nb = self.possibleWays(b, outs-1)
                numberWays += nb * outs
                longestWays.append(l)  

            if numberWays:
                r = max(longestWays)+1, numberWays
            else:
                r = 0, 0

            self._memo[k] = r   
            return r 
    
def p42():
    for i, b in enumerate(board.validWithHalfBorders(4, 2)):
        b.prt()
        print("            %s"%(i,))


def tRand():
    b = board.Board(4, 3)
    
    randomPlay(b, list(range(12)), list(range(12)), 200)   

def ex22():
    t = board.Board(2, 2, [0, 1,
                            1, 1]) 
    ways = waysComp(t, m2= range(4))
     
    
    for i, b in enumerate(board.validPos(2, 2)):  
        b.prt()
        l, nb = ways.possibleWays(b, 0)
        print("        %s longest: %s   numbers: %s"%(i, l, nb))

def testOuts():
    """ Check "outs" gives correct result
    """

    t = board.Board(4, 3, [0, 1, 1, 1, 
                           1, 1, 0, 0, 
                           1, 0, 0, 1 ] )


    ways_1 = waysComp(t, [5, 11], 
                         [5, 6, 7, 9, 10, 11])
    
    b = board.Board(4, 3, [0, 1, 1, 1, 
                           1, 0, 0, 0, 
                           1, 0, 0, 0 ] )
    
    
    print(ways_1.possibleWays(b, 0))  # 11, 3242 = 5!4! + 5! + 5! +2
    print(ways_1.possibleWays(b, 3))

    t_2 = board.Board(4, 4, [0, 1, 1, 0, 
                             1, 1, 1, 1,
                             1, 1, 0, 0, 
                             1, 0, 0, 1 ] )
  
    ways_2 = waysComp(t_2, [1, 2, 4, 9, 15],   # 1, 2, ,4 replace the 3 outs
                           [9, 10, 11, 13, 14, 15])
    
    b_2 = board.Board(4, 4, [0, 0, 0, 0,
                             0, 1, 1, 1, 
                             1, 0, 0, 0, 
                             1, 0, 0, 0 ] )
    
    print(ways_2.possibleWays(b_2, 0))  # Should be the same as previous line


def halfBorders42build():
    start = board.Board(5, 3)
    a2 = [6, 7, 8, 9, 11, 12, 13, 14]

    lengthTab = []
    nblogTab = []

    for i, b in enumerate(board.validWithHalfBorders(4, 2)):
        b.prt()
        ways = waysComp(b, m2=a2)       
        l, nb = ways.possibleWays(start, 1)
        nb_log= log10(nb)

        print("        %s longest: %s   numbers: %s  log: %s"%(i, l, nb, nb_log))        
        lengthTab.append(l)
        nblogTab.append(nb_log)

    print('\n\n')
    print("Total   length: %s    nb=10^%s"%(sum(lengthTab), sum(nblogTab)))

def halfBorders42Fillwith1():
    t = board.Board(5, 3, [0, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1])
    
    a = [6, 7, 8, 9, 11, 12, 13, 14]
    ways = waysComp(t, a, a)
    
    lengthTab = []
    nblogTab = []

    for i, b in enumerate(board.validWithHalfBorders(4, 2)):
        b.prt()
        l, nb = ways.possibleWays(b, 0)
        nb_log= log10(nb)

        print("        %s longest: %s   numbers: %s  log: %s"%(i, l, nb, nb_log))        

        lengthTab.append(l)
        nblogTab.append(nb_log)
    
    print('\n\n')
    print("Total   length: %s    nb=10^%s"%(sum(lengthTab), sum(nblogTab)))
        

def threeBorders42():
    valHalf42 = 4779
    start = board.Board(5, 4, [0, 1, 1, 1, 1,
                               1, 0, 0, 0, 0,
                               1, 0, 0, 0, 0,
                               0, 1, 1, 1, 1])    
    
    t = board.Board(5, 4, [0, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           0, 1, 1, 1, 1])
    
    a = [6, 7, 8, 9, 11, 12, 13, 14]
    ways = waysComp(t, a, a)
    
    lengthTab = []
    nblogTab = []

    for i, b in enumerate(board.validWithThreeBorders(4, 2)):
        if i >= 0:
            b.prt()
            l, nb = ways.possibleWays(b, 0)
            nb_log= log10(nb)
    
            print("        %s"%(i))
            print("           fill longest: %s   numbers: %s  log: %s"%(l, nb, nb_log))        
    
            waysBuild = waysComp(b, a, a)       
            b_l, b_nb = waysBuild.possibleWays(start, 0)
            b_nb_log= log10(b_nb)

            print("         build  longest: %s   numbers: %s  log: %s"%(b_l, b_nb, b_nb_log))        
            print("         total  longest: %s   numbers: %s  log: %s"%(l+b_l, nb * b_nb, nb_log + b_nb_log))        

    
            lengthTab.append(l + b_l)
            nblogTab.append(nb_log + b_nb_log)
    
    print('\n\n')
    print("Total   length: %s    nb=10^%s"%(sum(lengthTab), sum(nblogTab)))
    print()
    print('but taking only same number of valid with half border : %s'%(valHalf42,))
    lengthTab.sort(reverse = True)
    nblogTab.sort(reverse = True)
    print("Total   length: %s    nb=10^%s"%(sum(lengthTab[:valHalf42]), 
                                            sum(nblogTab[:valHalf42])))
       
def main():
    # testOuts()
    #halfBorders42Fillwith1()
    # halfBorders42build()
    threeBorders42()
       
if __name__ == '__main__':
    main()