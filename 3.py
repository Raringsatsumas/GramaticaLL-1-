from grammar import Grammar

productions = {
    'S': [['A', 'B', 'C'], ['S', 'uno']],
    'A': [['dos', 'B', 'C'], []],  # [] representa epsilon (ε)
    'B': [['C', 'tres'], []],
    'C': [['cuatro', 'B'], []],
}

# Crear y analizar la gramática
grammar = Grammar(productions)
grammar.eliminate_left_recursion()
grammar.compute_first_sets()
grammar.compute_follow_sets()
grammar.compute_prediction_sets()
grammar.is_ll1()
grammar.generate_asdr()
