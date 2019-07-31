%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% This example illustrates how forks are behave different from choice rules.
%%%  
%%%
%%% Undertanding "," as a fork, it has two answer sets: {a,c,d}  and
%%% {a,b,c,d}. This can be checked by running
%%%
%%% python rewrite.py example1.lp --output=reify | clingo 0 -Wno-atom-undefined - metaF.lp
%%%
%%% On the other hand, if we remplace rule
%%%
%%% a , b :- c.
%%%
%%% by
%%%
%%% 1{a ; b} :- c.
%%%
%%% we obtain 3 answer sets: {a,c,d}, {b,c,d} and {a,b,c,d}
%%%
%%% To check this run
%%%
%%% clingo 0 example2b.lp
%%%
%%% If we replace the above rule by
%%%
%%% 1{a ; b}1 :- c.
%%%
%%% we actually obtain the same answer sets as with the fork connective. Execute:
%%%
%%% clingo 0 example2c.lp
%%%
%%% However, if we add the rule
%%%
%%% a :- d.
%%%
%%% to this program and example2c.lp we obtain different answer sets. In particular, we
%%% obtain {a,c,d} and {a,b,c,d} for the fork case (see example1.lp) and {a,c,d} for the 
%%% choice case. For this last example, execute
%%%
%%% clingo 0 example2d.lp
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

a , b :- c.
c.
d.
