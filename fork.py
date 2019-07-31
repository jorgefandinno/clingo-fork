#!/usr/bin/env python

"""
This module implements a rewriter for Jorges meta programming project. :)
"""

import sys
import clingo
import clingo.ast as ast

auxiliary_atom_name = "__fork__aux__fork__"




class Transformer(object):
    """
    Basic visitor to traverse and modify an AST.

    Transformers to modify an AST should subclass this class and add visit_TYPE
    methods where TYPE corresponds to an ASTType. This function is called
    whenever a node of the respective type is visited. Its return value will
    replace the node in the parent.

    Function visit should be called on the root of the AST to be visited. It is
    the users responsibility to visit children of nodes that have node-specific
    visitor.
    """

    def __init__(self):
        pass

    def visit_children(self, x, *args, **kwargs):
        """
        Visits and transforms the children of the given node.
        """
        for key in x.child_keys:
            setattr(x, key, self.visit(getattr(x, key), *args, **kwargs))
        return x

    def visit(self, x, *args, **kwargs):
        """
        Visits the given node and returns its transformation.

        If there is a matching visit_TYPE function where TYPE corresponds to
        the ASTType of the given node then this function called and its value
        returned. Otherwise, its children are visited and transformed.

        This function accepts additional positional and keyword arguments,
        which are passed to node-specific visit functions and to the visit
        function called for child nodes.
        """
        if hasattr(x, "type"):
            attr = "visit_" + str(x.type)
            if hasattr(self, attr):
                return getattr(self, attr)(x, *args, **kwargs)
            else:
                return self.visit_children(x, *args, **kwargs)
        elif isinstance(x, list):
            return [self.visit(y, *args, **kwargs) for y in x]
        elif x is None:
            return x
        else:
            raise TypeError("unexpected type")

    def __call__(self, x, *args, **kwargs):
        """
        Alternative way to call visit.
        """
        return self.visit(x, *args, **kwargs)


class AuxTransformer(Transformer):
    """
    Transformer to add aux atoms to rules.
    """



    def __init__(self, aux):
        """
        The given aux atom will be added to visited rules.
        """
        Transformer.__init__(self)
        self.__aux = aux
        self.__visting_rule_head = False
        self.__visting_disjuntion = False
        self.__rule_id = 0
        self.__rule_id_number = None
        self.__auxiliary_atoms = []
        self.__auxiliary_rules = []
        self.__positive_term = clingo.Function('pos', [], True)
        self.__negative_term = clingo.Function('neg', [], True)
        self.__dnegative_term = clingo.Function('dneg', [], True)

    def visit_Rule(self, x, *args, **kwargs):
        """
        Adds aux atoms to the given rule.
        """
        # x.body.append(self.__aux)

        
        self.__rule_id = self.__rule_id + 1
        self.__rule_id_number = clingo.Number(self.__rule_id)
        self.__visting_rule_head = True
        x.head = super(AuxTransformer,self).visit(x.head)
        self.__visting_rule_head = False
        return x
        
    def visit_Disjunction(self, x, *args, **kwargs):
        self.__visting_disjuntion = True
        x.elements = super(AuxTransformer,self).visit(x.elements)
        self.__visting_disjuntion = False
        return x

    def visit_ConditionalLiteral(self, x, *args, **kwargs):
        """
        Make sure that conditions are traversed as non-head literals.
        """
        x.literal = self.visit(x.literal)
        visting_rule_head = self.__visting_rule_head
        try:
            self.__visting_rule_head = False
            x.condition = self.visit(x.condition)
        finally:
            self.__visting_rule_head = visting_rule_head
        return x

    def visit_Literal(self, x, *args, **kwargs):
        if self.__visting_rule_head and self.__visting_disjuntion:
            return self.visit_Literal_in_Head_Disjuntion(x, *args, **kwargs)
        else:
            return x

    def visit_Literal_in_Head_Disjuntion(self, x, *args, **kwargs):
        if x.sign == ast.Sign.DoubleNegation:
            sign = self.__dnegative_term
        elif x.sign == ast.Sign.Negation:
            sign = self.__negative_term
        else:
            sign = self.__positive_term
        rule_id = ast.Symbol(x.location,self.__rule_id_number)
        sign = ast.Symbol(x.location,sign)
        fun = ast.Function(x.location, auxiliary_atom_name, [ rule_id, sign, x.atom.term ], False)
        new_literal = ast.Literal(x.location, ast.Sign.NoSign, ast.SymbolicAtom(fun))
        self.__auxiliary_atoms.append(new_literal)
        rule = ast.Rule(x.location, head=x, body=[new_literal])
        self.__auxiliary_rules.append(rule)
        return new_literal


    def add_auxiliary_rules(self, bld):
        for rule in self.__auxiliary_rules:
            bld.add(rule)




class Application(object):
    """
    Application object as accepted by clingo.clingo_main().

    Rewrites the incoming logic programs, adding auxiliary atoms in the head for disjuntive logic programs
    """

    def __init__(self):
        """
        Initializes the application setting the program name.

        See clingo.clingo_main().
        """
        self.program_name = "rewrite"
        self.version = "1.0.0"

    def print_model(self, model, printer):
        table = {}
        for sym in model.symbols(shown=True):
            if sym.name != auxiliary_atom_name:
                sys.stdout.write(str(sym) + " ")
        sys.stdout.write("\n")
        return True

    def main(self, prg, files):
        """
        Overwrites clingo's main loop taking care of appending the __aux atom.
        """
        pos = {"filename": "<generated>", "line": 1, "column": 1}
        loc = {"begin": pos, "end": pos}
        sym = ast.Symbol(loc, clingo.Function(auxiliary_atom_name, [], True))
        aux = ast.Literal(loc, ast.Sign.NoSign, ast.SymbolicAtom(sym))
        atf = AuxTransformer(aux)
        
        files = [open(f) for f in files]
        if not files:
            files.append(sys.stdin)

        # prg.add("base", [], "#external " + auxiliary_atom_name + ".")

        with prg.builder() as bld:
            for f in files:
                clingo.parse_program(f.read(), lambda stm: bld.add(atf.visit(stm)))

            atf.add_auxiliary_rules(bld)


        prg.ground((("base", ()),))

        prg.solve()

        # with prg.solve(yield_=True) as prg_handle:
        #     for prg_model in prg_handle:
        #         self.print_model(prg_model, None)
        #         sys.stdout.write("\n")


sys.exit(int(clingo.clingo_main(Application(), sys.argv[1:])))
