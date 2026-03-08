## search_tester.py
## by Brandon Bennett --- 27/10/2009

## This is the top level file for running various search
## algorithms.

print( "Loading search_tester.py" )

import sys
from tree          import *
from queue_search  import *
from robot_servant import *
from knights_tour  import *
from eight_puzzle  import *

print( "*All imports loaded*\n" )

# Use this if you want to make Python wait between search tests.
def wait():
      input('<Press enter to continue>')


def run_tests_on_knight_puzzle():
      print( "*Running Knight's Tour search tests*\n" )
      ## Extend this definition to carry out tests as specified in
      ## question 1.a.i.
      search(get_knights_tour_problem(4,4), 'depth_first',   100000, [] )
      search(get_knights_tour_problem(5,5), 'depth_first',   500000, [] )

## Comment out next line if you don't want to run the knight's move puzzle tests
#run_tests_on_knight_puzzle()


def run_tests_on_robot_search_problem():
      ### This is for illustration.
      ### But you should use a similar proceedure to carry out the
      ### search tests specified in Part 2 of the coursework.
      MAX_NODES = 5000
      search( robot_search_problem_1, 'breadth_first', MAX_NODES, [])

      wait()
      search( robot_search_problem_1, 'breadth_first', MAX_NODES, ['loop_check'])
      wait()
      search( robot_search_problem_1, 'depth_first', MAX_NODES, [])
      wait()
      search( robot_search_problem_1, 'depth_first', MAX_NODES, ['loop_check'])
      wait()
      search( robot_search_problem_1, 'randomised_depth_first', MAX_NODES, [])
      wait()
      search( robot_search_problem_1, 'randomised_depth_first', MAX_NODES, ['loop_check'])

## Uncomment next line to run some tests on the "Robot Servant" problem
## run_tests_on_robot_search_problem()

def run_tests_on_eight_puzzle():
    ## You need to define a suitable set of tests to evaluate the
    ## effectiveness of various search strategies for solveing the 8-puzzle.
    ## See the coursework specification for guidance on what tests to do.
    ## Here is an example search test to get you started:
    search( eight_puzzle, 'depth_first', 5000, ['loop_check'] )

## Uncomment next line to run tests on the eight-puzzle problem
## run_tests_on_eight_puzzle()



