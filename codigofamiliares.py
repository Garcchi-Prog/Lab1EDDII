def BuscarPadre(raiz, nodo):
    if raiz is None:
        return None
    
    # Verificamos si  la raiz es el padre del nodo buscado tanto en la izquierda como en la derecha
    if (raiz.izquierda is  nodo) or (raiz.derecha is     nodo):
        return raiz
    
    #Se aplica recursion  para buscar el padre en el subarbol izquierdo 
    padre_izquierda = BuscarPadre(raiz.izquierda, nodo)
    if padre_izquierda is not None:
        return padre_izquierda
    
    #Se aplica recursion para buscar el padre en el subarbol derecho
    padre_derecha = BuscarPadre(raiz.derecha, nodo)
    if padre_derecha is not None:
        return padre_derecha

    #Si no se encuentra el nodo en ninguno de los subarboles, se devuelve none
    return None

def BuscarAbuelo (raiz, nodo):
    if raiz is None:
        return None
    
    #Se busca el padre del nodo dado
    padre = BuscarPadre(raiz, nodo)
    if padre is None:
        return None
    
    #Se busca el abuelo utilizando la funcion BuscarPadre, solamente que el nodo a buscar sera el del padre 
    abuelo=BuscarPadre(raiz, padre)
    return abuelo

def BuscarTio (raiz, nodo):
    if raiz is None:
        return None

    #Se busca al padre para tener una referencia para buscar el abuelo
    padre=BuscarPadre(raiz, nodo)
    #Si el padre no existe, no se puede encontrar al tio
    if padre is None:
        return None
    
    #Se busca el abuelo para tener una referencia para localizar al tio
    abuelo=BuscarPadre(raiz, padre)
    #Si el abuelo no existe, no se puede encontrar al tio
    if abuelo is None:
        return None
    
    #Caso 1: El hijo izquierdo del abuelo es el padre, por lo tanto el hijo derecho sera el tio
    if abuelo.izquierda is padre:
        return abuelo.derecha
    #Caso 2: El hijo derecho del abuelo es el padre, por lo tanto el hijo izquierdo sera el tio
    elif abuelo.derecha is padre:
        return abuelo.izquierda
    #Caso 3: El padre no es hijo del abuelo, por lo cual se retorna None
    else:
        return None