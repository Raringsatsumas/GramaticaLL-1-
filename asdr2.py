class ASDR:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token = self.tokens[0] if tokens else '$'
        self.recursion_level = 0
        self.recursion_limit = 1000
        self.visited = set()   # Para detección de llamadas repetidas
        # (la memoización se podría usar en lugar de visited)

    def consume(self, expected=None):
        if expected and self.token != expected:
            raise Exception(f"Error: Se esperaba {expected}, pero se encontró {self.token}")
        self.pos += 1
        self.token = self.tokens[self.pos] if self.pos < len(self.tokens) else '$'

    def parse(self):
        self.visited.clear()
        self.S()
        if self.token == '$':
            print("Análisis completado con éxito")
        else:
            raise Exception(f"Error: Se esperaba fin de entrada, pero se encontró {self.token}")

    def S(self):
        key = ('S', self.pos)
        if key in self.visited:
            return
        self.visited.add(key)
        self.recursion_level += 1
        try:
            # S → B uno | dos C | ε
            if self.token in {'uno'} or self.token in {'tres','cuatro','cinco'} or self.token in {'dos'}:
                # cubrimos B uno y dos C con distinta prioridad
                if self.token in {'uno','tres','cuatro','cinco'}:
                    self.B()
                    self.consume('uno')
                else:
                    self.consume('dos')
                    self.C()
            elif self.token in {'$', 'tres'}:
                # ε
                pass
            else:
                raise Exception(f"Error sintáctico en S: No se esperaba {self.token}")
        finally:
            self.recursion_level -= 1
            self.visited.remove(key)

    def A(self):
        key = ('A', self.pos)
        if key in self.visited:
            return
        self.visited.add(key)
        self.recursion_level += 1
        try:
            # A → S tres B C | cuatro | ε
            if self.token in {'dos','tres','cuatro','uno','cinco'}:
                if self.token == 'cuatro':
                    self.consume('cuatro')
                else:
                    self.S()
                    self.consume('tres')
                    self.B()
                    self.C()
            elif self.token in {'cinco','seis','$'}:
                # ε (cinco está en Follow(A))
                pass
            else:
                raise Exception(f"Error sintáctico en A: No se esperaba {self.token}")
        finally:
            self.recursion_level -= 1
            self.visited.remove(key)

    def B(self):
        key = ('B', self.pos)
        if key in self.visited:
            return
        self.visited.add(key)
        self.recursion_level += 1
        try:
            # B → A cinco C seis | ε
            if self.token in {'dos','tres','cuatro','uno','cinco'}:
                # Primera producción
                self.A()
                self.consume('cinco')
                self.C()
                self.consume('seis')
            elif self.token in {'$', 'tres', 'siete','uno','cinco','seis'}:
                # ε
                pass
            else:
                raise Exception(f"Error sintáctico en B: No se esperaba {self.token}")
        finally:
            self.recursion_level -= 1
            self.visited.remove(key)

    def C(self):
        key = ('C', self.pos)
        if key in self.visited:
            return
        self.visited.add(key)
        self.recursion_level += 1
        try:
            # C → siete B | ε
            if self.token == 'siete':
                self.consume('siete')
                self.B()
            elif self.token in {'$', 'seis','cinco','tres'}:
                # ε
                pass
            else:
                raise Exception(f"Error sintáctico en C: No se esperaba {self.token}")
        finally:
            self.recursion_level -= 1
            self.visited.remove(key)

print("Ejemplo con cadena incorrecta")
tokens = ['uno', 'dos', 'tres', 'tres']
parser = ASDR(tokens)
try:
    parser.parse()
except Exception as e:
    print(e)

print("Ejemplo con cadena correcta")
tokens = ['dos', 'siete']
parser = ASDR(tokens)
try:
    parser.parse()
except Exception as e:
    print(e)
