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

    def S(self):
        # Función para el no terminal S
        if self.token == 'dos' or self.token == '$' or self.token == 'tres' or self.token == 'cuatro' or self.token == 'uno':
            # S → A B C S'
            self.A()
            self.B()
            self.C()
            self.S_prime()
        else:
            raise Exception(f"Error sintáctico en S: No se esperaba {self.token}")

    def A(self):
        # Función para el no terminal A
        if self.token == 'dos':
            # A → dos B C
            self.consume('dos')
            self.B()
            self.C()
        elif self.token == '$' or self.token == 'uno' or self.token == 'tres' or self.token == 'cuatro':
            # A → ε
            pass
        else:
            raise Exception(f"Error sintáctico en A: No se esperaba {self.token}")

    def B(self):
        # Función para el no terminal B
        if self.token == 'tres' or self.token == 'cuatro':
            # B → C tres
            self.C()
            self.consume('tres')
        elif self.token == '$' or self.token == 'uno' or self.token == 'tres' or self.token == 'cuatro':
            # B → ε
            pass
        else:
            raise Exception(f"Error sintáctico en B: No se esperaba {self.token}")

    def C(self):
        # Función para el no terminal C
        if self.token == 'cuatro':
            # C → cuatro B
            self.consume('cuatro')
            self.B()
        elif self.token == '$' or self.token == 'uno' or self.token == 'tres' or self.token == 'cuatro':
            # C → ε
            pass
        else:
            raise Exception(f"Error sintáctico en C: No se esperaba {self.token}")

    def S_prime(self):
        # Función para el no terminal S'
        if self.token == 'uno':
            # S' → uno S'
            self.consume('uno')
            self.S_prime()
        elif self.token == '$':
            # S' → ε
            pass
        else:
            raise Exception(f"Error sintáctico en S': No se esperaba {self.token}")

print("Ejemplo con cadena incorrecta")
tokens = ['uno', 'dos', 'tres', 'tres']
parser = ASDR(tokens)
try:
    parser.parse()
except Exception as e:
    print(e)

print("Ejemplo con cadena correcta")
tokens = ['uno', 'uno', 'uno']
parser = ASDR(tokens)
try:
    parser.parse()
except Exception as e:
    print(e)
