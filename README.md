# clingo-fork

Clingo-fork replaces the semantics of disjuntive logic programs so that disjuntion in the head is undertood as forks instead of epistemic disjuntion (see [**Forgetting auxiliary atoms in forks**](https://doi.org/10.1016/j.artint.2019.07.005) for more details).

Requirements:
   - [**python 2.7**](https://www.python.org/download/releases/2.7/)
   - [**clingo 5.3.0**](https://github.com/potassco/clingo)

Usuage:
```bash
python2.7 fork.py examples/example1.lp
```