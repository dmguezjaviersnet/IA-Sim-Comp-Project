# Informe Proyecto Integrador (Inteligencia Artificial, Compilación y Simulación)

# El peligro en la órbita

## El DSL (OrbSim)

P

![main](./images/photo_2021-10-25_12-23-48.jpg)

- Parser LL(1)
- Evaluador de gramáticas atributadas (construcción de un AST)
- Autómata, con sus operaciones y método para llevar de NFA a DFA, para el análisis de expresiones regulares para el lexer.
  
También implementamos A*, pues consideramos que nos hará falta para el proyecto cuando esté más concebido, y ya empecemos a correr simulaciones.

## Regex Engine:

Usamos la siguiente gramática:

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

Usamos un parser LL(1)