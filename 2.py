from grammar import Grammar

productions = {
    'S': [['B', 'uno'], ['dos', 'C'], []],
    'A': [['S', 'tres', 'B', 'C'], ['cuatro'], []],  # [] representa epsilon (ε) 'B': [['A', 'cinco', 'C', 'seis'], []],
    'C': [['siete', 'B'], []],
}

# Crear y analizar la gramática
grammar = Grammar(productions)
grammar.eliminate_left_recursion()
grammar.compute_first_sets()
grammar.compute_follow_sets()
grammar.compute_prediction_sets()
grammar.is_ll1()
grammar.generate_asdr()
