# -*- coding: utf-8 -*-

"""
Created on Oct 3, 2015

@author: Matthieu Walraet
"""

import board
from math import log10





class waysCompB(object):
    """ As waysComp, except that given a start and a target,
        we can compute quickly number of ways for s->i and i->t 
        for all intermediate positions
        Way comp can only give i->t 
        
    """
        
    def __init__(self, start, target, outs=0, m1=None, m2=None):
        """
        start is starting position
        target is target position (a Board)
        m1 allowed moves for 1 
        m2 allowed moves for 2     """
        
        self._memo = dict()  # for memoization       
        t = (target.getPos(), 0)
        self._memo[t] = (0, 1, [])  # lenght of longest way, 
                                    # number of different ways
                                    # previous moves

        self._memoBack = dict()
        tf = (start.getPos(), outs)
        self._memoBack[tf] = (0, 1)
        
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

        self.possibleWays(start, outs)
    
    
    def possibleWays(self, b, outs=0, pk=None):
        """
        b is a starting position  (a Board)
        outs number of move still to be played outside that position
        pk, the parent key

        return a tupple (lenght of longest way, number of different ways)    
        """

        k = (b.getPos(), outs)
        r = self._memo.get( k )
        if r:
            if pk:
                r[2].append(pk)
            return r[0], r[1]
        else:
            longestWays = []
            numberWays = 0
            # 1 moves
            for s1 in self._m1:
                bNext = b.play1safe(1, s1)
                if bNext:
                    l, nb = self.possibleWays(bNext, outs, k)
                    numberWays += nb
                    longestWays.append(l)
            # 2 moves
            for s2 in self._m2:
                bNext = b.play1safe(2, s2)
                if bNext:
                    l, nb = self.possibleWays(bNext, outs, k)
                    numberWays += nb
                    longestWays.append(l)   
            # move 1 outside
            if outs:
                l, nb = self.possibleWays(b, outs-1, k)
                numberWays += nb * outs
                longestWays.append(l)  

            if numberWays:
                r = max(longestWays)+1, numberWays, []
                if pk:
                    r[2].append(pk)
            else:
                r = 0, 0, []
                if pk:
                    r[2].append(pk)
                    
            self._memo[k] = r   
            return r[0], r[1] 


    def possibleWaysBack(self, bt, outs=0):
        """
        bt is a intermediate position  as a tuple
        outs number of move still to be played outside that position
        compute the number of ways (and max length) of playing from start to here

        return a tupple (lenght of longest way, number of different ways)    
        """

        k = (bt, outs)
        
        r = self._memoBack.get( k )
        if r:
            return r
        else:
            longestWays = []
            numberWays = 0
            
            m_bt = self._memo.get(k)
            
            if m_bt:
                for pred in m_bt[2]:
                    l, nb = self.possibleWaysBack(*pred)
                    numberWays += nb
                    longestWays.append(l)                    
            
            else:
                print(" %s is not in possible positions"%(k,))


            if numberWays:
                r = max(longestWays)+1, numberWays
            else:
                r = 0, 0

            self._memoBack[k] = r   
            return r

   


def halfBorders42(outs=1):
    start = board.Board(5, 3)    
    
    t = board.Board(5, 3, [0, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1])
    
    a = [6, 7, 8, 9, 11, 12, 13, 14]
    ways = waysCompB(start, t, outs, None, a)
    
    lengthTab = []
    nblogTab = []

    for i, b in enumerate(board.validWithHalfBorders(4, 2)):
        if i >=0 :
            b.prt()
            l, nb = ways.possibleWays(b, 0)
            nb_log= log10(nb)
    
            print("        %s"%(i))
            print("           fill longest: %s   numbers: %s  log: %s"%(l, nb, nb_log))        
    
            b_l, b_nb = ways.possibleWaysBack(b.getPos(), 0)
            b_nb_log=log10(b_nb)

            print("         build  longest: %s   numbers: %s  log: %s"%(b_l, b_nb, b_nb_log))        
            print("         total  longest: %s   numbers: %s  log: %s"%(l+b_l, nb * b_nb, nb_log + b_nb_log))        

            lengthTab.append(l + b_l)
            nblogTab.append(nb_log + b_nb_log)
    
    print('\n\n')
    print("Total   length: %s    nb=10^%s"%(sum(lengthTab), sum(nblogTab)))

def halfBorders22(outs=1):
    start = board.Board(3, 3)    
    
    t = board.Board(3, 3, [0, 1, 1, 
                           1, 1, 1, 
                           1, 1, 1 ])
    
    a = [4, 5, 7, 8]
    ways = waysCompB(start, t, outs, None, a)
    
    lengthTab = []
    nblogTab = []

    for i, b in enumerate(board.validWithHalfBorders(2, 2)):
        if i >=0 :
            b.prt()
            l, nb = ways.possibleWays(b, 0)
            nb_log= log10(nb)
    
            print("        %s"%(i))
            print("           fill longest: %s   numbers: %s  log: %s"%(l, nb, nb_log))        
    
            b_l, b_nb = ways.possibleWaysBack(b.getPos(), 0)
            b_nb_log=log10(b_nb)

            print("         build  longest: %s   numbers: %s  log: %s"%(b_l, b_nb, b_nb_log))        
            print("         total  longest: %s   numbers: %s  log: %s"%(l+b_l, nb * b_nb, nb_log + b_nb_log))        

            lengthTab.append(l + b_l)
            nblogTab.append(nb_log + b_nb_log)
    
    print('\n\n')
    print("Total   length: %s    nb=10^%s"%(sum(lengthTab), sum(nblogTab)))
          

          

def threeBorders42(outs=0, startPos=None):
    valHalf42 = 4779
#    start = board.Board(5, 4, [0, 1, 1, 1, 1,
#                               1, 0, 0, 0, 0,
#                               1, 0, 0, 0, 0,
#                               0, 1, 1, 1, 1])    
    
    start = board.Board(5, 4, startPos)
    t = board.Board(5, 4, [0, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           0, 1, 1, 1, 1])
    
    a = [6, 7, 8, 9, 11, 12, 13, 14]
    ways = waysCompB(start, t, outs, None, a)
    
    lengthTab = []
    nblogTab = []

    for i, b in enumerate(board.validWithThreeBorders(4, 2)):
        if i >=0 :
            b.prt()
            l, nb = ways.possibleWays(b, 0)
            nb_log= log10(nb)
    
            print("        %s"%(i))
            print("           fill longest: %s   numbers: %s  log: %s"%(l, nb, nb_log))        
    
            b_l, b_nb = ways.possibleWaysBack(b.getPos(), 0)
            b_nb_log=log10(b_nb)

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
   
    # This computes "corner part" of "refining computation" chapter
    # This takes about two minutes on my computer
    halfBorders42(1)     

    print()
    print()
    
    
    # This computes the "other part" of same chapter
    # This should not be long.
    threeBorders42(0, [0, 1, 1, 1, 1,
                       1, 0, 0, 0, 0,
                       1, 0, 0, 0, 0,
                       0, 1, 1, 1, 1])
                    
	
       
if __name__ == '__main__':
    main()