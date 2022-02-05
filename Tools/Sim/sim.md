# Simulacion

La idea del proyecto es simular la interaccion de particula que orbitan la tierra que son consideradas desechos ya sea proveniente de restos de unidades de satelites cohetes etc que quedaron en deshuso en algun momento de la carrera espacial o de restos provenientes de colisiones entre esas particulas que se dividieron en otras particulas mas pequennas y que quedaron orbitando.

Estos objetos orbitan a una gran velocidad y puden ocasionar un danno grande a posibles lanzameintos de cehetes que se quieran enviar a la atmosfera. Por lo tanto es importante tener conocimiento de que tan probable es de que en un futuro un lanzamiento de un cohete sea exitoso o no dado si fue impactado por alguno de los abjetos basuras que se encuentran orbitando.

Con el lanzamientos de nuevas misiones se utilizan coehete que su funcionalidad basica es vancer la gravedad terrestre para llevar a la orbita baja o orbitas de mayor distancia satelites para ponerlos en orbita y una vez que cumplencon este objetivo pueden quedar orbitando y entrar de nuevo a la atmofera y se desintegran. Pero una mala maniobra hacer que algunos de sus componentes queden orbitando sin control alguno . Esto supone un gran problema para futuras misiones si no se tiene control de estos objetos.

Entonces para definir la simulacion vamos a definir algunos de las componentes que tenemos que son basicas para modelar la situacion. Entonces tendriamos que definir una entidad que nos defina los cohetes que se encargan de vencer la gravedad y que sirven para llevar satelites que una vez a la distancia adecuada se procede a ponerse en orbita. Tambien se definiria una clase satelite que representa a los satelites que estan funcionales y son utiles. Ademas se implementaria una clase que representa a la basura espacial que como definimos arriba son los elementos que quedan barado orbitando y de los cuales no se tiene control pero que se sabe su trayectoria. ademas se definirian puntos de lanzamieto. 


### Detectar colisiones entre objetos
Para detectar las colisiones entre los objetos es muy costoso ir de a pares de objetos y chequear si estos colisionan, para una muestra pequenna esto no supondria un problema, pero estmos tratando con miles de objetos por lo que decidimo usar una estructura de datos adecuada para esto. En un octree se puede representar el espacio tridimensional, entonces decidimos usar esta estructura de datos para representa la ubicacion de los objetos en el espacio. Definimos una clase Node que nos representa un nodo en el arbol octree, Ademas definimos una clase Octree que tiene un nodo root que es la raiz de nuestro arbol octree, (como una referencia al nodo "padre" de todo el arbol).

#### Como manejar el espacio geometrico? 
Para tener una representacion geometrica de nuestro entorno tomamos como referencia un eje de coordenadas de tres dimensiones donde el centro coincide con el centro del onjeto referente que en nuestro caso es la tierra. Para el espacio se pica por cubos. Esos cubos tiene un centro y un size, para representar esto definimos una clase ```Region``` que define a estos cuadrado, esta clase tiene un vector en 3d como centro y un valor que define el radio del cuadrado(que vendria siendo la distancia desde el centro hasta los laterales, no hasta las esquinas del cuadrado). Por facilidades para el calculo y la distribucion del espacio decidimos que todo los cubos tiendrian un size de longitud potencia de 2. Asi cada vez que entramos en un nuevo octante y se decide que hay que crear una nueva particion de ese octante en otros ocho mas pequenos el calculo y la determinacion de las nuevas dimensiones fuera mas precisa y facil de manejar. 

#### Como detectar las colisiones?
Decidimos que para detectar las colisiones determinamos que si un nodo del octree se encuentra en un punto donde ya no puede hace mas pequnno el espacio para representar mas objetos, y ademas en ese nodo existen mas de un objeto entonces  hay una colision entre los objetos que hay en ese nodo. 
Ademas de comprobar si colisionan los objetos que se encuntran sobre los ejes de alguno de los octantes que representan el espacio. 



# Elementos del lenguaje a implementar 

### Buid-In 
1. run -> empezar o continuar la simulacion 
2. stop -> detemer la simulacion
3. restart -> empezar desde el principio la simulacion 

4. int -> entero (puede ser el int de python )
5. float -> flotante (puede ser el float de python )


6. agent -> repsesenta un agente (puede ser visto como un objeto pero con peculiaridades)
7. obj -> repesenta un tipo objeto que son los obejetos de la simulacion 
8. tash -> representa basura (puede ser interpretado como un objeto )
9. callectors -> representa los recolectores de la basura
10. entities -> repesenta las entidades bajas de la simulacion 

### Definicion de objetos

1. masa -> la masa del objeto
2. posicion -> la posicion del objeto , (puede ser un "vector2d" o "vector3d")
3. diametro -> diametro del objeto (un foat)
4. move() -> un metodo que determina el proximo movimiento del objeto

### definicion de agentes

1. Todos los elementos de objecto (una clase mas baja en la gerarquia )
2. nextaction() -> un metodo que determina la proxima accion (puede ser sobrescrito)
3. freeze ()-> detine al agente y lo deja inmovil 
4. env -> el enviroment en que el agente se desenvuelve (esto es una referencia a una environment con el que interactua el agente)
5. live -> vida del agente (inicialmente 100)

### Definicion de Entities
1. posicion -> la posicion de la entidad
2. rool -> capacidad de interaccion con los agentes
3. quality -> un ranking que define la calidad de la entidad