A googolplex of go games
------------------------

Article is here: http://matthieuw.github.io/go-games-number/GoGamesNumber.pdf

SGF files
 - main9x9a.sgf
    - Describes the _main scheme_
 - sub.sgf
    - Describes the _sub-scheme_ and _sub-sub-scheme_

Python files
 - board.py           
   - Can compute (very roughly) a number of valid position
 - waycomp.py         
   - Can compute numbers of possible games (and longuest one) from two positions
 - waycompb.py
   - Optimization discussed in the article, in case you have many time the same initial position and different target positions
