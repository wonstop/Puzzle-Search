Assignment 1.1: Search algorithms
=================
Reffer to
Dr. K. P. Chan's course **CSIS0270 Artificial intelligence**  (University of Hong Kong, 2014).

My solution is a sliding tile puzzle solver written in Python 2.7. It solves the 8-puzzle position given in the assignment paper using breadth-first search (BFS), iterative deepening depth first search (IDDFS) and A* search. Some performance statistics are also provided to aid in comparing the algorithms.

Example output
==============

```
>>>>>>>>
```

Running
=======

1. Run unit tests with `python boardtest.py`
2. Run the puzzle solver with `python ai1.py`

Modules
=======

File           | Description
--------------:|:-------------------------------------------------------------------------------
   `search.py` | My algorithm implementations.
      `ai1.py` | Main module: runs timed searches against the initial board state.
    `board.py` | Board class: a sliding puzzle board with immutable state.
    `rules.py` | Static rules of the sliding puzzle game.
`boardtest.py` | Unit tests for board logic.
