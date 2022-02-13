
# Regex Engine:

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