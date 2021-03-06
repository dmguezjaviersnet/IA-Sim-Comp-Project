# Informe Proyecto Integrador (Inteligencia Artificial, Compilación y Simulación)

# El peligro en la órbita

![main](/photo_2021-10-25_12-23-48.jpg)

## Para ejecutar el proyecto

```
streamlit run ./orbsim_main.py
```

![main](./images/orbsim1.png)

## La simulación

Para la simulación hicimos una pequeña aplicación de python utilizando Pygame (como se muestra en la imagen anterior), donde se podrá visualizar todas las interacciones y eventos que se definan en el entorno de la simulación.

### El entorno

El entorno de nuestra simulación será un tablero 2D para representar el espacio que rodea a la Tierra y las entidades existentes en este espacio. Para representar este entorno utilizamos un `Quadtree progresivo`, o sea, que solamente se modifica en las regiones donde es necesario por la presencia de algún objeto, con el objetivo de encerrarlo y definir la región que este ocupa en el mapa. A pesar de no ser una estructura de datos recomendada para entornos dinámicos como el nuestro, hemos podido comprobar que para una demostración simple como la nuestra, con una profundidad de 8 el programa se comporta de forma aceptable con una cantidad moderada de entidades insertadas en el Quadtree.

Para poder realizar operaciones complejas en el Quadtree como el movimiento de objetos por el mapa, es necesario tener una representación en forma de grafo del mapa, y para esto es necesario computar para cada hoja del quadtree sus vecinos en el mapa. La representación de este grafo que utilizamos considera el centro de cada Quadtree como un nodo, y las aristas por lo tanto, van del centro de un Quadtree al centro de los Quadtrees vecinos. Acá mostramos 2 representaciones para los vecinos en un Quadtree que se mencionan en [1] por donde nos guiamos:

![neigh_repr](./images/quadtree_neigh_repr.png)

La que utilizamos es la que se encuentra a la izquierda.

### Las entidades

Las entidades que definimos por defecto para nuestra simulación son la basura espacial (`space debris`), los satélites(`satellite`) y unos agentes que son recolectores de basura espacial (`space debris collector`)  que serán configurables desde el DSL (__Orbsim__) que diseñamos.

**Space Debris**
La basura espacial tendrá una posición, velocidad, tamaño y color. La posición y velocidad se generan siempre de forma aleatoria.
Cuando se crea la misma mantiene una trayectoria alrededor de la órbita sobre la que se encuentra.
Esta puede ser definida desde el lenguaje orbsim de 2 formas:
- `spacedebris` te crea una basura con tamaño aleatorio y color predefinido
- `custom_space_debris(size, color)` te crea una basura con tamaño y color que se haya definido en el lenguaje.

Ejemplo:
```
let Tuple size1 = tuple(10,10);
let Tuple rgb1 = tuple(randint(0,255), randint(0,255), randint(0,255));
let SpaceDebris sp1 =  custom_space_debris(size1, rgb1);
let SpaceDebris sat1 = spacedebris;
```
Una vez creado un space debris en el lenguaje para agregarlo a la simulación debes usar `add_to_simulation`. Si se quiere
cambiar la basura desde el lenguaje a una órbita específica previamente declarada en el mismo se puede usar `move_to_orbit(orbit)`
Ejemplo:
```
let SpaceDebris sat1 = spacedebris;
sat1.add_to_simulation();
```
  
En caso de no definir ningún space debris inicial desde el lenguaje se crea cierta cantidad aleatoria de los mismos.


**Orbit**:

![orbita](./images/orbit_ejemplo1.png)

Las órbitas que consideramos para la simulación son de forma elíptica. Son representadas mediante **ElipticOrbit** y las propiedades
**semieje mayor**, **semieje menor** y **centro** son usadas para el movimiento de los objetos sobre la misma (satélites o basura espacial).
Desde el lenguaje se puede crear una órbita aleatoria mediante
`orbit`

Ejemplo:

![orbita2](./images/orbit_ej1.png)
![orbita2](./images/orbit_ej2.png)


**Satellite**

![satellite](./images/satellite1.png)
Los satélites tienen una posición, tamaño, tiempo de vida y velocidad. Estos se generan mayormente mediante un evento pero también
desde el lenguaje  __orbsim__ se puede añadir un nuevo satélite con posición, tiempo de vida , velocidad  y órbita sobre la que circula aleatorios mediante `satellite` y luego para añádirlo a la simulación usar `add_to_simulation`. Los satélites tienen un tiempo de vida útil que se irá reduciendo con el paso del tiempo o debido a las colisiones que ocurran durante el transcurso de la simulación.

Ejemplo de como crear satélites en el lenguaje orbsim:
```
let Int counter = 0;
loop (counter < randint(2, 6) ){
    counter = counter + 1;
    let Orbit o1 = orbit;
    o1.add_to_simulation();
};

counter = 0;
loop (counter < randint(2, 10) ){
    counter = counter + 1;
    let Satellite sat1 = satellite;
    sat1.add_to_simulation();
};
```






### Implicaciones y comportamiento del ambiente

Generalmente hay más de una órbita, y dentro de una misma órbita los objetos pueden ir a diferente velocidad y sentido por lo que inevitablemente ocurrirán `colisiones` entre distintos objetos ya sean basura espacial, agentes o satélites de distintas órbitas, o incluso en la misma órbita dependiendo de la velocidad y el sentido con el que se mueva ese objeto en su órbita. Estas colisiones tendrán ciertas consecuencias y efectos, fragmentación de la basura (reducción de su tamaño), desaparición de cierta basura (absorción por otra basura mucho más grande), reducción de la vida útil de los satélites, etc. Para poder encontar las colisiones simplemente analizamos cada hoja del Quadtree y analizamos si cualquier par de objetos en esa hoja se solapa parcialmente.

### Eventos


Usamos el modelo de dos servidores en serie para la simulación del proceso de fabricación y 
despegue de un  cohete para la posterior puesta en órbita de los satélites que contiene el mismo.
El tiempo de arribo del primer cohete que se va a fabricar se genera inicialmente, luego una vez que llega
si no hay ningún cohete en fabricación se genera el tiempo de partida de este y se pone en fabricación, 
en caso de que haya ya un cohete en fabricación se pone en cola. Una vez termina el proceso de fabricación
de un cohete se pasa al proceso de despegue . Para despegar si no hay ningún cohete despegando se genera el tiempo
de partida del nuevo cohete y se pone a despegar , en caso contrario se pone en cola. Una vez termina el proceso 
de despegue de un cohete este suelta un satélite en  una órbita aleatoria de las existentes. Un cohete puede tener a lo sumo 1 satélite.
El lambda usado y el tiempo de duración es configurable desde el lenguaje usando `custom_launchpad`.



Ejemplos:

```
custom_launchpad(5000, 0.001);
```

donde el primer parámetro es el tiempo de cierre y el segundo el lambda que se va a usar en la generación del tiempo de espera cada que vez que sea necesario para el próximo tiempo de arribo o para el tiempo de la próxima partida.

![main](./images/launchpad1.png)
![main](./images/launchpad2.png)


Ejemplo donde se customiza el launchpad y se generan orbitas y objetos custom desde el lenguaje orbsim:

![main](./images/img10.png)
![main](./images/img11.png)


En nuestra simulación  ocurre la aparición de nueva basura espacial de forma ocasional mediante un proceso de Poisson homogéneo. Tanto el T como el lambda del mismo son configurables desde el lenguaje orbsim usando `custom_create_space_debris_event`. Esta nueva basura que se genera tiene un tamaño,
posición, órbita sobre la que circula y velocidad aleatoria.

Ejemplo:
```
custom_create_space_debris_event(200, 0.8)
start;
```







### Los recolectores

Los `recolectores de basura espacial`, son agentes que definimos y que van a operar en nuestro entorno con el objetivo de recolectar la mayor cantidad de basura posible. Estos agentes tienen definidas varias características que impondrán restricciones a su comportamiento:

- Tienen definida una capacidad límite que se reducirá cada vez que recojan algo de basura espacial, dependiendo del tamaño de la basura y que eventualmente les impedirá recolectar basura de gran tamaño.
  
- Tienen definida una cantidad de combustible que se irá reduciendo con cada acción que realicen en el entorno, ya sea recolectar basura o moverse, y que eventualmente los dejará sin combustible para realizar estas acciones por lo que quedarán inmóviles.

- Tienen definido un tiempo de vida que se irá reduciendo con el paso del tiempo y que eventualmente los dejará inservibles.

- Tienen definido un rango de percepción, que le permitirá ver mayor o menor parte del entorno para tomar sus decisiones. Este rango de percepción lo definimos en términos del Quadtree.

El comportamiento de los recolectores está definido por varias acciones y restricciones.

Acciones:

- Recolectar basura (el agente necesita estar bien cerca del objeto para realizar esta acción).
- Moverse hacia la basura si en su rango de percepción detectó basura.
- Moverse de forma aleatoria por el mapa sino detectó basura en su rango de percepción.
- No realizar nada (idle), para indicar que ya puede realizar una nueva acción la próxima vez.
  
Restricciones:

- Solo puede realizar acciones si le queda tiempo de vida.
- Siempre priorizará recolectar la basura de menor tamaño en su rango de percepción, aunque tenga que moverse para esto.
- Si hay 2 basuras con el mismo tamaño, priorizará recolectar la que esté más cercana.
- Solo puede moverse si le queda combustible.
- Solo puede recolectar basura si le queda suficiente combustible o le queda suficiente capacidad para recolectar la basura.

El movimiento lo realiza entre nodos del `Quadtree`, siguiendo el camino más corto utilizando `A*` y la distancia euclideana al destino como heurística.

**Creando un agente recolector de basura espacial desde lenguaje orbsim:**
Se puede crear de dos formas:
- `agent` crea un agente recolector de basura con parámetros aleatorios
- `custom_create_agent(lifetime, capacity,  fuel, perception_range, velocity)` crea un agente recolector de basura usando los parámetros de entrada definido en el lenguaje


Ejemplo:

```
let Agent a1 = custom_create_agent(100, 5000, 500, 8, 50);
a1.add_to_simulation();
let Agent a2 = custom_create_agent(300, 4000, 40500, 8, 15);
a2.add_to_simulation();
let Agent a3 = custom_create_agent(500, 1000, 1500, 2, 5);
a3.add_to_simulation();
let Agent ar = agent;
ar.add_to_simulation();
start;
```

![main](./images/agent2.png)
Cada vez que el agente se va a mover para un objetivo se muestra el camino parar llegar al mismo.

Para mostrar el quadtree de forma visual se puede presionar la tecla `q` o desde el lenguaje orbsim escribir `drawquadtree`
para que se ejecute con la visualización del quadtree. Por defecto esta visualización está desactivada.

Para mostrar las órbitas de forma visual se puede presionar la tecla `o` o desde el lenguaje orbsim escribir  `show_orbits` para que se ejecute con la visualización de las órbitas. Por defecto esta visualización está desactivada.

Para pausar la simulación presione la tecla `p`.

Para mostrar el movimiento de la tierra se puede presionar la tecla `K_UP` o desde el lenguaje escribir `animate_earth` para 
que se ejecture con la visualización del movimiento. Por defecto esta visualización está desactvida.

Si se selecciona con el mouse un objeto orbitando se muestra una recta desde su centro hasta el punto centro de la órbita sobre la que está.

![main](./images/img12_select.png)




## El proceso de compilación

### Gramáticas

Implementamos clases `Grammar`, `Production`, `Terminal`, `NonTerminal` para representar gramáticas de forma intuitiva y sencilla. `Grammar` se construye con una lista de terminales, una lista de no-terminales, un no-terminal inicial y una lista de producciones. La producción nosotros la consideramos como un no-terminal, con todas sus posibles partes derechas, por lo que le pasamos también una lista con las reglas sintáticas de cada posible parte derecha.

```python
# No terminales
E = Non_terminal('E', 'ast')
T = Non_terminal('T', 'ast', 'tmp')
F = Non_terminal('F', 'ast')
nts = [E, T, F]

# Terminales
mul = Terminal('*')
div = Terminal('/')
add = Terminal('+')
sub = Terminal('-')
openb = Terminal('(')
closedb = Terminal(')')
integer = Terminal('integer')
empty = Epsilon()
eof = Eof()
terminals = [add, sub, mul, div, openb, closedb, integer, empty, eof]

# Producciones
p1 = Production(E,
                [[T, add, E], [T, sub, E], [T]],
                [[(E1_rule, True)], [(E2_rule, True)], [(E3_rule, True)]]
                )

p2 = Production(T, 
                [[F, mul, T], [F, div, T], [F]], 
                [[(T1_rule, True)], [(T2_rule, True)], [(T3_rule, True)]]
                )

p3 = Production(F, 
                [[openb, E, closedb], [integer]],
                [[(F1_rule, True)], [(F2_rule, True)]]
                )
prods = [p1, p2, p3]

arth_grammar = Grammar(terminals, nts, E, prods)
```

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

Implementamos el algoritmo de parsing para gramáticas LL(1) visto en conferencia, para poder parsear los tokens de Regex, a un AST con algunas de las operaciones de Regex:

- Concatenación
- Union |
- Clausura *
- Clausura positiva +
- Rangos [0-9], [a-z], [A-Z]
- ?

Luego en la evaluación de ese AST es donde construimos el autómata que reconoce esa expresión regular.

Entonces para tokenizar, creamos una clase `Lexer`, que recibe como parámetro de entrada un diccionario que a cada expresión regular (un string) que represente un token en nuestro lenguaje, le corresponda un `Token_Type`. Dependiendo del orden que pasemos como argumento las expresiones regulares que queremos reconocer y tokenizar en nuestro lenguaje, es la prioridad que se le dará a dicho Token a la hora de reconocerlo, por tanto si está más arriba en la declaración, significa que tiene mayor prioridad.

``` python
lexer = Lexer([
    ('loop', Token_Type.loop),
    ('func', Token_Type.func),
    ("([A-Z])([a-z]|[A-Z]|[0-9])*", Token_Type.type_id_orbsim)
])
```

### Parser

Para parsear implementamos clases `Lr0Item` con la representación de hasta dónde hemos leído los símbolos de una producción y `Lr1Item` el lookahead además, y el algoritmo de parsing para gramáticas LR(1) visto en conferencia utilizando la clase `State` que mencionamos previamente para representar cada estado del autómata LR(1), con sus correspondientes items LR(1). Para esto también añadimos un proceso de serialización para no tener que computar la tabla __ACTION-GOTO__ más de una vez, ya que es un proceso que puede demorar bastante. Nuestras clases `Lr0Item` y `Lr1Item` son hasheables, esto nos hizo falta porque durante el proceso de construcción del autómata LR(1) necesitábamos saber cuando generábamos un estado que ya existía, y que íbamos guardando en un diccionario de hash: estado.

### AST
En `orbsim_languaje.orbsim_ast` están los nodos para la representación del AST.
### Chequeo Semántico
Para el chequeo semántico se realizan tres recorridos sobre el AST usando el patrón visitor:
*TypeCollector*:Parar recolectar los tipos definidos en el lenguaje Orbsim. Estos tipos
pueden ser builtin o declarados mediante clases en el código.
*TypeBuilder*: Parar identificar los atributos y métodos definidos para los tipos.
*TypeChecker*: Para identificar el cumplimiento de las reglas semántica definidas para Orbsim

### El DSL (OrbSim)

Nuestra idea fue tener un lenguaje con algunas cosas de un lenguaje de propósito general, como ciclos, condicionales, variables, y decidimos agregar clases, pues consideramos que es una herramienta que facilitaría la incorporación de nuevos tipos al lenguaje que permitieran crear abstracciones para nuevos objetos, muchos de estos podrían estar como built-in.

Algunas reglas sintácticas que definimos en nuestro lenguaje:

- Los nombres de funciones y variables empiezan con minúscula.
- Los nombres de tipos built-in, así como de clases empiezan con mayúscula.
- La declaración de una clase, un ciclo, una condicional o una función se realiza entre llaves.
- Todas las instrucciones terminan con ;

Algunas reglas semánticas que definimos en nuestro lenguaje:
- No pueden exister dos variables con el mismo nombre en el mismo Scope.
- No pueden haber dos funciones  con el mismo nombre y la misma cantidad de parámetros.
- Dos métodos con el mismo nombre y la misma cantidad de parámetros no pueden estar definidos en un mismo tipo.
- La operación % solo es entre números enteros
- Las operaciones aritméticas +,-,*,/ puede ser entre dos números enteros o entre dos números float.
- Los elementos de una lista tienen que ser del mismo tipo
- 

# Tipos Builtins:
`Int`, `Float`, `String`, `List`(una lista de elementos del mismo tipo), `Tuple`,  `Bool`, `Vector3`
Declaración de variables en Orbsim:
`let <Type> id '=' <Expr>`
```
let Int a = 1;
```

Condicionales en Orbsim:
`if (<CondExpr>) then {List[stmt]} else {List[stmt]};`

```
let Int a = 2;
let Int b = 20;
 
if (a > b) then {
    b = b-2+1;
} 
else{
    b = a +2-1;
};
....
```

Ciclos en Orbsim:

`loop (<CondExpr>) {List[stmt]};`
```
let Int counter = 0;
let Int doble   = 10;

loop(counter < 10){
    doble = 2*2;
    counter = counter + 1;
};
....
```



Declaración de funciones en Orbsim:
`func <type> id (List[Params]) {Body};  `


```
func Int fib(Int n){
    if (n == 1 || n == 0) then {
        ret 1;
    }
    else{
        ret fib(n-1) + fib(n-2);
    };
};

let Int f = fib(5);
```

Definiendo  una clase en Orbsim:
`class <ID> {};`
```
class Point {
    Int a;
    Int b;
    func Point add (Point b){
        ret make Point(this.a + b.a, this.b + b.b);
        };
    };
...
```

Creando una instancia de una clase en Orbsim:
```
   let Point a =  make Point(2,3);
   ...
```

Las clases tienen atributos cuyo valor se le asigna al crear una instancia de la misma siempre verificando que los tipos de las expresiones a evaluar coincidan con los tipos de los atributos.

El lenguaje permite creación de números enteros aleatorios mediante `randint` y de números float aleatorios mediante
`randfloat`

![rand](./images/img13.png)
![rand](./images/img14.png)

## Interfaz Gráfica:

Para la interfaz gráfica se usó streamlit parar el editor de código junto con pygame para la parte de simulación e IA . 

Si el código compila y ejecuta correctamente:

![main](./images/img1.png)

En caso de haya algún error de compilación o ejecución.
![main](./images/img2.png)
![main](./images/img3.png)
![main](./images/img7.png)
![main](./images/img4.png)
![main](./images/img8.png)

Otros ejemplos:
![main](./images/img5.png)
![main](./images/img6.png)
![main](./images/img9.png)


## Referencias

- [1] PATHFINDING IN 3D SPACE - A*, THETA*, LAZY THETA* IN OCTREE STRUCTURE. March 8, 2016 Ruoqi He & Chia-Man Hung