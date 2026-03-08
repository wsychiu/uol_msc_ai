#! /usr/bin/env python3

## Set globals:
MODULE    = "P4DS_Formative_A2"
THIS_FILE = "A2_Formative_tests.py"

## ====== TESTS SPECIFICATION ======

## practice_testset.py

TESTS_VERSION = "1st Feb, 2023 (v1)"

SHOW_TEST_CALL   = True
SHOW_TEST_RESULT = True
SHOW_TEST_ANSWER = True

# You can set a timeout time for each test.
TIMEOUT_SECONDS = 30

HOLIDAYS_TEST = [ ["Brighton",            150,  ["beach", "culture"]], 
                  ["Whitby",              100,  ["beach", "culture"]],
                  ["Barcelona",           320,  ["beach", "culture", "hot"]],
                  ["Doncaster",            40,  []],
                  ["Crete",               300,  ["beach", "hot"]],
                  ["London",              250,  ["culture"]],
                  ["Sicily",              300,  ["culture", "hot", "beach"]],
                  ["Barbados",           1250,  ["hot", "beach"]],
                  ["Tanzania",            2500, ["hot", "beach", "wildlife"]],
                  ["Galapagos Islands",  4500,  ["beach", "wildlife"]],      
             ]       


TESTS = {

    "anagrams": [
      ( '__M__.anagrams("listen","silent")',  "eq_bool", True,  1),
      ( '__M__.anagrams("Listen","Silent")',  "eq_bool", True,  1),
      ( '__M__.anagrams("this","that")',      "eq_bool", False, 1),
      ( '__M__.anagrams("this","This")',      "eq_bool", False, 1),
    ],

   "is_palindrome": [
      ( '__M__.is_palindrome( "Abba")',       "eq_bool", True,  1),  
      ( '__M__.is_palindrome( "Python")',     "eq_bool", False, 1),  
      ( '__M__.is_palindrome( "Rotator")',    "eq_bool", True,  1), 
      ( '__M__.is_palindrome( "Was it a cat I saw?")',   "eq_bool", True, 1),
    ],

   "is_english_word": [
      ( '__M__.is_english_word("this")',         "eq_bool", True, 1),
      ( '__M__.is_english_word("Python")',       "eq_bool",    True, 1),
      #( '__M__.is_english_word("Pytastic")',    "eq_bool",  False, 1),
      ( '__M__.is_english_word("HelP")',              "eq_bool", False,  1),
      ( '__M__.is_english_word("Flibbertigibbet")',   "eq_bool", True,  1),
      ( '__M__.is_english_word("Brexit")',            "eq_bool", False, 1),
      ],

  "find_all_anagrams": [
        ( '__M__.find_all_anagrams("cheese")',  "eq_list", [], 1 ),
        ( '__M__.find_all_anagrams("Python")',  "eq_list", ['phyton', 'typhon'], 1),
        ( '__M__.find_all_anagrams("Listen!")', "eq_list", [], 1 ),
        ( '__M__.find_all_anagrams("SeaBird")', "eq_list", ['abiders', 'braised', 'darbies', 'sidebar'], 1),  
      ],
    
   "find_palindromes_of_length": [
       ( '__M__.find_palindromes_of_length(7)',  "eq_list", ['deified', 'halalah', 'reifier',
                                                        'repaper', 'reviver', 'rotator', 'sememes'], 1 ),
       ( '__M__.find_palindromes_of_length(10)',  "eq_list", [], 1 ),
      ],

  "password_strength": [
       #( '__M__.password_strength("python")',  "eq_str",    "ILLEGAL",     1 ),
       ( '__M__.password_strength("boa constrictor")',  "eq_str",   "ILLEGAL",  1 ),
       ( '__M__.password_strength("Secret")',           "eq_str",   "ILLEGAL",  1 ),
       ( '__M__.password_strength("secret99")',         "eq_str",   "WEAK",     1 ),
       ( '__M__.password_strength("Secret999!")',       "eq_str",   "MEDIUM",   1 ),  
       #( '__M__.password_strength("BMX-122333444555Z")',  "eq_str", "MEDIUM",   1 ),
       ( '__M__.password_strength("7Kings8all9Pies!")',  "eq_str",  "STRONG",   1 ),
    ],

  "available_features" : [
          ( "__M__.available_features(100, HOLIDAYS_TEST)", "eq_list", ["beach", "culture"], 1),
          ( "__M__.available_features(5000, HOLIDAYS_TEST)", "eq_list",
                    ["beach", "culture", "hot", "wildlife"], 1),
        ],

   "recommend_holidays": [
     
       ( '__M__.recommend_holidays(200, ["beach"], HOLIDAYS_TEST)', "eq_list",
               ["Brighton", "Whitby"], 1  ),
       ( '__M__.recommend_holidays(500, ["beach"], HOLIDAYS_TEST)', "eq_list",
               ['Barcelona', 'Brighton', 'Crete', 'Sicily', 'Whitby'], 1  ),
       ( '__M__.recommend_holidays(300, ["culture"], HOLIDAYS_TEST)', "eq_list",
               ["Brighton", "London",  "Sicily", "Whitby"], 1  ),
       ( '__M__.recommend_holidays(5000, ["beach", "wildlife"], HOLIDAYS_TEST)', "eq_list",
               ["Galapagos Islands", "Tanzania"], 1  ),
 #      ( '__M__.recommend_holidays(1000,   ["beach", "wildlife"], HOLIDAYS_TEST)', "eq_list",[], 1  ),  
 #      ( '__M__.recommend_holidays(100000, ["programming"], HOLIDAYS_TEST)', "eq_list",[], 1  ),
    ],

}


# You can define 'check_types' that determine how the value returned
# from the function call should be compared to the given answer.
# The simplest and most common is "equal", requiring == to hold between them.
# You can also use "sorted_equal" or define your own.
# CHECK_TYPES is a dictionary where each comarison type (string) is
# associated with a lambda function defining a comparison test function.

CHECK_TYPES =  { "equal"   :      lambda x, y: (type(x)==type(y) and x==y),
                 "eq_bool" :      lambda x, y: (type(x)==bool and type(y)==bool and x==y),
                 "eq_int"  :      lambda x, y: (type(x)==int and type(y)==int and x==y),
                 "eq_str"  :      lambda x, y: (type(x)==str and type(y)==str and x==y),
                 "eq_list" :      lambda x, y: (type(x)==list and type(y)==list and x==y),
                 "eq_df"   :      lambda x, y: (type(x)==pandas.DataFrame and type(y)==pandas.DataFrame and x.equals(y)),
                 "eq_list_members"  : lambda x, y: (type(x)==list and type(y)==list and sorted(x)==sorted(y)),
                 "df_has_index_set" : lambda x, y: (type(x)==pandas.DataFrame and set(x.index)==y),
                 "df_has_index_list" : lambda x, y: (type(x)==pandas.DataFrame and list(x.index)==y),
                 
                 "df_has_depth_set"  : lambda x, y: (type(x)==pandas.DataFrame and set(x['depth'])==y),
                 "df_has_depth_list" : lambda x, y: (type(x)==pandas.DataFrame and list(x['depth'])==y),
               }








## ====== TESTING FUNCTIONS ======


# jupyter_general_test_functions.py

## This tester module is quite complex as it can be used in several different
## modes, but should give equivalent results in all of these.

## Entry Points:
## do_tests(f)   For inline testing of a function from the actual file that
##           is being tested (eg a notebook) to test function f.
##
## do_all_tests() This is used by the external testing functions but can also be
##           used for inline testing so you can see the full test output
##           within the notebook that is being tested.
##
## main()    Called when program run as __main__ (just calls do_all_tests)
##           This exables autograding to be done from the command line.
##
## __gradescope()  This is intended to be called when bb_autograder is
##                 run on Gradescope. 
##              It does a bit little of preliminary setup.
##              Then calls do_all_tests;
##              Then writes results to results/results.json
##              (results.json is read, displayed and stored by Gradescope)


VERSION = 2.5 # 01/02/2023

import os
import sys
import shutil
import importlib
import json
import signal
import subprocess

## For my_timeout_eval
from multiprocessing import Process, Queue
from queue import Empty as QEmptyException

def tests_version():
     return version()

def version():
     return( ("Autograder:", VERSION), ("Tests:", TESTS_VERSION ) )


### The next two classes are for timeout on the test function calls

class TimeoutError(Exception):
    def __init__(self, message):
        super().__init__(message)

### THIS DOES NOT WORK IN WINDOWS (does not support the signal module fully)
## class Timeout:
##    def __init__(self, seconds):
##        self.seconds = seconds
##        self.error_message = "Timeout after " + str(seconds) + " seconds"
##    def handle_timeout(self, signum, frame):
##        raise TimeoutError(self.error_message)
##    def __enter__(self):
##        signal.signal(signal.SIGALRM, self.handle_timeout)
##        signal.alarm(self.seconds)
##    def __exit__(self, type, value, traceback):
##        signal.alarm(0)



## evaluate a code string relative to a given function definition with a timeout
## The substing fname will be replaces by __fvar__ in the string and this
## will be set to the function that is the value of func
## If the optional module argument is given then "__M__" will be set to
## that module ("__M__" may appear in the code string representing some module).

def eval_wrapper( c, fn, f, m):
        #print("In eval wrapper")
        c = c.replace(fn, "__fvar__")
        __fvar__ = f
        if m:
             __M__=m
        try:
            result = eval(c)
        except BaseException as e:
            result = e
        return result

import concurrent.futures         
def eval_with_function_def(timeout, code, fname, func, module=None):

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
           future = executor.submit(eval_wrapper, code, fname, func, module)
           try:
               #print("Getting result ...")
               result = future.result(timeout=10)
               #print("Result:", result)
               return result
           except concurrent.futures.TimeoutError as e:
               #print("Timed out")
               raise TimeoutError("!!! EXCEPTION: Reached time limit: {}s".format(timeout))
           except BaseException as e:
               print( "Exception raised:", type(e))  
               raise e



        
##    queue = Queue()
##    proc  = Process( target=eval_wrapper, args=(queue,code,fname,func,module))
##    proc.start()
##    try: 
##        output = queue.get(True, timeout)
##        proc.terminate()
##        return output
##    except QEmptyException as e:
##        #print("Queue Empty:", e.__repr__())
##        proc.terminate()
##        raise TimeoutError("!!! EXCEPTION: Reached time limit: {}s".format(timeout))
##    except BaseException as e:
##        #print("Exception in eval:", e.__repr__())
##        proc.terminate()
##        raise e


def testset_total_marks():
    total = 0
    for f in TESTS:
        total += sum([ t[3] for t in TESTS[f]] )
    return total

## This is the test function that is designed to be called from
## within a Jupyter notebook.
## If the file "__autograde_test.lock" is found it will just return None
## This is so testing can be blocked if the notebook code is imported
## to carry out testing from outside the notebook.

def do_tests( f ):
    if os.path.exists("__autograde_test.lock"):
      #print("Skipping embedded test (found '__autograde_test.lock' file)" )
      #return (0, 0) # It is expecting a pair
      return None
     
    def dummy(): pass ## this is just used to check whether f is a function
        
    if not type(f) == type(dummy): # hack because 'function' is not actually a type.
                           # It seems to be controversial what counts as a 'function'
        print("!!! ERROR: argument to test should be a function or list of functions")
        return (0,0) ### Maybe change this back ??

    ## Although we can find the name of a function using its __name__ attribute,
    ## it seems that this name as a variable is not bound to the function in the local
    ## scope. Hence I assign the variable __fvar__ to refer to the given function f.
    
    fname = f.__name__
    print( "*Autograder (v{})*".format(VERSION) )
    print( "Testing function:", fname )
    # __fvar__ = f    

    #print(fname)
    #print(TESTS)
    if fname in TESTS:
        testset = TESTS[fname]
    else:
        print("!!! No tests defined for:", fname )
        #return (0,0)
        return None 

    testset_total = 0
    testset_mark  = 0
    for test in testset:
        call, checktype, ans, marks = test
        testset_total += marks
        call = call.replace("__M__.", '')
        if SHOW_TEST_CALL:
             print("Evaluating:", call, "...")
        else:
             print("Evaluating:", "***test hidden***", "..." )
             
        #call = call.replace(fname, "__fvar__" )
        #print("__fvar__", __fvar__)
        
        try:
              result = eval_with_function_def( TIMEOUT_SECONDS, call, fname, f )
              #with Timeout(seconds= TIMEOUT_SECONDS ):
              #    result = eval( call )
        except TimeoutError:
              print("!!! TIMEOUT -- test took too long!" )
              print("!   The test was terminated after {} seconds".
                         format(TIMEOUT_SECONDS) )
              print("!   Marks: 0  (of {})".format(marks))
              continue
        except Exception as e:
              print("!!! An ERROR occurred when running this test." )
              print("    The following exception occurred:" )
              print("   ", e )
              print("!   Marks: 0  (of {})".format(marks))
              continue


        if SHOW_TEST_RESULT:
            print( "Returned:", result.__repr__() )
        else:
            print( "Returned:", "***result hidden***" )

        if SHOW_TEST_ANSWER:
            print( "Expected answer:", ans.__repr__() )
        
        is_correct = CHECK_TYPES[checktype](result,ans)
        markstr = "mark" if marks <= 1 else "marks"
        if is_correct:
              print("CORRECT :)   ", marks, markstr)
              testset_mark += marks
        else:
              print("Inorrect :(   (worth {} {})".format(marks, markstr)  )
    output =  ( "Total mark for '{}' is {} out of {}"
                 .format(fname, testset_mark, testset_total ) )       
    print( "-" * len(output) )
    print( output )
    print( "-" * len(output) )
    return None ## The mark should already be printed.
    # This func no longer used to collect the total marks.
    #return (testset_mark, testset_total)

##--------------------------------------------------------------------------   

## Note do_all_tests no longer takes a list of functions as args.
## They will just be taken from the TESTS dictionary.
## Dummy argument *args will read in but ignore any given arguments.
## This is just for compatibility with the previous version.    

def do_all_tests( *args, output_file = None ):
    if os.path.exists("__autograde_test.lock"):
         #print("Skipping embedded do_all_tests (found __autograde_test.lock file)" )
         return None

    print( "* BB Autograder *" )
    print( "Running tests for module:", MODULE  )
    print()

    if output_file:
        print( "Will write test output to file {} ...".format(output_file ) )
        original_stdout = sys.stdout
        out = open( output_file , "w" )
        sys.stdout = out
        print( "<H1>* BB Autograder *</H1>" )
        print( "Running tests for module: <b>{}</b><tt>".format(MODULE)  )

    try:
        #"this"[27]
        try:
            file_to_test = get_file_to_test( MODULE )
            if not file_to_test :
                print( "!!! ERROR: no input file found. Exiting checker !!!" )
                return False
            import_file = get_import_file( file_to_test )
            
        except Exception as e:
                print( "!!! ERROR: could not find import file (or extract from notebook) !!!" )
                print( "           the following exception occurred:\n", e )
                return False

        if import_file:
             add_extra_defs( import_file )
             total_mark = test_import_file( import_file )
        else:
             total_mark = False
        return total_mark
        
    except Exception as e:
        print( "!!! ERROR: an exception occured during import or testing !!!" )
        print( "           the following exception occurred:\n", e )
        return False
    
    finally:
        if output_file:
            #print( "Restoring stdout" )
            #print("</pre>")
            out.close()
            sys.stdout = original_stdout
            print( "Restored stdout" )

## Add a couple of definitions for functions that are defined in Jupyter
## but not in plain Python. These are:
##   display
##   get_ipython  (called by Python translation of the ! and % special characters)         
def add_extra_defs( import_file ):
    print("Adding extra defs to:", import_file)
    with open(import_file) as f:
          contents = f.read()
    contents = """
def display(x):
    pass

class DummyIpython:
      def system(self,_):
          pass
      def set_next_input(self,_):
          pass
      def run_line_magic(self,_1,_2):
          pass
        
def get_ipython():
    return DummyIpython()
""" + contents
    with open(import_file, "w") as f:
         f.write(contents)

def test_import_file( python_file  ):
  
    print( "Importing module to be tested ...")
      
    #print( "Creating lock file to block tests in the import module ..." )
    with open("__autograde_test.lock", "w") as f:
        f.write("PLEASE DELETE THIS FILE")
        f.write("This is a temporary lock file created by BB Autograder.")
        f.write("It prevents test functions begin called while a test is" )
        f.write("already in progress, which would cause an infinite loop).")
        f.write("It should be automatically deleted after each test run." )
        f.write("If it has somehow not been deleted please delete it," )
        f.write("otherwise calls to test functions will be blocked." )


    original_stdout = sys.stdout
    sys.stdout = open("tmp.out", "w")
    try:
        __M__ = importlib.import_module( python_file[:-3] )

        sys.stdout.close()
        sys.stdout = original_stdout
    except Exception as e:
        sys.stdout.close()
        sys.stdout = original_stdout
        feedback("!!! An ERROR occurred while loading file", python_file )
        feedback("    The following exception occurred:" )
        feedback("   ",  e )
        return False
    finally:
        #print( "Removing test function lock file" )
        if os.path.exists("__autograde_test.lock" ):
           os.remove("__autograde_test.lock" )     
    
    print( "* import successful *" )
    print("Executing tests ...\n\n")

    all_tests_mark = 0

    for fname in TESTS:
      print( "Testing:", fname )

      ### This is a specific hack for this assignment.
      ### Set the global variable in the imported module to the
      ### pre-saved QUAKE_DF (over-riding the one downloaded from web)
      if fname == "powerful_quakes":
               __M__.QUAKE_DF = QUAKE_DF
      
      testset = TESTS[fname]
      testset_mark = 0
      testset_total = 0
      for test in testset:
          call, checktype, ans, marks = test
          testset_total += marks
          call_output = call.replace("__M__.", "")
          if SHOW_TEST_CALL:               
              print("Evaluating:", call_output, "..." )
          else:
              print("Evaluating:", "***test hidden***", "..." )

          try:
              #with Timeout(seconds= TIMEOUT_SECONDS ):
              #    result = eval( call )
              result = eval_with_function_def( TIMEOUT_SECONDS,
                                               call, "__@XX@__", None,
                                               module=__M__)
          except TimeoutError:
              print("!!! TIMEOUT -- test took too long!" )
              print("!   The test was terminated after {} seconds".
                         format(TIMEOUT_SECONDS) )
              print("!   Marks: 0  (of {})".format(marks))
              continue
          except Exception as e:
              print("!!! An ERROR occurred when running this test." )
              print("    The following exception occurred:" )
              print("   ", e )
              print("!   Marks: 0  (of {})".format(marks))
              continue

          if SHOW_TEST_RESULT:
              print( "Returned:", result.__repr__() )
          else:
              print( "Returned:", "***result hidden***" )

          if SHOW_TEST_ANSWER:
              print( "Expected Answer:", ans.__repr__() )
          
          is_correct = CHECK_TYPES[checktype](result,ans)
          markstr = "mark" if marks <= 1 else "marks"
          if is_correct:
              print("CORRECT :)   ", marks, markstr)
              testset_mark += marks
          else:
              print("Inorrect :(   (worth {} {})".format(marks, markstr)  )
      print( "Total for '{}' is {} out of {}\n----\n"
              .format(fname, testset_mark, testset_total ) )       
      all_tests_mark += testset_mark

    print("* Tests completed *\n")
    all_tests_total = testset_total_marks()
    print("TOTAL MARK = {}    (out of {})\n".format(all_tests_mark, all_tests_total))
    final_comment = get_final_comment(all_tests_mark, all_tests_total)
    if GRADESCOPE:
        final_comment = "<h3>" + final_comment + "</h3>"
    print(final_comment + '\n')
    return all_tests_mark

    
def feedback( *args ):
    print( *args )


## This finds the input file corresponding to a given filestem string.
## This will by either a .ipynb or .py file with the given stem.
## If both exists it takes the most recently modified and prints a warning.
## If running in Gradescope it will look in the "submission" subdirectory
## and if the file is found it will copy it to the top directory.
## This should ensure it will work the same on Gradescope as locally.    
def get_file_to_test( stem ):
    in_submission_subdir = False
    if GRADESCOPE and os.path.exists("submission"):
        ## files will be in submission directory if running gradescope
        ## (But not if just simulating Gradescope then submission may
        ## not exist)
        os.chdir("submission")
        in_submission_subdir = True
        
    nbname = stem + ".ipynb"
    pyname = stem + ".py"
    #print("***", nbname, pyname)
    #print("cwd:", os.getcwd() )
    if os.path.exists( nbname ) :
        if os.path.exists( pyname ):
            print("!!! WARNING: Found both", nbname, "and", pyname )
            nb_mtime = os.path.getmtime( nbname )
            py_mtime = os.path.getmtime( pyname )
            latest   = (nbname if nb_mtime > py_mtime else pyname)
            print("    Will check the most recently modified:", latest )
            test_file = latest
        else:
            #print( "Found workfile:", nbname )
            test_file = nbname
    else:
        if os.path.exists( pyname ):
          test_file =  pyname
        else:
          print("!!! ERROR: Did not find input file !!!" )
          print("    Was expecting", nbname, "or", pyname )
          if in_submission_subdir:
              os.chdir('..')
              in_submission_subdir = False
          return None
    if in_submission_subdir:
          # Copy target file to directory above and move to dir above
          shutil.copyfile(test_file, "../" + test_file)
          ## Copy other files to dirctory above
          ## unless they are already there (to avoid overwriting)
          try:
               submission_files = os.listdir()
               above_files = os.listdir('..')
               for file in submission_files:
                   if not file in above_files:
                       if os.path.isfile(file):
                           #print("copying file:", file)
                           shutil.copy(file, '..')
                       elif os.path.isdir(file):
                           #print( "copying directory", file)
                           shutil.copytree(file, '../' + file)
          except:
               print("!!! WARNING: Something went wrong while moving additional submitted files.")
          
          os.chdir('..')
          in_submission_subdir = False
    return test_file
        


## Takes the 'submitted_filename' name (either .py or .ipynb)
## if is of the form stem.py file just returns the filename
## if of form stem.ipynb extracts the python to  a file <stem>_from_ipynb.py      
##        and returns that filename
##        
def get_import_file( submitted_filename ):
    if submitted_filename.endswith(".py"):
        return submitted_filename
    
    if submitted_filename.endswith(".ipynb"):
        print( "Extracting Python from", submitted_filename, "...")
        import nbformat
        from nbconvert import PythonExporter
        def notebook2python(notebookPath, pythonPath):
            with open(notebookPath) as fh:
                nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
            exporter = PythonExporter()
            source, meta = exporter.from_notebook_node(nb)
            with open(pythonPath, 'w') as fh:
                fh.writelines(source)


        #shutil.copyfile( submitted_filename, "__tmp_file.ipynb" )
        import_file = submitted_filename[0:-6] + "_from_nb.py"

        try:
             notebook2python( submitted_filename, import_file )
             
        except Exception as e:
            print( "!!! ERROR: could not extract from", submitted_filename )
            print( "    The following exception occurred:\n", e )
            return( False )
        
        ## print("Successfully extracted", import_file )
        return  import_file

def get_final_comment( marks, total ):
    percent = (marks/total)*100
    if percent == 100:
        return "**** PERFECT SCORE ****"
    if percent >= 90:
        return "*** SPECTACULAR ***"
    if percent >= 70:
        return "*** EXCELLENT ***"
    if percent >= 60:
        return "** VERY GOOD **"
    if percent >= 50:
        return "* GOOD *"
    if percent >= 40:
        return "A reasonable attempt but more study is advised."
    return ("You are advised to revisit this exercise and ask\n"
            "for help regarding any difficulties you are having.")


 
def save_results_json( mark, feedback_file, json_file = MODULE + "_bb_autograder_results.json" ):
    with open(feedback_file) as f:
        feedback_text = f.read()
    feedback_text = feedback_text.replace("\n\n", "<p>")
    feedback_text = feedback_text.replace("\n", "<br>")
    
    results = {}
    results["score"]  = mark
    results["output"] =  feedback_text
    results["visibility"] = "after_due_date" # Optional visibility setting
    results["stdout_visibility"] = "hidden"  # "visible", # Optional stdout visibility setting
    results["extra_data"]        = {} # Optional extra data to be stored
    with open( json_file, 'w' ) as jsf :
         json.dump( results, jsf )
    
GRADESCOPE = False
def __gradescope():
    global GRADESCOPE
    GRADESCOPE = True
    print("Running in Gradescope")

    ## BIT OF A HACK
    ## When running in Gradescope copy THIS_FILE to root dir.__dir__
    ## Need this because the file being tested may try to load the tester.
    ## (It can load it but the functions will be blocked by the lock file.)
    ## Duh! Would have been much easier to just create a dummy version
    ## of the test file, which has dummy versions of all the calls
    ## in the original test file!!!

    if not os.path.exists( THIS_FILE ):
        ## then copy all files from source to root
        shutil.copyfile("source/" + THIS_FILE, "./" + THIS_FILE )
        print("Moving files from source:")
        source_files = os.listdir("source")
        for f in source_files:
             if f == "__pycache__":
                  continue
             if os.path.isfile( "source/" + f):
                 shutil.copyfile( "source/" + f, "./" + f)
             if os.path.isdir( "source/" + f ):
                 shutil.copytree("source/" + f, './' + f)

    ### looks like we need this (maybe put inside a 'try')
    initialise_globals()
    
    feedback_file = MODULE + "_bb_autograder_feedback.txt"
    mark = 0
    try:
        mark = do_all_tests( output_file = feedback_file )
    except Exception as e:
        print( "!!! Autograder ERROR !!!")
        print( "    The exception generated was:\n", e )
    #print( "TOTAL MARK =",  mark )
    #print( "\nWriting json results to results.json")
    if not os.path.exists( feedback_file ):
        print( "!!! NO FEEDBACK FILE FOUND !!!" )
        with output( feedback_file, "w" ) as f:
               f.write( "!!! ERROR: no feedback report found !!!" )

    if mark == False or mark == None: # Gradescope only accepts a numerical result
        mark = 0
        
    print( "Saving json results to 'results/results.json'" )
    if not os.path.exists('results'):
        os.mkdir('results')
    save_results_json( mark, feedback_file, json_file = "results/results.json" )


def main():
    initialise_globals()
    mark = do_all_tests( output_file = None )

DO_MAIN = True
if __name__ == "__main__" and DO_MAIN:
    main()
    



