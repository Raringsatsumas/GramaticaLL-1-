# GramaticaLL-1

## Descripción

Este código define una clase Grammar que:

- Inicializa una gramática con sus reglas, identifica los terminales y no terminales.

- Elimina la recursividad por la izquierda para volverla apta para un análisis LL(1).

- Calcula los conjuntos FIRST, FOLLOW y los conjuntos de predicción de cada producción.

- Comprueba si la gramática es LL(1) verificando que las predicciones de sus alternativas sean disjuntas.

- Genera automáticamente el código de un analizador sintáctico descendente recursivo (ASDR) basado en esos conjuntos y demuestra su uso sobre una lista de tokens.

### Class ASDR

La clase ASDR implementa un parser LL(1) de manera recursiva: recibe una lista de tokens, mantiene un cursor y un “lookahead” (self.token), y define un método por cada no terminal (S, A, B, B_prime, C, D, E) que, mediante condicionales basados en self.token, elige la producción correcta (o ε), consume terminales con consume()—que avanza y verifica el token esperado—y arroja excepciones claras ante desajustes; el método parse() inicia en S() y al finalizar comprueba que no queden tokens, imprimiendo éxito o señalando errores sintácticos.

Tras ejecutar estos pasos, las gramáticas resultan NO ser LL(1).

### Primer punto

- Recursión inmediata por la izquierda en B (y además recursión indirecta vía D → B).
- Solapamiento de conjuntos FIRST en las alternativas de S.
- Intersecciones FIRST/FOLLOW ocasionadas por producciones ε.

### Segundo punto

- Recursividad por la izquierda indirecta entre S, A y B
- Conflictos FIRST/FIRST: el terminal dos aparece en las dos primeras reglas de S.
- Abundancia de producciones ε que crean cruces FIRST/FOLLOW y evitan la decisión con sólo un token de mirada.

### Tercer punto

- Recursión izquierda inmediata: S → S uno.

- Prefijos comunes en las alternativas de S:
S → A B C y S → S uno comparten los tokens {dos, cuatro}, generando conflicto FIRST/FIRST.

- Cruces FIRST/FOLLOW adicionales debido a ε en S, A, B y C, que impiden al parser elegir correctamente con un único lookahead.

## Archivos

- 1.py: creación y análisis de la gramática 1
- 2.py: creación y análisis de la gramática 2
- 3.py: creación y análisis de la gramática 3
- asdr1.py: analizador sintáctico descendente recursivo de la gramática 1
- asdr2.py: analizador sintáctico descendente recursivo de la gramática 2
- asdr3.py: analizador sintáctico descendente recursivo de la gramática 3
- grammar.py: contiene la clase Grammar, que entre otras cosas (para una gramática dada) verifica si es ll1, elimina la recursión por izquierda, computa los conjuntos de primeros, siguientes y de predicción, etc. 

## Ejecución

Dependiendo del objetivo de la ejecución, reemplazar el nombre del archivo por el script deseado

```
python <script>
```
