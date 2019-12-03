# encoding=UTF-8
import itertools
from collections import deque
from Queue import PriorityQueue
from sys import stdout, maxint

def result(iterations, queue, solvedBoard = None):
  return {
    "solved":     solvedBoard != None,
    "iterations": iterations,
    "queueSize":  len(queue),
    "pathCost":   solvedBoard.moves if solvedBoard else None ,
    "StepSeq":    solvedBoard.get_steps() if solvedBoard else None
  }

# Uninformed breadth-first search. Simple to implement yet uses a lot of memory.
# Fringe is a first-in-first-out queue and the data structure used is python's
# double ended queue (dequeue), a doubly-linked list with O(1) pop operation. We pop
# from left and populate from right.
def ucs(root_node, animate_progress):
  iterations = 0 # Only for stats.
  visited = set()
  queue = deque([root_node])

  while len(queue) > 0:
    iterations = iterations + 1
    animate_progress(iterations)

    node = queue.popleft() # Get shallowest node.
    visited.add(node.tilehash()) # Mark current node as visited.

    if node.is_goal():
      return result(iterations, queue, node)
    # Populate queue from right with unvisited legal moves from shallowest node.
    queue.extend(
      filter(
        lambda legalMove: legalMove.tilehash() not in visited,
        node.children()))

  # Loop did not find result: search space exhaustion, no goal found.
  return result(iterations, queue)

# 1b) Iterative deepening depth-first search. Should find the optimal solution like 
# BFS but use less memory. On the other hand the time cost is larger because nodes 
# above the goal depth are recomputed over and over again. No depth limit is set so 
# this implementation will not terminate if the search space is infinite. Fringe is a 
# LIFO queue. Here we use an ordinary python list with O(1) append and pop (both are
# done from the right).
def iddfs(root_node, animate_progress):
  iterations = 0 # Only for stats.

  # Depth goes from 0 to infinity. We start at 0 to ensure optimality: we must check
  # that the initial state is not a goal state before generating its children.
  for depth in itertools.count(): 
    queue = [root_node]
    
    # Visited is a dictionary with node hash as key and node depth as value. We need
    # to track depth as in DFS we may encounter visited nodes later at shallower depth.
    visited = {} 

    while len(queue) > 0:
      iterations = iterations + 1
      animate_progress(iterations)
      
      node = queue.pop() # Get deepest node.
      visited[node.tilehash()] = node.moves # Mark current node as visited.

      if node.is_goal():
        return result(iterations, queue, node)
     
      if node.moves < depth:
        queue.extend(
          filter(
            lambda child:
              child.tilehash() not in visited or
              visited[child.tilehash()] > child.moves,
            node.children()))

  # Loop did not return result -> search space exhaustion, no goal found.
  return result(iterations, queue) 

# A* search. Should find the result much faster than BFS and IDDFS.
# Fringe is a priority queue ordered by a cost estimate function.
# This is a general implementation that is parameterized to receive any heuristic.
# Nodes sharing same priority are in no special order -> traversal order
# is not fully deterministic.
def a_star(root_node, animate_progress, heuristic):
  iterations = 0 # Only for stats.
  visited = set()
  queue = PriorityQueue()
  queue.put((0, root_node))

  # Cost estimate = accumulated cost so far + heuristic estimate of future cost.
  def estimate_cost(node): return node.moves + heuristic(node)
  def queue_entry(node): return (estimate_cost(node), node)

  def unvisited_children(node):
    return filter(
      lambda child: child.tilehash() not in visited,
      node.children())

  while not queue.empty():
    iterations = iterations + 1
    animate_progress(iterations)

    node = queue.get()[1] # get node with highest priority
    visited.add(node.tilehash()) # Mark current node as visited

    if node.is_goal():
      return result(iterations, queue.queue, node) # Goal test

    for entry in map(queue_entry, unvisited_children(node)):
      queue.put(entry)

  # Loop did not return result -> search space exhaustion, no goal found.
  return result(iterations, queue)

# GREEDYYYYYYYYYY BEST FIRST 就是A*拿掉g(n)
def gbfs(root_node, animate_progress, heuristic):
  iterations = 0 # Only for stats.
  visited = set()
  queue = PriorityQueue()
  queue.put((0, root_node))

  # Cost estimate = heuristic estimate of future cost.
  def estimate_cost(node): return heuristic(node)
  def queue_entry(node): return (estimate_cost(node), node)

  def unvisited_children(node):
    return filter(
      lambda child: child.tilehash() not in visited,
      node.children())

  while not queue.empty():
    iterations = iterations + 1
    animate_progress(iterations)

    node = queue.get()[1] # get node with highest priority
    visited.add(node.tilehash()) # Mark current node as visited

    if node.is_goal():
      return result(iterations, queue.queue, node) # Goal test

    for entry in map(queue_entry, unvisited_children(node)):
      queue.put(entry)

  # Loop did not return result -> search space exhaustion, no goal found.
  return result(iterations, queue)


def rbfs(root_node, animate_progress, heuristic):
   iterations = 0 # Only for stats.
   rbfs_v = rbfs_r(root_node, heuristic, maxint, iterations, animate_progress)
   if rbfs_v[0]:
       return rbfs_v[2]


def rbfs_r(node, heuristic, f_limit, iterations, animate_progress):
  queue = PriorityQueue()

  # Cost estimate = accumulated cost so far + heuristic estimate of future cost.
  def estimate_cost(node): return max(node.moves + heuristic(node), node_f)
  def queue_entry(node): return (estimate_cost(node), node)

  node_f = node.moves + heuristic(node) # f embedded in board?
  if node.is_goal():
#    print("\n    * {:<20} {:<20}".format("Steps:", node.get_steps()))
    return (True, node_f, result(iterations, queue.queue, node)) # Goal test
    
  for entry in map(queue_entry, node.children()):
    queue.put(entry)
    
  if queue.qsize == 0:
    return (False, maxint, result(iterations, queue.queue))
  
  while True:
    iterations += 1
    animate_progress(iterations)
    node = queue.get()[1] # get node with highest priority
    best_f = node.moves + heuristic(node)
    if best_f > f_limit:
        return (False, maxint, result(iterations, queue.queue))
    node_alternative = queue.get()[1] if queue.qsize() != 0 else f_limit # get node with second-lowest priority
    alternative_f = estimate_cost(node_alternative)
    queue.put((alternative_f, node_alternative))
    result_ok, best_f, result_rbfs = rbfs_r(node, heuristic, min(f_limit, alternative_f), iterations, animate_progress)
    iterations = result_rbfs["iterations"]
    queue.put((best_f, node))
    if result_ok:
        result_rbfs["queueSize"] += queue.qsize()
        return (True, best_f, result_rbfs)
