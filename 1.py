from grammar import Grammar

productions = {
    'S': [['A', 'B', 'C'], ['D', 'E']],
    'A': [['dos', 'B', 'tres'], []],  # [] representa epsilon (ε)
    'B': [['B', 'cuatro', 'C', 'cinco'], []],
    'C': [['seis', 'A', 'B'], []],
    'D': [['uno', 'A', 'E'], ['B']],
    'E': [['tres']]
}

# Crear y analizar la gramática
grammar = Grammar(productions)
grammar.eliminate_left_recursion()
grammar.compute_first_sets()
grammar.compute_follow_sets()
grammar.compute_prediction_sets()
grammar.is_ll1()
grammar.generate_asdr()
