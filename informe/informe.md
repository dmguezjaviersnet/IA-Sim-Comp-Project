# Informe Proyecto Integrador (Inteligencia Artificial, Compilación y Simulación)

# El peligro en la órbita

![main](./images/photo_2021-10-25_12-23-48.jpg)


## El proceso de compilación


### Gramáticas

Implementamos clases `Grammar`, `Production`, `Terminal`, `NonTerminal` para representar gramáticas de forma intuitiva y sencilla.

### Lexer y Regex Engine

Implementamos nuestro propio Regex Engine como vimos en conferencia, haciendo uso de clases que implementamos como `Automaton` con los métodos para computar __epsilon clausura__ y __goto__, y también un método para convertir de autómata no determinista (__NFA__) a determinista (__DFA__). También implementamos una clase `State`, para representar los estados de un autómata (y el autómata en sí de otra forma), que nos facilitó el trabajo.

Diseñamos la siguiente gramática LL(1) de expresiones regulares básica para el Regex Engine:

```
   E -> T X
   X -> '|' T X
      | epsilon
   T -> F Y
   Y -> F Y 
      | epsilon
   F -> A P
   A -> character
      | ( E )
      | [ W ]
      | ε
      | \\n
   W -> R S
   S -> R S
      | epsilon
   R -> B Q
   Q -> - B Q
      | epsilon
   B -> character
   C -> character
   character -> any_character_except_metas
         | '\\' any_character_except_specials

   P -> M
      | epsilon
   M -> *
      | ?
      | +
```

Como es obvio, implementamos el algoritmo de parsing para gramáticas LL(1) visto en conferencia, para poder parsear los tokens de Regex, a un AST con algunas de las operaciones de Regex:

- Concatenación
- Union |
- Clausura *
- Clausura positiva +
- Rangos [0-9], [a-z]
- ?

Luego en la evaluación de ese AST es donde construimos el autómata que reconoce esa expresión regular.

Entonces para tokenizar, creamos una clase `Lexer`, que recibe como parámetro de entrada un diccionario que a cada expresión regular (un string) que represente un token en nuestro lenguaje, le corresponda un `Token_Type`. Dependiendo del orden que pasemos como argumento las expresiones regulares que queremos reconocer y tokenizar en nuestro lenguaje, es la prioridad que se le dará a dicho Token a la hora de reconocerlo, por tanto si está más arriba en la declaración, significa que tiene mayor prioridad.

### Parser

Para parsear implementamos clases `Lr0Item` y `Lr1Item`, y el algoritmo de parsing para gramáticas LR(1) visto en conferencia utilizando la clase `State` que mencionamos previamente para representar cada estado del autómata LR(1), con sus correspondientes items LR(1). Para esto también añadimos un proceso de serialización para no tener que computar la tabla __ACTION-GOTO__ más de una vez, ya que es un proceso que puede demorar bastante.
  
También implementamos A*, pues consideramos que nos hará falta para el proyecto cuando esté más concebido, y ya empecemos a correr simulaciones.

### El DSL (OrbSim)

Nuestra idea fue tener un lenguaje con algunas cosas de un lenguaje de propósito general, como ciclos, condicionales, variables, y decidimos agregar clases, pues consideramos que es una herramienta que facilitaría la incorporación de nuevos tipos al lenguaje que permitieran crear abstracciones para nuevos objetos, muchos de estos podrían estar como builtin.


## Regex Engine:

Usamos la siguiente gramática:

## Interfaz Gráfica:

Para la interfaz gráfica usamos streamlit:




Usamos un parser LL(1)

