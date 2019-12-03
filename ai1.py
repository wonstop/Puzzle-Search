# encoding=UTF-8
# Usage: python ai1.py

from sys import stdout
import datetime as dt

from board import Board
from search import ucs, iddfs, a_star, gbfs, rbfs

def run_timed(algorithm, board, heuristic = None):
  # Write a dot to stdout every twenty thousand iterations.
  def anim(iterations):
    if (iterations % 20000 == 0):
      stdout.write("."); stdout.flush()

  start = dt.datetime.now()
  result = algorithm(board, anim, heuristic) if heuristic else algorithm(board, anim)
  end = dt.datetime.now()

  # Add approximate time elapsed as datetime.timedelta to result object.
  result["executionTime"] = end - start 
  return result

def print_result(result):
  stats = [("Execution time",     result["executionTime"]),
           ("Path cost to goal",  "{} moves".format(result["pathCost"])),
           ("Iterations",         result["iterations"]),
           ("Queue size at goal", result["queueSize"]),
           ("StepSequence", result["StepSeq"])
          ]

  for s in stats:
    print("    * {:<20} {:<20}".format(s[0] + ":", str(s[1])))
  print(" " + "got result!" if result.get("solved") else "no result")

  print("")

def main():
  # The initial board position as given in the assignment.
#  board = Board([[7,2,4],
#                 [5,0,6],
#                 [8,3,1]])
#  board = Board([[8,1,2],
#                 [7,6,3],
#                 [5,4,0]])
  board = Board([[1, 2, 13, 4], 
                 [12, 0, 3, 5], 
                 [11, 15, 14, 6], 
                 [10, 9, 8, 7]])

  print("****************************************************************\n"
        "****************************************************************\n")
  stdout.write("  a) Uninformed cost search")
  print_result(run_timed(ucs, board))

  stdout.write("  b) Iterative deepening depth-first search")
  print_result(run_timed(iddfs, board))

  stdout.write("  c) A* search using sum of manhattan distances heuristic")
  print_result(run_timed(a_star, board, lambda b: b.manhattan_distances_sum()))

  stdout.write("  d) GREEDY search using sum of manhattan distances heuristic")
  print_result(run_timed(gbfs, board, lambda b: b.manhattan_distances_sum()))

  stdout.write("  e) RBFS search using sum of manhattan distances heuristic")
  print_result(run_timed(rbfs, board, lambda b: b.manhattan_distances_sum()))
# Execute solver only when running this module
if __name__ == "__main__":
  main()
