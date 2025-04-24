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
        if self.token == 'cuatro' or self.token == 'dos' or self.token == '$' or self.token == 'seis':
            # S → A B C
            self.A()
            self.B()
            self.C()
        elif self.token == 'cuatro' or self.token == 'uno' or self.token == 'tres':
            # S → D E
            self.D()
            self.E()
        else:
            raise Exception(f"Error sintáctico en S: No se esperaba {self.token}")

    def A(self):
        # Función para el no terminal A
        if self.token == 'dos':
            # A → dos B tres
            self.consume('dos')
            self.B()
            self.consume('tres')
        elif self.token == 'cuatro' or self.token == 'tres' or self.token == '$' or self.token == 'cinco' or self.token == 'seis':
            # A → ε
            pass  # Epsilon producción
        else:
            raise Exception(f"Error sintáctico en A: No se esperaba {self.token}")

    def B(self):
        # Función para el no terminal B
        if self.token == 'cuatro' or self.token == 'tres' or self.token == '$' or self.token == 'cinco' or self.token == 'seis':
            # B → B'
            self.B_prime()
        else:
            raise Exception(f"Error sintáctico en B: No se esperaba {self.token}")

    def C(self):
        # Función para el no terminal C
        if self.token == 'seis':
            # C → seis A B
            self.consume('seis')
            self.A()
            self.B()
        elif self.token == 'cinco' or self.token == '$':
            # C → ε
            pass  # Epsilon producción
        else:
            raise Exception(f"Error sintáctico en C: No se esperaba {self.token}")

    def D(self):
        # Función para el no terminal D
        if self.token == 'uno':
            # D → uno A E
            self.consume('uno')
            self.A()
            self.E()
        elif self.token == 'cuatro' or self.token == 'tres':
            # D → B
            self.B()
        else:
            raise Exception(f"Error sintáctico en D: No se esperaba {self.token}")

    def E(self):
        # Función para el no terminal E
        if self.token == 'tres':
            # E → tres
            self.consume('tres')
        else:
            raise Exception(f"Error sintáctico en E: No se esperaba {self.token}")

    def B_prime(self):
        # Función para el no terminal B'
        if self.token == 'cuatro':
            # B' → cuatro C cinco B'
            self.consume('cuatro')
            self.C()
            self.consume('cinco')
            self.B_prime()
        elif self.token == 'cinco' or self.token == 'tres' or self.token == '$' or self.token == 'seis':
            # B' → ε
            pass  # Epsilon producción
        else:
            raise Exception(f"Error sintáctico en B': No se esperaba {self.token}")

print("Ejemplo con cadena incorrecta")
tokens = ['uno', 'dos', 'tres', 'tres']
parser = ASDR(tokens)
try:
    parser.parse()
except Exception as e:
    print(e)

print("Ejemplo con cadena correcta")
tokens = ['tres']
parser = ASDR(tokens)
try:
    parser.parse()
except Exception as e:
    print(e)
