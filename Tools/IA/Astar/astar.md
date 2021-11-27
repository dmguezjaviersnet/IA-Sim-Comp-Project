# Astar

En el fichero `Graph.py` hay una implementacion de un grafo que recibe un `defaultdic` para construir el grafo , ese defualtdic contiene la informacion de las aristas y de los pesos de estas. 
En la misma clase hay un metodo que se llama `astar` el cual recive `src` (vertice inicial) y `dest` (vertice final) y el metodo te devuelve el camino de `src` a `dest` usando el algoritmo de `astar`  para encontrar el camino. Actualmenta la heuristca que tiene es la distancia de Manhatan, la cual se peude cambiar sobrescribiendo el metodo `heuristic` de la calse `Graph` para que este actualice el array `_h` donde se guarda el valor de la heuristica para cada nodo para despues ser usado en el algoritmo.
