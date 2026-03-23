#CODIGO ENCARGADO DE HACER  LAS OPERACIONES AVL




def rotacion_simple_derecha(nodo):
    n_raiz = nodo.izq
    nodo.izquierda = n_raiz.derecha
    n_raiz.derecha = nodo
    return n_raiz


def rotacion_simple_izquierda(nodo):
    n_raiz = nodo.der
    nodo.derecha = n_raiz.izquierda
    n_raiz.izquierda = nodo
    return n_raiz

def rotacion_doble_izquierda_derecha(nodo):
    nodo.izquierda = rotacion_simple_izquierda(nodo.izquierda)
    n_raiz= rotacion_simple_derecha(nodo)
    return n_raiz

def rotacion_doble_derecha_izquierda(nodo):
    nodo.derecha = rotacion_simple_derecha(nodo.derecha)
    n_raiz= rotacion_simple_izquierda(nodo)
    return n_raiz


def equilibrar(nodo):
    if nodo is None:
        return nodo

    equilibrio = obtener_equilibrio(nodo)

    if equilibrio > 1:
        if obtener_equilibrio(nodo.izquierda) >= 0:
            return rotacion_simple_derecha(nodo)
        else:
            return rotacion_doble_izquierda_derecha(nodo)

    if equilibrio < -1:
        if obtener_equilibrio(nodo.derecha) <= 0:
            return rotacion_simple_izquierda(nodo)
        else:
            return rotacion_doble_derecha_izquierda(nodo)

    return nodo

def obtener_equilibrio(nodo):
    if nodo is None:
        return 0
    return altura(nodo.izquierda) - altura(nodo.derecha)

def altura(nodo):
    if nodo is None:
        return 0
    return 1 + max(altura(nodo.izquierda), altura(nodo.derecha))