
def tests_version():
     return( "1st Feb, 2023")

TESTS = {
  "number_of_vowels": [
      ("How many vowels?",   4, 1),
      ("Sooo many vowels!",  6, 1),
      ("XXXX",               0, 1)
      ],
   
   "number_of_distinct_vowels": [
     ("Hello World",        2, 1),
      ("Sooo many vowels!", 3, 1),
      ("XXXX",              0, 1),
      ("Eutopia",           5, 1)
    ],

    "password_strength": [
       ("python",            "WEAK",     1 ),
       ("Secret9",           "WEAK",     1 ),
       ("secret99",          "MEDIUM",   1 ),
       ("Secret999!",        "MEDIUM",   1 ),  
       ("BMX-122333444555Z", "MEDIUM",   1 ),
       ("7Kings8all9Pies",   "STRONG",   1 ),
    ],

    "megabyte_bars_cost": [
       ( 3, 3.75,   1 ),
       (12, 10,     1 ),
       (15, 13.75,  1 ),
       (26, 20.25,  1 ),
       (100, 76.5,  1 )
    ],

}


def do_tests( function ):
    max_marks = 0
    marks = 0
    function_name = function.__name__
    print("\nRunning tests for function:", function_name )
    tests = TESTS[function_name]
    for test in tests:
        (test_input, test_answer, test_marks) = test
        max_marks += test_marks

        print( "  * {}( {} )  ...".format(function_name, test_input.__repr__() ))

        if not type(test_input) == tuple:
           test_input = (test_input,)

        result = function(*test_input)

        print("    returned:", result.__repr__() )

        # Handle case where answer may be a list in any order
        # by sorting both the result and the answer.
        if ( type(test_answer) == tuple and test_answer[0] == "any_order"
             and type(result) == list 
           ):
           result.sort()
           test_answer = test_answer[1]
           test_answer.sort() 

        if result == test_answer:
           print("    Correct :)   ({})".format(test_marks) )
           marks += test_marks
        else:
           print("    Incorrect :(   (should be {})".format(test_answer.__repr__()))
    print( "Total marks for this function: {} (of {})".format(marks, max_marks) )          
    return (marks, max_marks)
        







