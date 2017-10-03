#!/usr/bin/python
# coding=UTF-8
class Connective:
    # table[0] = not left not right
    # table[1] = not left but right
    # table[2] = left but not right
    # table[3] = left and right
    def __init__(self, short, symbol, name, table):
        self.short = short
        self.symbol = symbol
        self.name = name
        self.table = table
    def eval(self, left, right):
        return self.table[ ( 2 if left else 0 ) + ( 1 if right else 0 ) ]
    def __str__(self):
        return self.short

connectives = [
    Connective('⊥', 'O', 'Contradiction', [ 0, 0, 0, 0 ]),
    Connective('⊤', 'V', 'Tautology', [ 1, 1, 1, 1 ]),
    Connective('I', 'I', 'Proposition 1', [ 0, 0, 1, 1 ]),
    Connective('F', 'F', 'Negation of 1', [ 1, 1, 0, 0 ]),
    Connective('H', 'H', 'Proposition 2', [ 0, 1, 0, 1 ]),
    Connective('G', 'G', 'Negation of 2', [ 1, 0, 1, 0 ]),
    Connective('∧', 'K', 'Conjunction', [ 0, 0, 0, 1 ]),
    Connective('↑', 'D', 'Alternative denial', [ 1, 1, 1, 0 ]),
    Connective('∨', 'A', 'Disjunction', [ 0, 1, 1, 1 ]),
    Connective('↓', 'X', 'Joint denial', [ 1, 0, 0, 0 ]),
    Connective('↛', 'L', 'Material nonimplication', [ 0, 0, 1, 0 ]),
    Connective('→', 'C', 'Material implication', [ 1, 1, 0, 1 ]),
    Connective('⊄', 'M', 'Converse nonimplication', [ 0, 1, 0, 0 ]),
    Connective('←', 'B', 'Converse implication', [ 1, 0, 1, 1 ]),
    Connective('⊕', 'J', 'Exclusive disjunction', [ 0, 1, 1, 0 ]),
    Connective('≡', 'E', 'Biconditional', [ 1, 0, 0, 1 ]),
]

class Formula:
    None

class BooleanFormula(Formula):
    def __init__(self, connective, left, right):
        self.connective = connective
        self.left = left
        self.right = right
    def eval(self, context):
        return self.connective.eval(self.left.eval(context), self.right.eval(context))
    def __str__(self):
        return '(' + str(self.left) + ')' + str(self.connective) + '(' + str(self.right) + ')'

class Variable(Formula):
    def __init__(self, name):
        self.name = name
    def eval(self, context):
        return context[self.name]
    def __str__(self):
        return 'x' + str(self.name)

variables = [
    Variable(0),
    Variable(1),
    Variable(2),
    Variable(3),
    Variable(4),
]

def get_trees(max_variables, max_depth):
    if (max_depth < 0):
        return
    for variable in variables[:max_variables]:
        yield variable
    for left in get_trees(max_variables, max_depth - 1):
        for right in get_trees(max_variables, max_depth - 1):
            for connective in connectives:
                yield BooleanFormula(connective, left, right)

def get_assignments(max_variables):
    if (max_variables == 0):
        yield []
        return
    for a in get_assignments(max_variables - 1):
        yield [ 0 ] + a
        yield [ 1 ] + a

max_variables = 2
trees = get_trees(max_variables, 1)

tables = {}

for tree in trees:
    key = tuple([tree.eval(a) for a in get_assignments(max_variables)])
    if (key in tables):
        tables[key].append(str(tree))
    else:
        tables[key] = [str(tree)]

for t in tables:
    print(str(t) + ': ')
    print('\n'.join(tables[t]))
        

