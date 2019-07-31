%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% This example illustrates how forks are behave different from standard ASP epistemic
%%% dijuntion. 
%%%
%%% Undertood as a regular ASP program, it has a unique answer set {a,c,d}. This can be
%%% observed by running 
%%% 
%%%    clingo 0 example1.lp
%%%
%%% On the other hand, undertanding ","" as a fork, it has two answer sets: {a,c,d}  and
%%% {a,b,c,d}. This can be checked by running
%%%
%%% python rewrite.py example1.lp --output=reify | clingo 0 -Wno-atom-undefined - metaF.lp
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

a(X) : b(X).
a(1).
b(1).
b(2).
