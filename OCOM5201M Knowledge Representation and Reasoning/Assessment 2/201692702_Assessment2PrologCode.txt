% Assessment 2 Given Prolog Code.

whitebox :- format('~s', ["\u25A1"]).
space    :- format('~s', [" "]).
blackBox :- format('~s', ["\u25A0"]).

numb(0). numb(1). numb(2). numb(3). numb(4). numb(5).
numb(6). numb(7). numb(8). numb(9). numb(10). 

state([R,C]) :- numb(R),  numb(C).

showWhere(Formula) :- showRows(Formula, 0).

showRows(Formula, N) :- numb(N), !, showCols(Formula, N, 0),
                        NPlus is N + 1, showRows(Formula, NPlus).
showRows(_, _).

showCols(Formula, R, C) :- numb(C), holds(Formula, [R,C]), !, 
                           blackBox, space, CPlus is C + 1,
                           showCols(Formula, R, CPlus).

showCols(Formula, R, C) :- numb(C), !, 
                           whitebox, space, CPlus is C + 1, 
                           showCols(Formula, R, CPlus).
showCols(_, _, _) :- nl.

holds(Formula, State) :- holdsList(Formula, StateList),
                         member(State,StateList).

holds( or(P,_), S):- holds(P,S).
holds( or(_,Q), S):- holds(Q,S).

holds( and(P,Q), S) :- holds(P,S), holds(Q,S).

holds( not(P), S) :- form(P), chkstate(S), !, not(holds(P,S)).

holds( implies(P, Q), S) :- holds(or(not(P),Q),S).

holds( dia(R, F), S) :- rel(R, S, T), holds(F,T).

holds( box(R,F), S) :- foreach(rel(R,S,T),holds(F,T)).

form(bread).
form(filling).
form(or(X,Y))  :- form(X), form(Y).
form(and(X,Y)) :- form(X), form(Y).
form(implies(X,Y)) :- form(X), form(Y).
form(not(X))   :- form(X).
form(dia(_,X)) :- form(X).
form(box(_,X)) :- form(X).

chkstate(X) :- state(X), !.
chkstate(X) :- write('unknown state : '),write(X), nl, fail. 

rel(above, [X,Y], [Z,Y]) :- numb(X), numb(Y), numb(Z), X < Z.
rel(oneabove, [X,Y], [Z,Y]) :- numb(X), numb(Y), numb(Z), Z is X + 1.

rel(below, [X,Y], [Z,Y]) :- rel(above, [Z,Y], [X,Y]).
rel(onebelow, [X,Y], [Z,Y]) :- rel(oneabove, [Z,Y], [X,Y]).

rel(isLeftOf, [X,Y], [X,Z]) :- numb(X), numb(Y), numb(Z), Y < Z.

rel(isRightOf, [X,Y], [X,Z])    :- rel(isLeftOf, [X,Z], [X,Y]).

holdsList(bread, [ [3,3], [3,4], [3,5], [3,6], [3,7] ]). 
holdsList(filling, [ [4,3], [4,4], [4,5], [4,6], [4,7] ]). 
holdsList(bread, [ [5,3], [5,4], [5,5], [5,6], [5,7] ]).


%Question 5.1 Supporting Relations
check_same_row(Relation) :- findall(S, holds(Relation,S), ListOfThings), same_rows(ListOfThings).
same_rows([[Row,_]|Remainder]) :- same_rows(Remainder, Row).
same_rows([],_).
same_rows([[Row,_]|Remainder], FirstOne) :- Row=FirstOne, same_rows(Remainder, FirstOne).

%Question 5.2 Supporting Relations
or(P,_) :- P.
or(_,Q) :- Q.
check_left :- holds(bread,B),holds(dia(isLeftOf, filling), B), !.
check_right :- holds(bread,B),holds(dia(isRightOf, filling), B), !.

%Question 5.3 Supporting Relations
check_above :- holds(bread,B), holds(dia(above, filling), B).
check_below :- holds(bread, B), holds(dia(below, filling), B).

%TASK 1:
%Any place that has bread cannot also have filling and no place that has filling can also have bread.

%Answers are allowed to be more than one line as long is the whole file submitted has no syntax errors.
%To answer task 1: remove the % from start of next line and insert your formula in the space
answer1(foreach(holds(bread,S), not(holds(filling, S)))).

%TASK 2:
%Filling must have bread immediately above it and below it.

%Answers are allowed to be more than one line as long is the whole file submitted has no syntax errors.
%To answer task 2: remove the % from start of next line and insert your formula in the space
answer2(foreach(holds(filling,S), holds(box(onebelow, bread), S)), 
        foreach(holds(filling,T), holds(box(oneabove, bread), T))).

%TASK 3:
%Going more than one row below filling there should be no bread.

%Answers are allowed to be more than one line as long is the whole file submitted has no syntax errors.
%To answer task 3: remove the % from start of next line and insert your formula in the space
answer3(foreach((holds(bread,S),  holds(dia(below,filling),S)), holds(dia(onebelow,filling),S))).

%TASK 4:
%If somewhere has filling, then everywhere which is in any row anywhere above cannot have filling.

%Answers are allowed to be more than one line as long is the whole file submitted has no syntax errors.
%To answer task 4: remove the % from start of next line and insert your formula in the space
answer4(foreach(holds(dia(above,filling), S), holds(not(filling), S))).

%TASK 5
%Give three different examples of ways in which the above constraints could all be satisfied but 
%it can be argued that it is not really a sandwich. Hint: think about size of sandwiches may help.

%Your answer will be English sentences describing a problematic sandwich. 
%For example: "A sandwich that is knotted" rather than listing places which are bread and filling.
%That was just a silly example. It is unclear what a knotted sandwich would be and it is nothing like correct.

%In task 5 only (not in tasks 1 to 4) you may choose to define one or more extra relations. 
%There are no extra marks for doing this - just a possibility if you find an answer that needs it.
%Just add your relations after the ones given above.
%Answers are allowed to be more than one line as long is the whole file submitted has no syntax errors.

%ANSWER 5.1
%write your answer here as a comment, as many lines as you need but start each with the % for comments
% "A wavy, stepped, or non-flat sandwich", i.e. a sandwich with filling in different rows

%Give a formula below that prevents your example when it holds in EVERY state.
%That is: If your formula holds everywhere than this kind of problematic sandwich cannot happen.
%Remove the % and insert your formula in the space in the next line.
answer51(check_same_row(filling)).

%ANSWER 5.2
%write your answer here as a comment, as many lines as you need but start each with the % for comments
% "A sandwich with filling surrounded horizontally with bread - a pie"

%Give a formula below that prevents your example when it holds in EVERY state.
%That is: If your formula holds everywhere than this kind of problematic sandwich cannot happen.
%Remove the % and insert your formula in the space in the next line.
answer52(not(or(check_left, check_right))).

%ANSWER 5.3
%write your answer here as a comment, as many lines as you need but start each with the % for comments
% "A sandwich with missing filling or no filling at all"

%Give a formula below that prevents your example when it holds in EVERY state.
%That is: If your formula holds everywhere than this kind of problematic sandwich cannot happen.
%Remove the % and insert your formula in the space in the next line.
answer53(foreach(holds(bread,B), (or(holds(dia(above, filling), B), holds(dia(below, filling), B)), !))).