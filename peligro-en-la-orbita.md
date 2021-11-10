## Breve resumen

Nuestra idea de forma general es simular y analizar la complejidad de la situación de la basura espacial en la órbita terrestre
y como pudiera afectar a futuras misiones espaciales.

### *Simulación*

- Simular el estado del campo de escombros que orbita la Tierra, y como la ocurrencia de colisiones con satélites, naves u otros escombros, puede incrementar la presencia de basura espacial.
- Simular despegues de naves desde la tierra y su viaje a través de los escombros, así como las colisiones con la basura espacial.

### *IA*

- Dada una nave que desea despegar, poder trazar una ruta, a través de los escombros que pueda encontrarse la nave en la órbita, que permita evitar colisiones o al menos disminuir la probabilidad de que ocurran, tomando en cuenta la capacidad de maniobrar de cada nave, la disponibilidad de combustible para hacer la maniobra, etc.

- Como poner un satélite en órbita de tal forma que podamos minimizar las probabilidades de que ocurra una colisión con basura espacial y a la vez funcione correctamente.

### *Compilación*

Crear un lenguaje con una sintaxis que permita:

- Definir todo tipo de nave espacial o satélite con sus características.
- Definir el campo de escombros que se desee.
- Correr simulaciones de lanzamientos de satélites o naves espaciales, con las respectivas implicaciones, como posibles colisiones que aumentan la cantidad de basura espacial, uso de combustible de la nave o satélite, etc.
- Conocer la trayectoria de una nave en una simulación.
- Simular el proceso de creación de nuevos escombros a causa de colisiones.
- Simular la evolución del campo de escombros a lo largo del tiempo.
- Establecer parámetros para las simulaciones.
- Conocer el estado de la simulación para tomar decisiones que permitan mejorar el resultado y este pueda ser utilizado en la vida real.

Consideramos que el problema es bastante complejo, por lo que nos concentraremos inicialmente en algunas de las características que consideremos más importantes para el objetivo de nuestro software, y luego si tuviésemos nuevas ideas para mejorar el programa, intentaríamos incorporarlas.

## Miembros del equipo

- Javier E. Domínguez Hernández C-312 (@dmguezjaviersnet)
- David Orlando De Quesada Oliva C-311 (@dav1ddq0)
- Daniel De La Cruz Prieto C-311 (@dcruzp)
