# -*- coding: utf-8 -*-

"""
Created on Thu Sep 24 19:59:14 2015

@author: Matthieu Walraet
"""

import itertools

def getNeighboursTemplate(width, height):
    
    if (width, height) not in Board._neighboursTemplates:
        # print("New neighbours template for %s, %s"%(width, height)  )
        newTemplate = []
        for j in range(height):
            for i in range(width):
                p = j * width + i
                
                neighbours = []
                
                if i > 0: 
                    neighbours.append(p-1)
                if i < width-1:
                    neighbours.append(p+1)
                if j > 0:
                    neighbours.append(p-width)
                if j < height-1:
                    neighbours.append(p+width)
                    
                newTemplate.append(tuple(neighbours))
        Board._neighboursTemplates[(width, height)] = newTemplate
    
    return Board._neighboursTemplates[(width, height)]


class Board(object):
    """
    A go position
    """
    
    _neighboursTemplates = dict()
    _colorChar = ['.', '#', 'O']       
    
    def __init__(self, width, height, content=None):
        
        self._width = width
        self._height = height
        self._size = width * height
        self._neighboursTemplate = getNeighboursTemplate(width, height)

        if content:
            self._board = list(content)
        else:
            self._board = [0 for i in range(self._size)]

    
    def neighbours(self, p):
        return self._neighboursTemplate[p]
        
    def copy(self):
        return Board(self._width, self._height, self._board)

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getPos(self):
        return tuple(self._board)
        
    def getStone(self, pos):
        return self._board[pos]
        
    def setStone(self, pos, col):
        self._board[pos] = col
    
    def getStonesOfColor(self, col):
        return [p for p in range(self._size) if self._board[p]== col ]
    
    def takenGroups(self, seed=None):  
        """ 
        return list of tuple (color, set of stones) 
        with group of stones with no liberty left
        """          
        visited = set()
        grps = []
        
        if not seed:
            seed = range(self._size)

        for stone in seed:
            if stone not in visited:
                groupColor = self._board[stone]
                
                if groupColor:
                    group = set()
                    toAdd = set([stone])
                    taken = True 
                    
                    while toAdd:
                        a = toAdd.pop()
                        group.add(a)
                        visited.add(a)
                        
                        for n in self.neighbours(a):
                            nc = self._board[n]
                            
                            if nc:
                                if nc==groupColor and n not in visited:
                                    toAdd.add(n)
                            else:
                                taken = False
                    
                    if taken:
                        grps.append( (groupColor,group))
                        #print("taken:       %s %s"%(groupColor, group))
                    #else:
                        #print("Still alive: %s %s"%(groupColor, group))
        return grps

    def takenStonesColor(self, color, seed=None):
        """ 
        return stones of given color that belongs to group
        with no liberties
        """
        
        taken = set()
      
        for c, g in self.takenGroups(seed):
            if c == color:
                taken = taken.union(g)

        return taken

    def removeStones(self, stones):
        for s in stones:
            self._board[s] = 0

    def insertRow(self, row=None, pos=0):
        if not row:
            row = [0 for _ in range(self._width)]
        
        aPos = pos*self._width
        self._board[aPos:aPos] = row

        self._height += 1
        self._size = self._width * self._height
        self._neighboursTemplate = getNeighboursTemplate(self._width, self._height)

    def insertColumn(self, column=None, pos=0):
        if not column:
            column = [0 for _ in range(self._height)]

        self._width += 1
        
        for i, ci in enumerate(column):
            iwpp = i * self._width + pos
            self._board[iwpp:iwpp] = [ci]

        self._size = self._width * self._height
        self._neighboursTemplate = getNeighboursTemplate(self._width, self._height)

    def toStrings(self):
        for i in range(0, self._size, self._width):  
           yield ' '.join(Board._colorChar[c] for c in self._board[i : i + self._width])

            
    def prt(self):
        print()
        for s in self.toStrings():
            print(s)


    def play1safe(self, col, pos):
        """
        Play a move, it's illegal to take 1     
        """
    
        if self.getStone(pos):
            # Already a stone here
            return None
    
        # opponent color
        oc = 3 - col
            
        bNext = self.copy()
        bNext.setStone(pos, col)    
        
        taken = bNext.takenStonesColor(oc, bNext.neighbours(pos))
        
        if taken:
            if col == 2:
                # Illegal to take 1, to avoid repetition
                return None
    
            bNext.removeStones(taken)
            
        if bNext.takenGroups([pos]):
             # can't play there, no liberty lef
             return None
      
        return bNext

def validPos(w, h):
    """
    count number of valid possible positions
    
    """

    
    for b in itertools.product([0, 1, 2], repeat=w*h):
        # print(b)
        gb = Board(w, h, b)
        
        if not gb.takenGroups():
            yield gb
            


def validWithHalfBorders(w, h):
    for b in itertools.product([0, 1, 2], repeat=w*h):
        # print(b)
        gb = Board(w, h, b)
        
        gb.insertRow([1] * w )
        gb.insertColumn([0] + [1] *h )
        
        if not gb.takenGroups():
            yield gb
            

def validWithFullBorders(w, h):
    for b in itertools.product([0, 1, 2], repeat=w*h):
        # print(b)
        gb = Board(w, h, b)
        
        gb.insertRow([1] * w )
        gb.insertRow([1] * w, h+1)
        gb.insertColumn([0] + [1] *h + [0])
        gb.insertColumn([0] + [1] *h + [0], w+1)
        
        if not gb.takenGroups():
            yield gb
          


def validWithThreeBorders(w, h):
    """No border on right"""

    
    for b in itertools.product([0, 1, 2], repeat=w*h):
        # print(b)
        gb = Board(w, h, b)
        
        gb.insertRow([1] * w )
        gb.insertRow([1] * w, h+1)
        gb.insertColumn([0] + [1] *h + [0])
        
        if not gb.takenGroups():
            yield gb
            



def count(it):
    return sum(1 for _ in it)

def countPositions(w, h):
    print()
    i = count(validPos(w, h))
    print("%s x %s                      %s"%(w, h, i))

    j = count(validWithHalfBorders(w, h))
    print("%s x %s with half borders    %s"%(w, h, j))
        
    k = count(validWithFullBorders(w, h))
    print("%s x %s with full borders    %s"%(w, h, k))

    l =  count(validWithThreeBorders(w, h))
    print("%s x %s with three borders   %s"%(w, h, l))


def main():
    
    countPositions(2, 2)  
    countPositions(3, 3)
    countPositions(4, 2)
    
    

    
        
        
if __name__ == '__main__':
    main()
    
    