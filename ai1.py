# encoding=UTF-8
# Usage: python ai1.py

from sys import stdout
import datetime as dt

from board import Board
from search import bfs, iddfs, a_star, gbfs, rbfs

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
           ("Queue size at goal", result["queueSize"])]

  for s in stats:
    print("    * {:<20} {:<20}".format(s[0] + ":", str(s[1])))
  print(" " + "v" if result.get("solved") else "x")

  print("")

def main():
  # The initial board position as given in the assignment.
#  board = Board([[7,2,4],
#                 [5,0,6],
#                 [8,3,1]])
  board = Board([[1,2,0],
                 [8,6,3],
                 [7,5,4]])
#  board = Board([[2,6,3],
#                 [1,0,4],
#                 [8,7,5]])

  print("****************************************************************\n"
        "****************************************************************\n")
#  stdout.write("  a) Uninformed breadth-first search")
#  print_result(run_timed(bfs, board))
#
#  stdout.write("  b) Iterative deepening depth-first search")
#  print_result(run_timed(iddfs, board))

#  stdout.write("  c I) A* search using number of misplaced tiles heuristic")
#  print_result(run_timed(a_star, board, lambda b: b.count_misplaced()))

#  stdout.write("  c II) A* search using sum of manhattan distances heuristic")
#  print_result(run_timed(a_star, board, lambda b: b.manhattan_distances_sum()))

#  stdout.write("  d I) GREEDY search using number of misplaced tiles heuristic")
#  print_result(run_timed(gbfs, board, lambda b: b.count_misplaced()))

#  stdout.write("  d II) GREEDY search using sum of manhattan distances heuristic")
#  print_result(run_timed(gbfs, board, lambda b: b.manhattan_distances_sum()))

  stdout.write("  e) RBFS search using sum of manhattan distances heuristic")
  print_result(run_timed(rbfs, board, lambda b: b.manhattan_distances_sum()))
# Execute solver only when running this module
if __name__ == "__main__":
  main()
