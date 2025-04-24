class Grammar:
    def __init__(self, productions):
        # Inicializamos la gramática con las reglas dadas
        self.productions = productions
        self.non_terminals = list(self.productions.keys())
        self.terminals = set()

        # Identificar los terminales
        for nt in self.non_terminals:
            for prod in self.productions[nt]:
                for symbol in prod:
                    if symbol and symbol not in self.non_terminals:
                        self.terminals.add(symbol)

        self.first_sets = {}
        self.follow_sets = {}
        self.prediction_sets = {}

    def eliminate_left_recursion(self):
        print("=== Eliminación de Recursividad por la Izquierda ===")
        print("Gramática original:")
        self.print_grammar()

        # Hacemos una copia de los no terminales originales para no modificar la lista durante la iteración
        original_non_terminals = self.non_terminals.copy()
        new_productions = {}

        # Para cada no-terminal original
        for A in original_non_terminals:
            new_productions[A] = []
            alpha_rules = []  # Reglas que no comienzan con A
            beta_rules = []   # Reglas que comienzan con A (recursivas)

            for production in self.productions[A]:
                if production and production[0] == A:
                    # Si la producción es de la forma A → A β
                    beta_rules.append(production[1:])
                else:
                    # Si la producción es de la forma A → γ
                    alpha_rules.append(production)

            if beta_rules:
                # Si hay recursividad, crear un nuevo no-terminal A'
                new_non_terminal = A + "'"

                # A → γA' para toda γ
                for alpha in alpha_rules:
                    if alpha:  # Si no es epsilon
                        new_rule = alpha.copy()
                        new_rule.append(new_non_terminal)
                        new_productions[A].append(new_rule)
                    else:
                        # Si es epsilon (A → ε), entonces A → A'
                        new_productions[A].append([new_non_terminal])

                # A' → βA' | ε para toda β
                new_productions[new_non_terminal] = []
                for beta in beta_rules:
                    new_rule = beta.copy()
                    new_rule.append(new_non_terminal)
                    new_productions[new_non_terminal].append(new_rule)
                new_productions[new_non_terminal].append([])  # Añadir ε

                # Añadir el nuevo no-terminal a la lista
                self.non_terminals.append(new_non_terminal)
            else:
                # Si no hay recursividad, mantener las producciones originales
                new_productions[A] = self.productions[A]

        self.productions = new_productions
        print("\nGramática sin recursividad por la izquierda:")
        self.print_grammar()
        return new_productions

    def print_grammar(self):
        for nt, prods in self.productions.items():
            for prod in prods:
                if prod:
                    print(f"{nt} → {' '.join(prod)}")
                else:
                    print(f"{nt} → ε")

    def compute_first_sets(self):
        print("\n=== Cálculo de PRIMEROS ===")
        # Inicializar PRIMEROS para todos los símbolos
        self.first_sets = {}
        for nt in self.non_terminals:
            self.first_sets[nt] = set()

        for terminal in self.terminals:
            self.first_sets[terminal] = {terminal}

        # Añadir epsilon a los conjuntos PRIMEROS
        for nt in self.non_terminals:
            if any(len(prod) == 0 for prod in self.productions[nt]):
                self.first_sets[nt].add('ε')

        # Calcular los conjuntos PRIMEROS
        changed = True
        while changed:
            changed = False
            for A in self.non_terminals:
                for production in self.productions[A]:
                    # Si es producción vacía (epsilon), ya está añadido
                    if not production:
                        continue

                    # Conjunto PRIMEROS para esta producción
                    k = 0
                    first_of_current = set()
                    all_can_derive_epsilon = True

                    while k < len(production) and all_can_derive_epsilon:
                        symbol = production[k]
                        if symbol in self.first_sets:
                            # Añadir todos los PRIMEROS excepto epsilon
                            first_of_current.update(self.first_sets[symbol] - {'ε'})

                            # Comprobar si el símbolo actual puede derivar en epsilon
                            if 'ε' not in self.first_sets[symbol]:
                                all_can_derive_epsilon = False
                        else:
                            # Si es un terminal que no está en first_sets
                            first_of_current.add(symbol)
                            all_can_derive_epsilon = False
                        k += 1

                    # Si todos los símbolos pueden derivar en epsilon, añadir epsilon
                    if all_can_derive_epsilon:
                        first_of_current.add('ε')

                    # Actualizar el conjunto PRIMEROS de A
                    old_size = len(self.first_sets[A])
                    self.first_sets[A].update(first_of_current)
                    if old_size < len(self.first_sets[A]):
                        changed = True

        # Mostrar los conjuntos PRIMEROS
        for nt in self.non_terminals:
            print(f"PRIMEROS({nt}) = {self.first_sets[nt]}")

        return self.first_sets

    def first_of_string(self, string):
        # Calcular PRIMEROS de una cadena de símbolos
        if not string:
            return {'ε'}

        result = set()
        all_derive_epsilon = True
        i = 0

        while i < len(string) and all_derive_epsilon:
            symbol = string[i]
            if symbol in self.first_sets:
                # Añadir todos los PRIMEROS excepto epsilon
                result.update(self.first_sets[symbol] - {'ε'})

                # Comprobar si el símbolo actual puede derivar en epsilon
                if 'ε' not in self.first_sets[symbol]:
                    all_derive_epsilon = False
            else:
                # Si es un terminal
                result.add(symbol)
                all_derive_epsilon = False
            i += 1

        # Si todos los símbolos pueden derivar en epsilon, añadir epsilon
        if all_derive_epsilon:
            result.add('ε')

        return result

    def compute_follow_sets(self):
        print("\n=== Cálculo de SIGUIENTES ===")
        # Inicializar SIGUIENTES para todos los no terminales
        self.follow_sets = {nt: set() for nt in self.non_terminals}

        # Añadir $ al SIGUIENTES del símbolo inicial
        self.follow_sets['S'].add('$')

        # Calcular los conjuntos SIGUIENTES
        changed = True
        while changed:
            changed = False
            for A in self.non_terminals:
                for production in self.productions[A]:
                    for i in range(len(production)):
                        B = production[i]
                        # Solo nos interesan los no terminales
                        if B not in self.non_terminals:
                            continue

                        # Si B es seguido por algún símbolo
                        if i + 1 < len(production):
                            # Calcular PRIMEROS(resto de la producción)
                            gamma = production[i+1:]
                            first_gamma = self.first_of_string(gamma)

                            # Añadir PRIMEROS(gamma) - {ε} a SIGUIENTES(B)
                            old_size = len(self.follow_sets[B])
                            self.follow_sets[B].update(first_gamma - {'ε'})
                            if old_size < len(self.follow_sets[B]):
                                changed = True

                            # Si epsilon está en PRIMEROS(gamma), añadir SIGUIENTES(A) a SIGUIENTES(B)
                            if 'ε' in first_gamma:
                                old_size = len(self.follow_sets[B])
                                self.follow_sets[B].update(self.follow_sets[A])
                                if old_size < len(self.follow_sets[B]):
                                    changed = True
                        else:
                            # Si B es el último símbolo, añadir SIGUIENTES(A) a SIGUIENTES(B)
                            old_size = len(self.follow_sets[B])
                            self.follow_sets[B].update(self.follow_sets[A])
                            if old_size < len(self.follow_sets[B]):
                                changed = True

        # Mostrar los conjuntos SIGUIENTES
        for nt in self.non_terminals:
            print(f"SIGUIENTES({nt}) = {self.follow_sets[nt]}")

        return self.follow_sets

    def compute_prediction_sets(self):
        print("\n=== Cálculo de Conjuntos de Predicción ===")
        # Calcular los conjuntos de predicción para cada regla
        self.prediction_sets = {}
        rule_number = 1

        for A in self.non_terminals:
            for production in self.productions[A]:
                # Calcular PRIMEROS de la producción
                first_prod = self.first_of_string(production)

                prediction = set()
                # Añadir PRIMEROS(producción) - {ε} a predicción
                prediction.update(first_prod - {'ε'})

                # Si epsilon está en PRIMEROS(producción), añadir SIGUIENTES(A)
                if 'ε' in first_prod:
                    prediction.update(self.follow_sets[A])

                rule_id = f"{A} → {' '.join(production) if production else 'ε'}"
                self.prediction_sets[rule_id] = prediction
                print(f"PREDICCIÓN({rule_number}: {rule_id}) = {prediction}")
                rule_number += 1

        return self.prediction_sets

    def is_ll1(self):
        print("\n=== Comprobación si la gramática es LL(1) ===")
        # Una gramática es LL(1) si para cada no terminal A, los conjuntos de predicción
        # de todas sus producciones son disjuntos.

        is_ll1 = True
        for A in self.non_terminals:
            productions_A = self.productions[A]
            prediction_sets_A = []

            for production in productions_A:
                rule_id = f"{A} → {' '.join(production) if production else 'ε'}"
                prediction_sets_A.append(self.prediction_sets[rule_id])

            # Comprobar si hay intersecciones entre los conjuntos de predicción
            for i in range(len(prediction_sets_A)):
                for j in range(i + 1, len(prediction_sets_A)):
                    intersection = prediction_sets_A[i] & prediction_sets_A[j]
                    if intersection:
                        is_ll1 = False
                        print(f"Conflicto entre reglas de {A}: {intersection}")

        if is_ll1:
            print("La gramática es LL(1)")
        else:
            print("La gramática NO es LL(1) debido a los conflictos mostrados arriba")

        return is_ll1

    def generate_asdr(self):
        print("\n=== Generación de ASDR (Analizador Sintáctico Descendente Recursivo) ===")
        asdr_code = """
class ASDR:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token = self.tokens[0] if tokens else '$'

    def consume(self, expected=None):
        if expected and self.token != expected:
            raise Exception(f"Error: Se esperaba {expected}, pero se encontró {self.token}")

        self.pos += 1
        if self.pos < len(self.tokens):
            self.token = self.tokens[self.pos]
        else:
            self.token = '$'  # Fin de entrada

    def parse(self):
        self.S()
        if self.token == '$':
            print("Análisis completado con éxito")
        else:
            raise Exception(f"Error: Se esperaba fin de entrada, pero se encontró {self.token}")
"""

        # Generar función para cada no terminal
        for A in self.non_terminals:
            # Reemplazar el apóstrofe de forma segura
            function_name = A
            if "'" in function_name:
                function_name = function_name.replace("'", "_prime")

            function_code = f"\n    def {function_name}(self):\n"
            function_code += f"        # Función para el no terminal {A}\n"

            # Añadir verificaciones para cada producción
            productions_A = self.productions[A]
            first_prod = True

            for production in productions_A:
                rule_id = f"{A} → {' '.join(production) if production else 'ε'}"
                prediction_set = self.prediction_sets[rule_id]

                condition = " or ".join([f"self.token == '{terminal}'" for terminal in prediction_set if terminal != 'ε'])
                if 'ε' in prediction_set:
                    # Si epsilon está en el conjunto de predicción, también incluimos el SIGUIENTES
                    follow_condition = " or ".join([f"self.token == '{terminal}'" for terminal in self.follow_sets[A]])
                    if condition and follow_condition:
                        condition = f"({condition}) or ({follow_condition})"
                    elif follow_condition:
                        condition = follow_condition

                if first_prod:
                    function_code += f"        if {condition or 'False'}:\n"
                    first_prod = False
                else:
                    function_code += f"        elif {condition or 'False'}:\n"

                # Implementar la producción
                function_code += "            # " + rule_id + "\n"
                for symbol in production:
                    if symbol in self.non_terminals:
                        # Reemplazar el apóstrofe en los nombres de funciones
                        symbol_function = symbol
                        if "'" in symbol_function:
                            symbol_function = symbol_function.replace("'", "_prime")
                        function_code += f"            self.{symbol_function}()\n"
                    else:
                        function_code += f"            self.consume('{symbol}')\n"

            # Añadir manejo de error
            function_code += "        else:\n"
            function_code += f"            raise Exception(f\"Error sintáctico en {A}: No se esperaba {{self.token}}\")\n"

            asdr_code += function_code

        print(asdr_code)
        return asdr_code
