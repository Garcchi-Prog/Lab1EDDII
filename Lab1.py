import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import csv
import os
import random
from datetime import datetime

# COLORES GLOBALES (simples, definidos como variables sueltas)
# ============================================================
# Se definen como constantes globales para poder reutilizarlos
# en toda la interfaz sin repetir los valores hexadecimales.
# Cambiar un color aqui lo cambia en toda la aplicacion.
COLOR_FONDO = "#2c3e50"      # Azul oscuro: fondo principal de la ventana
COLOR_PANEL = "#34495e"      # Azul medio: fondo de paneles laterales
COLOR_TARJETA = "#1C2128"    # Negro oscuro: fondo de tarjetas y areas de texto
COLOR_BORDE = "#7f8c8d"      # Gris: separadores visuales entre secciones
COLOR_BOTON = "#3498db"      # Azul brillante: botones de accion principal
COLOR_EXITO = "#2ecc71"      # Verde: operaciones exitosas (insertar, encontrado)
COLOR_ERROR = "#e74c3c"      # Rojo: errores y operaciones de eliminacion
COLOR_ALERTA = "#f39c12"     # Naranja: alertas y busquedas especiales
COLOR_TEXTO = "#ecf0f1"      # Blanco suave: texto principal
COLOR_TEXTO_SEC = "#bdc3c7"  # Gris claro: texto secundario / etiquetas

# CLASE NODO
# ============================================================
class Nodo:
    """
    Clase que representa un nodo del arbol AVL.
    Guarda los datos del curso y las referencias a hijos.
    """
    def __init__(self, datos):
        # datos es una lista con los campos del CSV
        self.datos = datos
        # Calculamos la satisfaccion segun la formula del laboratorio
        # Este valor sera la clave de ordenamiento del arbol (como la "llave" del BST)
        self.satisfaccion = self.calcular_satisfaccion()
        # Referencias a los subarboles hijo izquierdo y derecho
        # Empiezan en None porque un nodo nuevo es una hoja (sin hijos)
        self.izquierda = None
        self.derecha = None
        # La altura comienza en 1 porque el nodo solo se cuenta a si mismo
        self.altura = 1
    
    def calcular_satisfaccion(self):
        """
        Formula: rating * 0.7 + ((5*positivas + negativas + 3*neutras) / total) * 0.3
        Resultado redondeado a 5 decimales

        La formula combina dos componentes con pesos distintos:
          - 70% viene del rating general del curso (dato directo)
          - 30% viene de una ponderacion de reviews por tipo:
              * Las positivas valen 5 puntos
              * Las negativas valen 1 punto
              * Las neutras valen 3 puntos
            Esto se divide entre el total para normalizarlo.
        """
        try:
    # Los convierte a float para evitar problemas de formato          
            rating = float(self.datos[3])
            positivas = float(self.datos[11])
            negativas = float(self.datos[12])
            neutras = float(self.datos[13])
            total_reviews = float(self.datos[4])
            
            # Solo calculamos si hay al menos una review (evita division por cero)
            if total_reviews > 0:
                valor = rating * 0.7 + ((5 * positivas + negativas + 3 * neutras) / total_reviews) * 0.3
                return round(valor, 5)
            return 0.0
        # tira error si algun campo no es convertible a float, en ese caso retornamos 0.0
        except:
            return 0.0
    
    # Metodos para acceder a los campos facilmente
    # Estos "getters" encapsulan los indices del CSV para no usar numeros magicos en el resto del codigo.
    # Si el CSV cambia de estructura, solo hay que actualizar estos metodos.
    def get_id(self):
        return self.datos[0] if len(self.datos) > 0 else ""
    
    def get_titulo(self):
        return self.datos[1] if len(self.datos) > 1 else ""
    
    def get_rating(self):
        return self.datos[3] if len(self.datos) > 3 else "0"
    
    def get_reviews(self):
        return self.datos[4] if len(self.datos) > 4 else "0"
    
    def get_clases(self):
        return self.datos[5] if len(self.datos) > 5 else "0"
    
    def get_fecha_creacion(self):
        return self.datos[6] if len(self.datos) > 6 else ""
    
    def get_positivas(self):
        return self.datos[11] if len(self.datos) > 11 else "0"
    
    def get_negativas(self):
        return self.datos[12] if len(self.datos) > 12 else "0"
    
    def get_neutras(self):
        return self.datos[13] if len(self.datos) > 13 else "0"


# Funciones de AVL


def obtener_altura(nodo):
    """Devolvemos la altura de un nodo (0 si es None)
    
    Tratamos None como altura 0 para simplificar el codigo, para que no haya que
    verificar si el nodo existe antes de llamar a esta funcion.
    """
    if nodo is None:
        return 0
    return nodo.altura

def actualizar_altura(nodo):
    """Actualizamos la altura de un nodo basado en sus hijos
    
    La altura de un nodo es 1 (el propio nodo) mas la mayor
    altura entre sus dos subarboles. Se llama despues de cada
    insercion o eliminacion para mantener el dato actualizado.
    """
    if nodo is not None:
        alt_izq = obtener_altura(nodo.izquierda)
        alt_der = obtener_altura(nodo.derecha)
        nodo.altura = 1 + max(alt_izq, alt_der)

def obtener_balance(nodo):
    """Calculamos el factor de balance de un nodo usando la convencion derecha - izquierda.

    Restamos la altura del subarbol derecho MENOS la del izquierdo,
    siguiendo la convencion vista en clase:
      - Si el resultado es positivo, el subarbol derecho es mas alto (cargado a la derecha).
      - Si el resultado es negativo, el subarbol izquierdo es mas alto (cargado a la izquierda).
      - Si el resultado es 0, ambos subarboles tienen la misma altura (perfectamente balanceado).

    Un nodo esta en equilibrio AVL si el valor absoluto de este factor es <= 1.
    Retornamos 0 si el nodo es None para evitar errores al llamar la funcion con hojas inexistentes.
    """
    if nodo is None:
        return 0
    # Convencion der - izq: positivo = cargado a la derecha, negativo = cargado a la izquierda
    return obtener_altura(nodo.derecha) - obtener_altura(nodo.izquierda)

def rotacion_derecha(y):
    
    x = y.izquierda
    temp = x.derecha
    
    # Realizar rotacion
    x.derecha = y
    y.izquierda = temp
    
    # Actualizar alturas: primero y (que ahora esta abajo) y luego x (que subio)
    actualizar_altura(y)
    actualizar_altura(x)
    
    # x es ahora la nueva raiz de este subarbol
    return x

def rotacion_izquierda(x):
    
    y = x.derecha
    temp = y.izquierda
    
    # Realizar rotacion
    y.izquierda = x
    x.derecha = temp
    
    # Actualizar alturas: primero x (que ahora esta abajo) y luego y (que subio)
    actualizar_altura(x)
    actualizar_altura(y)
    
    # y es ahora la nueva raiz de este subarbol
    return y

def rotacion_doble_derecha_izquierda(nodo):
    
    # Paso 1: convertimos el subarbol derecho   
    nodo.derecha = rotacion_derecha(nodo.derecha)
    # Paso 2: ahora aplico la rotacion izquierda simple sobre el nodo desbalanceado
    return rotacion_izquierda(nodo)

def rotacion_doble_izquierda_derecha(nodo):
   
    # Paso 1: convierto el subarbol izquierdo de LR a LL
    nodo.izquierda = rotacion_izquierda(nodo.izquierda)
    # Paso 2: ahora aplico la rotacion derecha simple sobre el nodo desbalanceado
    return rotacion_derecha(nodo)

# ============================================================
# FUNCIONES RECURSIVAS REQUERIDAS POR EL LABORATORIO
# ============================================================

def buscar_padre(raiz, nodo):
    """
    Busca el padre de un nodo de forma recursiva.
    Retorna el nodo padre o None si no tiene.

    Estrategia: en cada nodo se verifica si alguno de sus hijos
    directos ES el nodo buscado (usando 'is', no ==, para comparar
    por identidad en memoria y no por valor). Si no, se busca
    recursivamente en ambos subarboles.
    """
    if raiz is None:
        return None
    
    # Verificar si la raiz actual es el padre
    if raiz.izquierda is nodo or raiz.derecha is nodo:
        return raiz
    
    # Buscar en subarbol izquierdo
    padre_izq = buscar_padre(raiz.izquierda, nodo)
    if padre_izq is not None:
        return padre_izq
    
    # Si no se encontro a la izquierda, buscar en el subarbol derecho
    return buscar_padre(raiz.derecha, nodo)

def buscar_abuelo(raiz, nodo):
    """
    Busca el abuelo de un nodo.
    Primero encuentra el padre, luego el padre del padre.

    Reutiliza buscar_padre dos veces: una para encontrar el padre
    directo, y otra para encontrar el padre de ese padre (el abuelo).
    Si el nodo no tiene padre o el padre no tiene padre, retorna None.
    """
    padre = buscar_padre(raiz, nodo)
    if padre is None:
        return None
    return buscar_padre(raiz, padre)

def buscar_tio(raiz, nodo):
    """
    Busca el tio de un nodo (hermano del padre).
    """
    padre = buscar_padre(raiz, nodo)
    if padre is None:
        return None
    
    abuelo = buscar_padre(raiz, padre)
    if abuelo is None:
        return None
    
    # CORRECCIÓN: Comparar por satisfacción en lugar de identidad
    if abuelo.izquierda and abuelo.izquierda.satisfaccion == padre.satisfaccion:
        return abuelo.derecha
    else:
        return abuelo.izquierda

def obtener_nivel(raiz, nodo, nivel_actual=0):
    """
    Obtiene el nivel (profundidad) de un nodo.
    La raiz es nivel 0.

    Recorre el arbol llevando un contador de profundidad.
    Cuando encuentra el nodo buscado (por identidad 'is'),
    retorna el nivel acumulado. Si no lo encuentra en ningun
    subarbol, retorna -1 como señal de "no encontrado".
    """
    if raiz is None:
        return -1
    if raiz is nodo:
        return nivel_actual
    
    # Intentar encontrarlo en el subarbol izquierdo, incrementando el nivel
    nivel_izq = obtener_nivel(raiz.izquierda, nodo, nivel_actual + 1)
    if nivel_izq != -1:
        return nivel_izq
    
    # Si no estaba a la izquierda, buscar en el subarbol derecho
    return obtener_nivel(raiz.derecha, nodo, nivel_actual + 1)

# ============================================================
# CLASE ARBOL AVL
# ============================================================

class ArbolAVL:
    """
    Implementacion del arbol AVL con operaciones basicas.
    Se auto-balancea despues de cada insercion o eliminacion.

    Propiedad clave del AVL: en todo momento, la diferencia de
    alturas entre el subarbol izquierdo y derecho de cualquier
    nodo es a lo sumo 1. Esto garantiza que las operaciones de
    busqueda, insercion y eliminacion son O(log n).
    """
    
    def __init__(self):
        self.raiz = None
        # El dataset actua como un "catalogo" o indice plano del CSV.
        # Permite buscar rapidamente los datos de un curso por su ID
        # sin tener que recorrer el arbol (que esta ordenado por satisfaccion).
        self.dataset = {}
    
    def cargar_dataset(self, ruta_archivo):
        """
        Carga el archivo CSV en memoria.
        Retorna mensaje de exito o error.

        Se lee todo el CSV y se guarda en self.dataset como un
        diccionario {id_curso: fila_completa}. Esto permite insertar
        nodos rapidamente buscando por ID sin releer el archivo.
        """
        try:
            self.dataset.clear()
            with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector)  # saltar encabezado (primera fila con nombres de columna)
                for fila in lector:
                    if fila and len(fila) > 0:
                        # Asegurar que tenga 14 campos rellenando con "0" si faltan
                        # Esto evita IndexError al acceder a columnas opcionales
                        while len(fila) < 14:
                            fila.append("0")
                        self.dataset[fila[0]] = fila
            return True, f"Dataset cargado: {len(self.dataset)} registros"
        except Exception as e:
            return False, f"Error al cargar: {str(e)}"
    
    def insertar(self, id_curso):
        """
        Inserta un nodo por su ID.
        Busca los datos en el dataset y los inserta en el arbol.

        Flujo:
          1. Verificar que el ID exista en el dataset.
          2. Crear el Nodo con los datos del curso (calcula satisfaccion automaticamente).
          3. Verificar que no exista otro nodo con la misma satisfaccion
             (el arbol esta ordenado por satisfaccion, no puede haber duplicados).
          4. Llamar a la insercion recursiva que ademas balancea el arbol.
        """
        if id_curso not in self.dataset:
            return False, f"El ID '{id_curso}' no existe en el dataset"
        
        datos = self.dataset[id_curso]
        nuevo_nodo = Nodo(datos)
        
        # Verificar si ya existe un nodo con esa satisfaccion (claves duplicadas rompen el BST)
        if self._existe_satisfaccion(self.raiz, nuevo_nodo.satisfaccion):
            return False, "Ya existe un curso con esa misma satisfaccion"
        
        self.raiz = self._insertar_recursivo(self.raiz, nuevo_nodo)
        return True, f"Curso '{nuevo_nodo.get_titulo()[:30]}' insertado"
    
    def _existe_satisfaccion(self, nodo, satisfaccion):
        """Verifica si ya existe un nodo con esa satisfaccion
        
        Aprovecha el orden del BST para buscar en O(log n):
        si la satisfaccion buscada es menor que la del nodo actual,
        solo puede estar en el subarbol izquierdo, y viceversa.
        """
        if nodo is None:
            return False
        if nodo.satisfaccion == satisfaccion:
            return True
        if satisfaccion < nodo.satisfaccion:
            return self._existe_satisfaccion(nodo.izquierda, satisfaccion)
        else:
            return self._existe_satisfaccion(nodo.derecha, satisfaccion)
    
    def _insertar_recursivo(self, nodo, nuevo):
        """
        Insercion recursiva con balanceo usando la convencion der - izq.

        Funciona en dos fases:
          FASE 1 - Insercion BST normal:
            Bajo recursivamente por el arbol comparando satisfacciones
            hasta encontrar una posicion vacia (None) donde colocar el nuevo nodo.

          FASE 2 - Rebalanceo en el camino de regreso:
            Al volver de la recursion, actualizo la altura y verifico
            el balance con la formula der - izq. Si el balance supera
            los limites aceptables (> 1 o < -1), aplico la rotacion
            adecuada segun el caso de desbalance detectado.

        Los 4 casos de desbalance con la convencion der - izq
        (balance = altura_derecha - altura_izquierda):

          - Right-Right (RR): balance > 1 y nuevo va al subarbol derecho-derecho
                              -> aplico rotacion izquierda simple.
          - Left-Left   (LL): balance < -1 y nuevo va al subarbol izquierdo-izquierdo
                              -> aplico rotacion derecha simple.
          - Right-Left  (RL): balance > 1 y nuevo va al subarbol derecho-izquierdo
                              -> primero roto a la derecha el hijo derecho, luego roto
                                 a la izquierda el nodo desbalanceado.
          - Left-Right  (LR): balance < -1 y nuevo va al subarbol izquierdo-derecho
                              -> primero roto a la izquierda el hijo izquierdo, luego
                                 roto a la derecha el nodo desbalanceado.
        """
        # Caso base: llegamos a una hoja, aqui va el nuevo nodo
        if nodo is None:
            return nuevo
        
        # Insertar segun valor de satisfaccion (logica de BST)
        if nuevo.satisfaccion < nodo.satisfaccion:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, nuevo)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, nuevo)
        
        # Actualizo la altura del nodo actual al volver de la recursion
        actualizar_altura(nodo)
        
        # Obtengo el factor de balance (der - izq) para detectar desbalance
        balance = obtener_balance(nodo)
        
        # Caso RR: subarbol derecho mas alto Y nuevo fue por la rama derecha-derecha.
        # El balance > 1 confirma que la derecha pesa mas; la satisfaccion del nuevo
        # mayor que la del hijo derecho confirma que bajo por su subarbol derecho.
        # Solucion: una sola rotacion izquierda simple endereza el arbol.
        if balance > 1 and nuevo.satisfaccion > nodo.derecha.satisfaccion:
            return rotacion_izquierda(nodo)
        
        # Caso LL: subarbol izquierdo mas alto Y nuevo fue por la rama izquierda-izquierda.
        # El balance < -1 confirma que la izquierda pesa mas; la satisfaccion del nuevo
        # menor que la del hijo izquierdo confirma que bajo por su subarbol izquierdo.
        # Solucion: una sola rotacion derecha simple endereza el arbol.
        if balance < -1 and nuevo.satisfaccion < nodo.izquierda.satisfaccion:
            return rotacion_derecha(nodo)
        
        # Caso RL: subarbol derecho mas alto PERO nuevo fue por la rama derecha-izquierda.
        # El balance > 1 indica que la derecha pesa mas, pero la satisfaccion del nuevo
        # menor que la del hijo derecho delata que el nuevo bajo hacia la izquierda de ese hijo.
        # Solucion: rotacion doble Derecha-Izquierda (primero roto derecha el hijo, luego
        # roto izquierda el nodo), dejando el peso alineado antes de la rotacion final.
        if balance > 1 and nuevo.satisfaccion < nodo.derecha.satisfaccion:
            return rotacion_doble_derecha_izquierda(nodo)
        
        # Caso LR: subarbol izquierdo mas alto PERO nuevo fue por la rama izquierda-derecha.
        # El balance < -1 indica que la izquierda pesa mas, pero la satisfaccion del nuevo
        # mayor que la del hijo izquierdo delata que el nuevo bajo hacia la derecha de ese hijo.
        # Solucion: rotacion doble Izquierda-Derecha (primero roto izquierda el hijo, luego
        # roto derecha el nodo), dejando el peso alineado antes de la rotacion final.
        if balance < -1 and nuevo.satisfaccion > nodo.izquierda.satisfaccion:
            return rotacion_doble_izquierda_derecha(nodo)
        
        # Si el balance sigue siendo correcto (+-1 o 0), retorno el nodo sin cambios
        return nodo
    
    def eliminar(self, valor, tipo):
        """
        Elimina un nodo por ID o por satisfaccion.
        tipo: "id" o "satis"

        Primero se localiza el nodo a eliminar (para obtener
        su satisfaccion, que es la clave del arbol). Luego se
        llama a la eliminacion recursiva que usa esa clave.
        """
        nodo_a_eliminar = None
        
        if tipo == "id":
            # Busqueda por ID recorre todo el arbol (no aprovecha el orden)
            nodo_a_eliminar = self.buscar_por_id(self.raiz, valor)
        else:  # por satisfaccion
            try:
                sat = float(valor)
                nodo_a_eliminar = self.buscar_por_satisfaccion(self.raiz, sat)
            except:
                return False, "Valor de satisfaccion invalido"
        
        if nodo_a_eliminar is None:
            return False, "Nodo no encontrado"
        
        self.raiz = self._eliminar_recursivo(self.raiz, nodo_a_eliminar.satisfaccion)
        return True, f"Nodo {nodo_a_eliminar.get_id()} eliminado"
    
    def buscar_por_id(self, nodo, id_buscar):
        """Busqueda recursiva por ID (recorre todo el arbol)
        
        Como el arbol esta ordenado por satisfaccion (no por ID),
        no se puede hacer una busqueda BST eficiente por ID.
        Se recorre el arbol completo en preorden hasta encontrarlo.
        Complejidad: O(n) en el peor caso.
        """
        if nodo is None:
            return None
        if nodo.get_id() == id_buscar:
            return nodo
        
        # Buscar en ambos subarboles (no podemos descartar ninguno)
        izq = self.buscar_por_id(nodo.izquierda, id_buscar)
        if izq:
            return izq
        return self.buscar_por_id(nodo.derecha, id_buscar)
    
    def buscar_por_satisfaccion(self, nodo, sat_buscar):
        """Busqueda por satisfaccion (aprovecha el orden del BST)
        
        Al estar el arbol ordenado por satisfaccion, en cada nodo
        podemos descartar la mitad del arbol. Complejidad: O(log n).
        """
        if nodo is None:
            return None
        if nodo.satisfaccion == sat_buscar:
            return nodo
        if sat_buscar < nodo.satisfaccion:
            return self.buscar_por_satisfaccion(nodo.izquierda, sat_buscar)
        else:
            return self.buscar_por_satisfaccion(nodo.derecha, sat_buscar)
    
    def _eliminar_recursivo(self, nodo, satisfaccion):
        """
        Eliminacion recursiva con balanceo usando la convencion der - izq.

        Igual que la insercion, opera en dos fases:

          FASE 1 - Eliminar el nodo (logica BST estandar):
            Hay tres sub-casos segun la cantidad de hijos del nodo encontrado:
              a) Nodo hoja (sin hijos):
                 Simplemente lo elimino retornando None. El padre queda apuntando
                 a None donde antes estaba este nodo.
              b) Nodo con un solo hijo (izquierdo O derecho):
                 Lo reemplazo directamente por su unico hijo. El nodo desaparece
                 y su hijo sube a ocupar su lugar en el arbol.
              c) Nodo con dos hijos:
                 No puedo eliminarlo directamente sin romper el BST. Busco el
                 sucesor en orden (el nodo con la satisfaccion inmediatamente
                 mayor, es decir, el minimo del subarbol derecho). Copio sus
                 datos al nodo actual para reemplazarlo "en sitio", y luego
                 elimino el sucesor de su posicion original en el subarbol
                 derecho (donde siempre es un caso a o b, nunca c).

          FASE 2 - Rebalanceo al volver de la recursion:
            A diferencia de la insercion (donde el nuevo nodo indica el caso),
            en la eliminacion uso obtener_balance() del hijo para confirmar
            hacia que lado esta cargado el subarbol que provoco el desbalance.
            Con la convencion der - izq los cuatro casos son:

            - RR (balance > 1 y balance_hijo_derecho >= 0):
                El subarbol derecho es mas alto Y su hijo derecho tambien lo es
                (o estan igualados). Una rotacion izquierda simple lo corrige.

            - RL (balance > 1 y balance_hijo_derecho < 0):
                El subarbol derecho es mas alto PERO su hijo izquierdo pesa mas.
                El peso esta "doblado hacia adentro": necesito la rotacion doble
                Derecha-Izquierda (roto derecha el hijo derecho, luego izquierda
                el nodo) para alinear el peso antes de corregirlo.

            - LL (balance < -1 y balance_hijo_izquierdo <= 0):
                El subarbol izquierdo es mas alto Y su hijo izquierdo tambien lo es
                (o estan igualados). Una rotacion derecha simple lo corrige.

            - LR (balance < -1 y balance_hijo_izquierdo > 0):
                El subarbol izquierdo es mas alto PERO su hijo derecho pesa mas.
                El peso esta "doblado hacia adentro": necesito la rotacion doble
                Izquierda-Derecha (roto izquierda el hijo izquierdo, luego derecha
                el nodo) para alinear el peso antes de corregirlo.

          Nota importante sobre >= 0 y <= 0 en los casos RR y LL:
            En la eliminacion puede quedar un hijo con balance 0 (ambos subarboles
            iguales) cuando se elimina exactamente el nodo que daba ventaja a uno
            de sus lados. Si no incluyera el caso == 0, ese hijo quedaria sin
            clasificar y el rebalanceo fallaria silenciosamente. Por eso uso >= 0
            para RR y <= 0 para LL en lugar de > 0 y < 0 como en la insercion.
        """
        if nodo is None:
            return None
        
        # Desciendo al nodo correcto segun el orden BST
        if satisfaccion < nodo.satisfaccion:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, satisfaccion)
        elif satisfaccion > nodo.satisfaccion:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, satisfaccion)
        else:
            # Nodo encontrado - aplico uno de los 3 casos de eliminacion

            # Caso a / b (sin hijo izquierdo):
            # Si no hay hijo izquierdo, el hijo derecho sube directamente.
            # Funciona tanto para nodo hoja (derecha = None) como para nodo con un hijo.
            if nodo.izquierda is None:
                return nodo.derecha

            # Caso b (sin hijo derecho):
            # Solo queda el hijo izquierdo, que sube directamente.
            elif nodo.derecha is None:
                return nodo.izquierda
            
            # Caso c (dos hijos):
            # Busco el sucesor: el nodo con la satisfaccion minima en el subarbol derecho.
            # Es el candidato natural para reemplazar al eliminado porque es mayor que todo
            # el subarbol izquierdo y menor que todo el resto del subarbol derecho.
            sucesor = self._minimo(nodo.derecha)
            # Copio los datos del sucesor al nodo actual (el "reemplazo en sitio")
            nodo.datos = sucesor.datos
            nodo.satisfaccion = sucesor.satisfaccion
            # Elimino el sucesor de su posicion en el subarbol derecho.
            # El sucesor es siempre el minimo, asi que no tiene hijo izquierdo
            # -> su eliminacion cae en el caso a o b, nunca en c (no hay recursion infinita).
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.satisfaccion)
        
        # Actualizo la altura al volver de la recursion, ya con el hijo modificado
        actualizar_altura(nodo)
        
        # Calculo el factor de balance (der - izq) para detectar si hay que rotar
        balance = obtener_balance(nodo)
        
        # Caso RR: subarbol derecho mas alto Y su hijo derecho cargado a la derecha (o igual).
        # El >= 0 cubre tambien el caso de hijo balanceado (balance == 0), que puede
        # darse en eliminaciones cuando se remueve el nodo que igualaba las alturas.
        # Solucion: rotacion izquierda simple.
        if balance > 1 and obtener_balance(nodo.derecha) >= 0:
            return rotacion_izquierda(nodo)
        
        # Caso RL: subarbol derecho mas alto PERO su hijo izquierdo pesa mas (balance < 0).
        # Una rotacion izquierda simple empeoraria la situacion porque el peso esta
        # "doblado hacia adentro". Uso la rotacion doble Derecha-Izquierda para
        # alinear primero el subarbol derecho y luego corregir el nodo desbalanceado.
        if balance > 1 and obtener_balance(nodo.derecha) < 0:
            return rotacion_doble_derecha_izquierda(nodo)
        
        # Caso LL: subarbol izquierdo mas alto Y su hijo izquierdo cargado a la izquierda (o igual).
        # El <= 0 cubre tambien el caso de hijo balanceado (balance == 0), mismo razonamiento
        # que en RR pero para el lado izquierdo.
        # Solucion: rotacion derecha simple.
        if balance < -1 and obtener_balance(nodo.izquierda) <= 0:
            return rotacion_derecha(nodo)
        
        # Caso LR: subarbol izquierdo mas alto PERO su hijo derecho pesa mas (balance > 0).
        # Una rotacion derecha simple empeoraria la situacion porque el peso esta
        # "doblado hacia adentro". Uso la rotacion doble Izquierda-Derecha para
        # alinear primero el subarbol izquierdo y luego corregir el nodo desbalanceado.
        if balance < -1 and obtener_balance(nodo.izquierda) > 0:
            return rotacion_doble_izquierda_derecha(nodo)
        
        # Si el balance sigue siendo correcto (+-1 o 0), retorno el nodo sin cambios
        return nodo
    
    def _minimo(self, nodo):
        """Encuentra el nodo con valor minimo en un subarbol
        
        En un BST, el minimo siempre esta en la hoja mas a la izquierda.
        Se recorre hacia la izquierda hasta que no haya mas hijos izquierdos.
        Se usa en la eliminacion para encontrar el sucesor en orden.
        """
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    
    def buscar(self, valor, tipo):
        """Metodo publico para buscar
        
        Delega la busqueda al metodo adecuado segun el tipo indicado.
        Es la interfaz publica que usan los botones de la UI.
        """
        if tipo == "id":
            return self.buscar_por_id(self.raiz, valor)
        else:
            try:
                return self.buscar_por_satisfaccion(self.raiz, float(valor))
            except:
                return None
    
    def recorrido_inorden(self):
        """Retorna lista de nodos en orden
        
        El recorrido inorden de un BST siempre produce los nodos
        ordenados de menor a mayor por su clave (satisfaccion).
        Se usa como base para las busquedas especiales del punto 4,
        que necesitan revisar todos los nodos sin importar el orden del BST.
        """
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado
    
    def _inorden(self, nodo, lista):
        # Patrón recursivo: izquierda -> raiz -> derecha
        # Esto garantiza que los nodos se agregan en orden ascendente de satisfaccion
        if nodo:
            self._inorden(nodo.izquierda, lista)
            lista.append(nodo)
            self._inorden(nodo.derecha, lista)
    
    def recorrido_por_niveles(self):
        """
        Recorrido BFS (por niveles) implementado recursivamente.
        Retorna lista de listas, donde cada sublista es un nivel.

        Normalmente el BFS se implementa con una cola (iterativo),
        pero aqui se implementa recursivamente usando listas como
        cola implicita: en cada llamada se procesa el nivel actual
        y se construye la lista del siguiente nivel para la proxima llamada.
        """
        if self.raiz is None:
            return []
        
        resultado = []
        # Se empieza con una lista que contiene solo la raiz (nivel 0)
        self._bfs_recursivo([self.raiz], resultado)
        return resultado
    
    def _bfs_recursivo(self, nivel_actual, resultado):
        """Funcion auxiliar recursiva para BFS
        
        Recibe la lista de nodos del nivel actual, guarda sus IDs,
        construye la lista de nodos del siguiente nivel (todos los
        hijos de los nodos actuales) y se llama a si misma con ese
        siguiente nivel. La recursion termina cuando no hay mas hijos.
        """
        if not nivel_actual:
            return
        
        # Guardar IDs del nivel actual en el resultado
        ids_nivel = [nodo.get_id() for nodo in nivel_actual]
        resultado.append(ids_nivel)
        
        # Construir la lista del siguiente nivel con todos los hijos
        siguiente_nivel = []
        for nodo in nivel_actual:
            if nodo.izquierda:
                siguiente_nivel.append(nodo.izquierda)
            if nodo.derecha:
                siguiente_nivel.append(nodo.derecha)
        
        # Llamada recursiva con el siguiente nivel (si esta vacio, la recursion termina)
        self._bfs_recursivo(siguiente_nivel, resultado)
    
    def contar_nodos(self):
        """Cuenta total de nodos en el arbol
        
        Reutiliza el recorrido inorden que ya visita todos los nodos.
        Aunque no es la forma mas eficiente (O(n)), es simple y correcta.
        """
        return len(self.recorrido_inorden())
    
    # BUSQUEDAS ESPECIALES (punto 4 del laboratorio)
    # Las 4 busquedas especiales siguen el mismo patron:
    #   1. Obtener todos los nodos con recorrido_inorden()
    #   2. Filtrar con una condicion especifica
    #   3. Retornar la lista de nodos que cumplen la condicion
    # Todas son O(n) porque deben revisar todos los nodos del arbol.
    # ============================================================
    
    def buscar_4a_positivas_mayores(self):
        """
        4a: Reviews positivas > (negativas + neutras)

        Filtra cursos donde las opiniones buenas son mayoria absoluta,
        es decir, superan a todas las opiniones no-positivas juntas.
        """
        resultado = []
        todos = self.recorrido_inorden()
        
        for nodo in todos:
            pos = float(nodo.get_positivas())
            neg = float(nodo.get_negativas())
            neu = float(nodo.get_neutras())
            
            if pos > (neg + neu):
                resultado.append(nodo)
        
        return resultado
    
    def buscar_4b_fecha_posterior(self, fecha_str):
        """
        4b: Fecha de creacion posterior a la dada.
        Formato esperado: YYYY-MM-DD

        Convierte las fechas a objetos datetime para poder compararlas.
        Solo toma los primeros 10 caracteres de la fecha del nodo
        (por si el CSV incluye hora ademas de la fecha).
        """
        try:
            fecha_ref = datetime.strptime(fecha_str, "%Y-%m-%d")
            resultado = []
            todos = self.recorrido_inorden()
            
            for nodo in todos:
                try:
                    # [:10] para tomar solo "YYYY-MM-DD" e ignorar la hora si existe
                    fecha_nodo = datetime.strptime(nodo.get_fecha_creacion()[:10], "%Y-%m-%d")
                    if fecha_nodo > fecha_ref:
                        resultado.append(nodo)
                except:
                    # Si la fecha del nodo no tiene el formato correcto, se omite
                    continue
            
            return resultado
        except:
            # Si la fecha de referencia tiene formato invalido, retornar lista vacia
            return []
    
    def buscar_4c_rango_clases(self, min_clases, max_clases):
        """
        4c: Cantidad de clases dentro de un rango [min, max]

        Filtra cursos cuyo numero de clases este dentro del intervalo
        cerrado [min_clases, max_clases], ambos extremos incluidos.
        """
        resultado = []
        todos = self.recorrido_inorden()
        
        for nodo in todos:
            try:
                clases = int(nodo.get_clases())
                if min_clases <= clases <= max_clases:
                    resultado.append(nodo)
            except:
                # Si el campo no es convertible a int, se omite el nodo
                continue
        
        return resultado
    
    def buscar_4d_sobre_promedio(self, tipo):
        """
        4d: Reviews positivas, negativas o neutras superiores al promedio.
        tipo: "positivas", "negativas" o "neutras"

        Calcula primero el promedio del tipo de review solicitado
        entre todos los nodos del arbol, y luego filtra los que
        superan ese promedio. Se hace en dos pasadas sobre la lista.
        """
        todos = self.recorrido_inorden()
        if not todos:
            return []
        
        # Calcular promedio segun el tipo seleccionado
        if tipo == "positivas":
            valores = [float(n.get_positivas()) for n in todos]
        elif tipo == "negativas":
            valores = [float(n.get_negativas()) for n in todos]
        else:  # neutras
            valores = [float(n.get_neutras()) for n in todos]
        
        promedio = sum(valores) / len(valores)
        
        # Segunda pasada: filtrar los nodos que superan el promedio calculado
        resultado = []
        for nodo in todos:
            if tipo == "positivas":
                valor = float(nodo.get_positivas())
            elif tipo == "negativas":
                valor = float(nodo.get_negativas())
            else:
                valor = float(nodo.get_neutras())
            
            if valor > promedio:
                resultado.append(nodo)
        
        return resultado

# VISUALIZACION CON CANVAS
# ============================================================

class VisualizadorArbol(tk.Canvas):
    """
    Canvas personalizado para dibujar el arbol AVL.
    Usa circulos para nodos y lineas para conexiones.

    Hereda de tk.Canvas, lo que le da acceso directo a todos
    los metodos de dibujo (create_oval, create_line, create_text).
    El arbol se dibuja en tres pasos separados:
      1. Calcular posiciones (x, y) de cada nodo
      2. Dibujar las lineas de conexion (para que queden detras)
      3. Dibujar los circulos de los nodos (encima de las lineas)
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", highlightthickness=1, **kwargs)
        self.arbol = None
        self.nodo_resaltado = None   # ID del nodo a resaltar en amarillo (resultado de busqueda)
        self.posiciones = {}         # Diccionario {id_nodo: (x, y)} con coordenadas de cada nodo
        
        # Configurar la region de scroll para permitir arboles grandes
        self.config(scrollregion=(0, 0, 2000, 1500))
    
    def dibujar_arbol(self, arbol, nodo_resaltado=None):
        """Dibuja el arbol completo
        
        Borra todo lo que habia en el canvas y redibuja desde cero.
        Se llama cada vez que el arbol cambia (insercion, eliminacion)
        o cuando se hace una busqueda que resalta un nodo.
        """
        self.delete("all")   # Limpiar el canvas completamente
        self.arbol = arbol
        self.nodo_resaltado = nodo_resaltado
        self.posiciones = {}
        
        if arbol is None or arbol.raiz is None:
            self.create_text(400, 300, text="Arbol vacio", font=("Arial", 16))
            return
        
        # Paso 1: calcular posiciones (la raiz empieza en el centro-arriba)
        self._calcular_posiciones(arbol.raiz, 400, 50, 200)
        
        # Paso 2: dibujar conexiones primero (para que queden detras de los nodos)
        self._dibujar_conexiones(arbol.raiz)
        
        # Paso 3: dibujar los nodos encima de las lineas
        self._dibujar_nodos(arbol.raiz)
    
    def _calcular_posiciones(self, nodo, x, y, separacion):
        """Calcula las coordenadas de cada nodo
        
        Algoritmo de posicionamiento recursivo:
        - La raiz se coloca en (x=400, y=50)
        - Cada hijo izquierdo se desplaza 'separacion' pixeles a la izquierda
        - Cada hijo derecho se desplaza 'separacion' pixeles a la derecha
        - Todos los hijos bajan 80 pixeles respecto a su padre
        - La separacion se divide a la mitad en cada nivel para que
          los nodos mas profundos no se superpongan
        """
        if nodo is None:
            return
        
        self.posiciones[nodo.get_id()] = (x, y)
        
        # Hijo izquierdo: va a la izquierda y abajo
        if nodo.izquierda:
            self._calcular_posiciones(nodo.izquierda, x - separacion, y + 80, separacion // 2)
        
        # Hijo derecho: va a la derecha y abajo
        if nodo.derecha:
            self._calcular_posiciones(nodo.derecha, x + separacion, y + 80, separacion // 2)
    
    def _dibujar_conexiones(self, nodo):
        """Dibuja las lineas entre nodos
        
        Las lineas conectan el borde inferior del nodo padre (+20 en y)
        con el borde superior del nodo hijo (-20 en y) para que no
        queden tapadas por los circulos.
        """
        if nodo is None or nodo.get_id() not in self.posiciones:
            return
        
        x, y = self.posiciones[nodo.get_id()]
        
        # Linea al hijo izquierdo
        if nodo.izquierda and nodo.izquierda.get_id() in self.posiciones:
            x_izq, y_izq = self.posiciones[nodo.izquierda.get_id()]
            self.create_line(x, y + 20, x_izq, y_izq - 20, fill="#7f8c8d", width=2)
            self._dibujar_conexiones(nodo.izquierda)
        
        # Linea al hijo derecho
        if nodo.derecha and nodo.derecha.get_id() in self.posiciones:
            x_der, y_der = self.posiciones[nodo.derecha.get_id()]
            self.create_line(x, y + 20, x_der, y_der - 20, fill="#7f8c8d", width=2)
            self._dibujar_conexiones(nodo.derecha)
    
    def _dibujar_nodos(self, nodo):
        """Dibuja los circulos de los nodos
        
        El color del circulo indica el estado de balance del nodo:
          - Amarillo: nodo resaltado (resultado de busqueda)
          - Verde:    balance = 0 (perfectamente balanceado)
          - Azul:     balance = +-1 (aceptable para AVL)
          - Rojo:     balance >= +-2 (desbalanceado, no deberia ocurrir en un AVL correcto)
        Dentro del circulo se muestra el ID (truncado a 8 chars) y la satisfaccion (3 decimales).
        """
        if nodo is None or nodo.get_id() not in self.posiciones:
            return
        
        x, y = self.posiciones[nodo.get_id()]
        
        # Determinar color segun balance
        balance = obtener_balance(nodo)
        
        if self.nodo_resaltado == nodo.get_id():
            color_borde = COLOR_ALERTA
            color_relleno = "#fff3cd"
        elif balance == 0:
            color_borde = COLOR_EXITO  # verde = balanceado
            color_relleno = "#d5f4e6"
        elif abs(balance) == 1:
            color_borde = COLOR_BOTON  # azul = casi balanceado
            color_relleno = "#d6eaf8"
        else:
            color_borde = COLOR_ERROR  # rojo = desbalanceado (no deberia pasar en AVL)
            color_relleno = "#fadbd8"
        
        # Dibujar circulo con radio de 25 pixeles
        radio = 25
        self.create_oval(x - radio, y - radio, x + radio, y + radio,
                          fill=color_relleno, outline=color_borde, width=2)
        
        # Dibujar ID (truncado si es muy largo para caber en el circulo)
        id_texto = nodo.get_id()[:8]
        self.create_text(x, y - 5, text=id_texto, font=("Arial", 9, "bold"))
        
        # Dibujar satisfaccion debajo del ID, con fuente mas pequeña
        self.create_text(x, y + 10, text=f"{nodo.satisfaccion:.5f}", 
                        font=("Arial", 7), fill="#555")
        
        # Recursivamente dibujar hijos
        self._dibujar_nodos(nodo.izquierda)
        self._dibujar_nodos(nodo.derecha)

# VENTANA DE INFORMACION DEL NODO
# ============================================================

class VentanaInfo(tk.Toplevel):
    """Ventana emergente que muestra toda la informacion de un curso
    
    Hereda de tk.Toplevel para crear una ventana secundaria independiente
    que no bloquea la ventana principal. Se organiza en dos pestañas:
      - "Datos del Curso": todos los campos del CSV
      - "En el Arbol": relaciones familiares (padre, abuelo, tio) y nivel
    """
    
    def __init__(self, parent, nodo, arbol):
        super().__init__(parent)
        self.title(f"Informacion del Curso - {nodo.get_id()}")
        self.geometry("550x500")
        self.configure(bg=COLOR_PANEL)
        self.resizable(True, True)
        
        # Frame principal
        frame = tk.Frame(self, bg=COLOR_PANEL)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Titulo del curso (en la parte superior, fuera de las pestañas)
        lbl_titulo = tk.Label(frame, text=nodo.get_titulo(), 
                             font=("Arial", 12, "bold"),
                             bg=COLOR_PANEL, fg=COLOR_BOTON, wraplength=500)
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        # Notebook (contenedor de pestañas de tkinter)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # Pestaña 1: Datos del curso
        tab1 = tk.Frame(notebook, bg=COLOR_TARJETA)
        notebook.add(tab1, text="Datos del Curso")
        
        # Lista de tuplas (etiqueta, valor) para mostrar los datos del curso
        campos = [
            ("ID:", nodo.get_id()),
            ("Satisfaccion:", f"{nodo.satisfaccion:.5f}"),
            ("Rating:", nodo.get_rating()),
            ("Total Reviews:", nodo.get_reviews()),
            ("Reviews Positivas:", nodo.get_positivas()),
            ("Reviews Negativas:", nodo.get_negativas()),
            ("Reviews Neutras:", nodo.get_neutras()),
            ("Numero de Clases:", nodo.get_clases()),
            ("Fecha Creacion:", nodo.get_fecha_creacion()),
            ("Instructor ID:", nodo.datos[9] if len(nodo.datos) > 9 else ""),
            ("URL:", nodo.datos[2] if len(nodo.datos) > 2 else ""),
        ]
        
        # Crear filas alternando colores para mejorar la legibilidad
        for i, (etiqueta, valor) in enumerate(campos):
            fila = tk.Frame(tab1, bg=COLOR_TARJETA if i % 2 == 0 else COLOR_PANEL)
            fila.pack(fill="x")
            tk.Label(fila, text=etiqueta, width=15, anchor="e",
                    bg=fila["bg"], fg=COLOR_TEXTO_SEC).pack(side="left", padx=5, pady=3)
            tk.Label(fila, text=valor, anchor="w",
                    bg=fila["bg"], fg=COLOR_TEXTO).pack(side="left", padx=5, pady=3)
        
        # Pestaña 2: Informacion del Arbol
        tab2 = tk.Frame(notebook, bg=COLOR_TARJETA)
        notebook.add(tab2, text="En el Arbol")
        
        # Calcular las relaciones del nodo usando las funciones recursivas del laboratorio
        padre = buscar_padre(arbol.raiz, nodo)
        abuelo = buscar_abuelo(arbol.raiz, nodo)
        tio = buscar_tio(arbol.raiz, nodo)
        nivel = obtener_nivel(arbol.raiz, nodo)
        balance = obtener_balance(nodo)
        
        info_arbol = [
            ("Nivel en el arbol:", str(nivel)),
            ("Factor de Balance:", str(balance)),
            ("Padre:", f"{padre.get_id()} - {padre.get_titulo()[:30]}" if padre else "No tiene (es la raiz)"),
            ("Abuelo:", f"{abuelo.get_id()} - {abuelo.get_titulo()[:30]}" if abuelo else "No tiene abuelo"),
            ("Tio:", f"{tio.get_id()} - {tio.get_titulo()[:30]}" if tio else "No tiene tio"),
        ]
        
        for i, (etiqueta, valor) in enumerate(info_arbol):
            fila = tk.Frame(tab2, bg=COLOR_TARJETA if i % 2 == 0 else COLOR_PANEL)
            fila.pack(fill="x")
            tk.Label(fila, text=etiqueta, width=15, anchor="e",
                    bg=fila["bg"], fg=COLOR_TEXTO_SEC).pack(side="left", padx=5, pady=5)
            tk.Label(fila, text=valor, anchor="w",
                    bg=fila["bg"], fg=COLOR_TEXTO).pack(side="left", padx=5, pady=5)
        
        # Boton cerrar
        btn_cerrar = tk.Button(frame, text="Cerrar", command=self.destroy,
                              bg=COLOR_BOTON, fg="white", width=15)
        btn_cerrar.pack(pady=15)

# VENTANA DE RESULTADOS DE BUSQUEDA
# ============================================================

class VentanaResultados(tk.Toplevel):
    """Muestra los resultados de busqueda avanzada en una tabla
    
    Usa ttk.Treeview como componente de tabla para mostrar multiples
    resultados de las busquedas especiales (4a, 4b, 4c, 4d).
    Permite hacer doble clic en una fila para ver la info completa del curso.
    """
    
    def __init__(self, parent, nodos, arbol, titulo="Resultados"):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("700x400")
        self.configure(bg=COLOR_PANEL)
        
        self.arbol = arbol
        # Convertir la lista a diccionario para poder acceder rapidamente
        # al nodo completo desde el ID que devuelve el Treeview al hacer clic
        self.nodos = {n.get_id(): n for n in nodos}
        
        # Header con titulo y contador de resultados
        header = tk.Frame(self, bg=COLOR_PANEL)
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text=titulo, font=("Arial", 11, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(side="left")
        tk.Label(header, text=f"  ({len(nodos)} resultados)",
                bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC).pack(side="left")
        
        # Tabla (Treeview de tkinter, equivalente a una tabla HTML)
        columnas = ("id", "titulo", "satisfaccion", "rating", "reviews", "clases")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        
        # Configurar encabezados y anchos de columna
        self.tabla.heading("id", text="ID")
        self.tabla.heading("titulo", text="Titulo")
        self.tabla.heading("satisfaccion", text="Satisfaccion")
        self.tabla.heading("rating", text="Rating")
        self.tabla.heading("reviews", text="Reviews")
        self.tabla.heading("clases", text="Clases")
        
        self.tabla.column("id", width=80, anchor="center")
        self.tabla.column("titulo", width=250, anchor="w")
        self.tabla.column("satisfaccion", width=100, anchor="center")
        self.tabla.column("rating", width=70, anchor="center")
        self.tabla.column("reviews", width=70, anchor="center")
        self.tabla.column("clases", width=60, anchor="center")
        
        # Scrollbar vertical vinculada al Treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="left", fill="y", pady=10, padx=(0, 10))
        
        # Insertar cada nodo como una fila en la tabla
        # iid=nodo.get_id() permite identificar la fila por el ID del curso al hacer clic
        for nodo in nodos:
            self.tabla.insert("", "end", iid=nodo.get_id(), values=(
                nodo.get_id(),
                nodo.get_titulo()[:40],
                f"{nodo.satisfaccion:.5f}",
                nodo.get_rating(),
                nodo.get_reviews(),
                nodo.get_clases()
            ))
        
        # Vincular el evento de doble clic a la funcion que abre la ventana de info
        self.tabla.bind("<Double-1>", self._mostrar_info)
        
        # Label de instruccion para el usuario
        tk.Label(self, text="Doble clic en una fila para ver informacion completa",
                bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC, font=("Arial", 9)).pack(pady=(0, 10))
    
    def _mostrar_info(self, event):
        """Abre ventana de info al hacer doble clic
        
        Obtiene el ID de la fila seleccionada en el Treeview,
        busca el nodo en el diccionario self.nodos y abre VentanaInfo.
        """
        seleccion = self.tabla.selection()
        if seleccion:
            nodo_id = seleccion[0]
            if nodo_id in self.nodos:
                VentanaInfo(self, self.nodos[nodo_id], self.arbol)

# APLICACION PRINCIPAL
# ============================================================

class AplicacionAVL(tk.Tk):
    """Ventana principal de la aplicacion
    
    Hereda de tk.Tk para ser la ventana raiz del programa.
    Organiza la interfaz en tres paneles horizontales:
      - Panel izquierdo:  controles de operaciones (insertar, eliminar, buscar)
      - Panel central:    visualizacion grafica del arbol (canvas)
      - Panel derecho:    busquedas especiales y log de operaciones
    """
    
    def __init__(self):
        super().__init__()
        self.title("Laboratorio 1 - Arbol AVL (Cursos Udemy)")
        self.geometry("1200x750")
        self.configure(bg=COLOR_FONDO)
        
        # Inicializar arbol (empieza vacio, sin dataset cargado)
        self.arbol = ArbolAVL()
        
        # Construir los tres paneles de la interfaz
        self._crear_menu()
        self._crear_panel_izquierdo()
        self._crear_panel_central()
        self._crear_panel_derecho()

        # Mensaje inicial en el log para orientar al usuario
        self._log("Sistema iniciado. Cargue un dataset para comenzar.")
    
    def _crear_menu(self):
        """Crea la barra de menu
        
        Crea un menu estandar de tkinter con dos entradas:
          - Archivo: para cargar el CSV y salir
          - Ayuda: para mostrar informacion del programa
        """
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Cargar Dataset", command=self._cargar_dataset)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)
        
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self._acerca_de)
    
    def _crear_panel_izquierdo(self):
        """Panel con controles de operaciones
        
        Ancho fijo de 300px que no crece aunque la ventana se expanda.
        pack_propagate(False) evita que el frame se redimensione segun su contenido.
        Contiene cuatro secciones separadas visualmente: Dataset, Insertar, Eliminar, Buscar.
        """
        panel = tk.Frame(self, bg=COLOR_PANEL, width=300)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        panel.pack_propagate(False)
        
        # Titulo
        tk.Label(panel, text="Operaciones", font=("Arial", 12, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(pady=10)
        
        # === SECCION DATASET ===
        self._crear_seccion(panel, "Dataset")
        tk.Button(panel, text="Cargar CSV", command=self._cargar_dataset,
                 bg=COLOR_BOTON, fg="white", width=25).pack(pady=5)
        # Label que muestra el nombre del archivo cargado y la cantidad de registros
        self.lbl_dataset = tk.Label(panel, text="Sin dataset cargado",
                                   bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC, wraplength=280)
        self.lbl_dataset.pack(pady=5)
        
        # === SECCION INSERTAR ===
        self._crear_seccion(panel, "Insertar Nodo")
        tk.Label(panel, text="ID del curso:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=20)
        self.entry_insertar = tk.Entry(panel, width=30)
        self.entry_insertar.pack(pady=5)
        tk.Button(panel, text="Insertar", command=self._insertar,
                 bg=COLOR_EXITO, fg="white", width=25).pack(pady=5)
        
        # Insertar multiples: campo de texto con IDs separados por coma
        tk.Label(panel, text="IDs separados por coma:", bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC).pack(anchor="w", padx=20, pady=(10,0))
        self.entry_multi = tk.Text(panel, height=3, width=30)
        self.entry_multi.pack(pady=5)
        tk.Button(panel, text="Insertar Multiples", command=self._insertar_multi,
                 bg=COLOR_EXITO, fg="white", width=25).pack(pady=5)
        
        # Insertar aleatorios: selecciona N cursos al azar del dataset
        frame_rand = tk.Frame(panel, bg=COLOR_PANEL)
        frame_rand.pack(pady=5)
        tk.Label(frame_rand, text="Cantidad:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left")
        self.entry_rand = tk.Entry(frame_rand, width=5)
        self.entry_rand.insert(0, "5")
        self.entry_rand.pack(side="left", padx=5)
        tk.Button(frame_rand, text="Aleatorios", command=self._insertar_random,
                 bg=COLOR_EXITO, fg="white").pack(side="left")
        
        # === SECCION ELIMINAR ===
        self._crear_seccion(panel, "Eliminar Nodo")
        tk.Label(panel, text="Valor a eliminar:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=20)
        self.entry_eliminar = tk.Entry(panel, width=30)
        self.entry_eliminar.pack(pady=5)
        
        # Radio buttons para elegir si se busca por ID o por valor de satisfaccion
        self.tipo_eliminar = tk.StringVar(value="id")
        tk.Radiobutton(panel, text="Por ID", variable=self.tipo_eliminar, 
                      value="id", bg=COLOR_PANEL, fg=COLOR_TEXTO,
                      selectcolor=COLOR_TARJETA).pack(anchor="w", padx=20)
        tk.Radiobutton(panel, text="Por Satisfaccion", variable=self.tipo_eliminar,
                      value="satis", bg=COLOR_PANEL, fg=COLOR_TEXTO,
                      selectcolor=COLOR_TARJETA).pack(anchor="w", padx=20)
        
        tk.Button(panel, text="Eliminar", command=self._eliminar,
                 bg=COLOR_ERROR, fg="white", width=25).pack(pady=5)
        
        # === SECCION BUSCAR ===
        self._crear_seccion(panel, "Buscar Nodo")
        tk.Label(panel, text="Valor a buscar:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=20)
        self.entry_buscar = tk.Entry(panel, width=30)
        self.entry_buscar.pack(pady=5)
        
        # Radio buttons para elegir tipo de busqueda
        self.tipo_buscar = tk.StringVar(value="id")
        tk.Radiobutton(panel, text="Por ID", variable=self.tipo_buscar,
                      value="id", bg=COLOR_PANEL, fg=COLOR_TEXTO,
                      selectcolor=COLOR_TARJETA).pack(anchor="w", padx=20)
        tk.Radiobutton(panel, text="Por Satisfaccion", variable=self.tipo_buscar,
                      value="satis", bg=COLOR_PANEL, fg=COLOR_TEXTO,
                      selectcolor=COLOR_TARJETA).pack(anchor="w", padx=20)
        
        tk.Button(panel, text="Buscar", command=self._buscar,
                 bg=COLOR_BOTON, fg="white", width=25).pack(pady=5)
    
    def _crear_panel_central(self):
        """Panel con la visualizacion del arbol
        
        Ocupa todo el espacio disponible entre los dos paneles laterales
        gracias a fill="both" y expand=True. Contiene el canvas con
        scrollbars horizontal y vertical para arboles grandes.
        """
        panel = tk.Frame(self, bg=COLOR_FONDO)
        panel.pack(side="left", fill="both", expand=True, pady=10)
        
        # Header con titulo y contador de nodos
        header = tk.Frame(panel, bg=COLOR_FONDO)
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="Visualizacion del Arbol AVL", 
                font=("Arial", 11, "bold"),
                bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left")
        # Este label se actualiza cada vez que cambia el arbol
        self.lbl_contador = tk.Label(header, text="Nodos: 0",
                                    bg=COLOR_FONDO, fg=COLOR_EXITO)
        self.lbl_contador.pack(side="right")
        
        # Canvas con scrollbars (usa grid para poder tener scrollbars en dos ejes)
        frame_canvas = tk.Frame(panel, bg="white")
        frame_canvas.pack(fill="both", expand=True, padx=10, pady=5)
        
        # El canvas es una instancia de VisualizadorArbol (subclase de tk.Canvas)
        self.canvas = VisualizadorArbol(frame_canvas, width=800, height=600)
        hbar = ttk.Scrollbar(frame_canvas, orient="horizontal", command=self.canvas.xview)
        vbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
        # Usar grid para colocar canvas y scrollbars correctamente
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="ew")
        
        # Permitir que la celda del canvas crezca con la ventana
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
    
    def _crear_panel_derecho(self):
        """Panel con busquedas especiales y log
        
        Ancho fijo de 300px igual que el panel izquierdo.
        Contiene los 4 botones de busqueda especial del laboratorio,
        el boton de recorrido por niveles y el log de operaciones.
        """
        panel = tk.Frame(self, bg=COLOR_PANEL, width=300)
        panel.pack(side="right", fill="y", padx=10, pady=10)
        panel.pack_propagate(False)
        
        # Titulo
        tk.Label(panel, text="Busquedas Especiales", font=("Arial", 12, "bold"),
                bg=COLOR_PANEL, fg=COLOR_ALERTA).pack(pady=10)
        
        # 4a: buscar cursos donde positivas > negativas + neutras
        tk.Button(panel, text="4a) Positivas > Neg + Neutras",
                 command=self._buscar_4a, bg="#9b59b6", fg="white",
                 width=30).pack(pady=5)
        
        # 4b: buscar cursos creados despues de una fecha dada
        tk.Label(panel, text="4b) Fecha posterior a (AAAA-MM-DD):",
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10,0))
        self.entry_fecha = tk.Entry(panel, width=15)
        self.entry_fecha.insert(0, "2020-01-01")
        self.entry_fecha.pack(pady=5)
        tk.Button(panel, text="Buscar por Fecha", command=self._buscar_4b,
                 bg="#9b59b6", fg="white", width=30).pack(pady=5)
        # Crea un encabezado o contenedor visual llamado "Relaciones Familiares" dentro del panel lateral
        self._crear_seccion(panel, "Relaciones Familiares")
        # Etiqueta informativa para indicar al usuario que debe ingresar un ID
        tk.Label(panel, text="ID del nodo:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10)
        # Campo de entrada para que el usuario ingrese el ID del nodo del cual quiere buscar las relaciones familiares
        self.entry_familia = tk.Entry(panel, width=30)
        self.entry_familia.pack(pady=5)
        # Botones para buscar el padre, abuelo y tio del nodo ingresado
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=5)
        # Cada boton llama a una funcion diferente que realiza la busqueda correspondiente y muestra los resultados en el log o en ventanas emergentes
        tk.Button(btn_frame, text="Buscar Padre", command=self._buscar_padre_ui,
                 bg=COLOR_BOTON, fg="white", width=12).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Buscar Abuelo", command=self._buscar_abuelo_ui,
                 bg=COLOR_BOTON, fg="white", width=12).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Buscar Tío", command=self._buscar_tio_ui,
                 bg=COLOR_BOTON, fg="white", width=12).pack(side="left", padx=2)
        
        # 4c: buscar cursos con numero de clases en un rango [min, max]
        frame_rango = tk.Frame(panel, bg=COLOR_PANEL)
        frame_rango.pack(pady=5)
        tk.Label(frame_rango, text="Min:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left")
        self.entry_min = tk.Entry(frame_rango, width=6)
        self.entry_min.insert(0, "10")
        self.entry_min.pack(side="left", padx=3)
        tk.Label(frame_rango, text="Max:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left")
        self.entry_max = tk.Entry(frame_rango, width=6)
        self.entry_max.insert(0, "50")
        self.entry_max.pack(side="left", padx=3)
        tk.Button(panel, text="4c) Buscar por Rango de Clases",
                 command=self._buscar_4c, bg="#9b59b6", fg="white",
                 width=30).pack(pady=5)
        
        # 4d: buscar cursos con un tipo de review por encima del promedio del arbol
        tk.Label(panel, text="4d) Tipo de reviews sobre promedio:",
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10,0))
        # Combobox (dropdown) para elegir el tipo de review
        self.combo_tipo = ttk.Combobox(panel, values=["positivas", "negativas", "neutras"],
                                       width=15, state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=5)
        tk.Button(panel, text="Buscar sobre Promedio", command=self._buscar_4d,
                 bg="#9b59b6", fg="white", width=30).pack(pady=5)
        
        # Boton para mostrar el recorrido BFS por niveles en ventana separada
        self._crear_seccion(panel, "Recorrido")
        tk.Button(panel, text="Mostrar Recorrido por Niveles",
                 command=self._mostrar_recorrido, bg=COLOR_ALERTA, fg="white",
                 width=30).pack(pady=5)
        
        # Area de log: muestra el historial de operaciones con marca de tiempo
        self._crear_seccion(panel, "Registro de Operaciones")
        # ScrolledText combina Text con Scrollbar vertical en un solo widget
        self.txt_log = scrolledtext.ScrolledText(panel, width=35, height=12,
                                                bg=COLOR_TARJETA, fg=COLOR_TEXTO)
        self.txt_log.pack(padx=5, pady=5)
        # Deshabilitado para que el usuario no pueda escribir en el log
        self.txt_log.configure(state="disabled")
    
    def _crear_seccion(self, parent, titulo):
        """Crea un separador visual con titulo
        
        Patron reutilizable para separar visualmente las secciones
        dentro de un panel. Consiste en una linea horizontal (Frame
        de 2px de alto) y un Label con el titulo de la seccion.
        """
        tk.Frame(parent, bg=COLOR_BORDE, height=2).pack(fill="x", padx=10, pady=15)
        tk.Label(parent, text=titulo, font=("Arial", 10, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(anchor="w", padx=10)
    
    def _log(self, mensaje, tipo="info"):
        """Agrega mensaje al log
        
        Habilita el widget temporalmente para insertar el texto,
        lo colorea segun el tipo (info/exito/error), y lo deshabilita
        de nuevo. Luego hace scroll hasta el final para que el ultimo
        mensaje sea siempre visible.
        """
        self.txt_log.configure(state="normal")
        import datetime
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Configurar colores segun el tipo de mensaje
        if tipo == "error":
            tag = "error"
            self.txt_log.tag_configure("error", foreground=COLOR_ERROR)
        elif tipo == "exito":
            tag = "exito"
            self.txt_log.tag_configure("exito", foreground=COLOR_EXITO)
        else:
            tag = "info"
            self.txt_log.tag_configure("info", foreground=COLOR_TEXTO)
        
        self.txt_log.insert("end", f"[{hora}] {mensaje}\\n", tag)
        self.txt_log.see("end")   # Hacer scroll hasta el ultimo mensaje
        self.txt_log.configure(state="disabled")
    
    def _actualizar_vista(self, resaltar_id=None):
        """Redibuja el arbol y actualiza contadores
        
        Se llama despues de cualquier operacion que modifique el arbol
        (insertar, eliminar) o que necesite resaltar un nodo (buscar).
        El parametro resaltar_id indica que nodo pintar en amarillo.
        """
        self.canvas.dibujar_arbol(self.arbol, resaltar_id)
        self.lbl_contador.configure(text=f"Nodos: {self.arbol.contar_nodos()}")
    
    # ACCIONES DE LOS BOTONES
    # Cada metodo _accion() valida la entrada, llama al metodo
    # correspondiente del arbol, registra el resultado en el log
    # y actualiza la visualizacion si es necesario.
    # ============================================================
    
    def _cargar_dataset(self):
        """Carga el archivo CSV
        
        Abre un dialogo de seleccion de archivo filtrado por .csv.
        Si el usuario selecciona un archivo, lo carga en el arbol
        y actualiza el label con el nombre del archivo y el conteo.
        """
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")]
        )
        if ruta:
            exito, mensaje = self.arbol.cargar_dataset(ruta)
            if exito:
                nombre = os.path.basename(ruta)
                self.lbl_dataset.configure(text=f"{nombre}\\n{mensaje}")
                self._log(mensaje, "exito")
            else:
                self._log(mensaje, "error")
    
    def _insertar(self):
        """Inserta un solo nodo
        
        Lee el ID del campo de entrada, llama a insertar() del arbol,
        y si tiene exito limpia el campo y redibuja el arbol resaltando
        el nodo recien insertado.
        """
        id_curso = self.entry_insertar.get().strip()
        if not id_curso:
            self._log("Ingrese un ID", "error")
            return
        
        exito, mensaje = self.arbol.insertar(id_curso)
        if exito:
            self._log(mensaje, "exito")
            self.entry_insertar.delete(0, "end")
            self._actualizar_vista(id_curso)
        else:
            self._log(mensaje, "error")
    
    def _insertar_multi(self):
        """Inserta multiples nodos
        
        Lee el contenido del widget Text, separa por comas,
        e intenta insertar cada ID. Reporta cuantos se insertaron
        exitosamente vs cuantos fallaron.
        """
        texto = self.entry_multi.get("1.0", "end").strip()
        if not texto:
            self._log("Ingrese al menos un ID", "error")
            return
        
        ids = [i.strip() for i in texto.split(",") if i.strip()]
        exitosos = 0
        
        for id_curso in ids:
            exito, mensaje = self.arbol.insertar(id_curso)
            if exito:
                exitosos += 1
            else:
                self._log(f"{id_curso}: {mensaje}", "error")
        
        self._log(f"Insertados {exitosos} de {len(ids)} nodos", "exito")
        self.entry_multi.delete("1.0", "end")
        self._actualizar_vista()
    
    def _insertar_random(self):
        """Inserta nodos aleatorios del dataset
        
        Usa random.sample para seleccionar IDs unicos al azar del dataset.
        Si se pide mas de los disponibles, inserta todos los disponibles.
        Util para poblar rapidamente el arbol al probar la aplicacion.
        """
        if not self.arbol.dataset:
            self._log("Cargue un dataset primero", "error")
            return
        
        try:
            cantidad = int(self.entry_rand.get())
        except:
            cantidad = 5
        
        ids_disponibles = list(self.arbol.dataset.keys())
        # No pedir mas de los que hay disponibles
        if cantidad > len(ids_disponibles):
            cantidad = len(ids_disponibles)
        
        seleccionados = random.sample(ids_disponibles, cantidad)
        exitosos = 0
        
        for id_curso in seleccionados:
            exito, _ = self.arbol.insertar(id_curso)
            if exito:
                exitosos += 1
        
        self._log(f"Insertados {exitosos} nodos aleatorios", "exito")
        self._actualizar_vista()
    
    def _eliminar(self):
        """Elimina un nodo
        
        Lee el valor del campo de entrada y el tipo (ID o satisfaccion)
        del radio button, llama a eliminar() y actualiza la vista.
        """
        valor = self.entry_eliminar.get().strip()
        if not valor:
            self._log("Ingrese un valor", "error")
            return
        
        tipo = self.tipo_eliminar.get()
        exito, mensaje = self.arbol.eliminar(valor, tipo)
        
        if exito:
            self._log(mensaje, "exito")
            self.entry_eliminar.delete(0, "end")
            self._actualizar_vista()
        else:
            self._log(mensaje, "error")
    
    def _buscar(self):
        """Busca un nodo y muestra su info
        
        Si encuentra el nodo, redibuja el arbol resaltandolo en amarillo
        y abre VentanaInfo con todos sus datos y relaciones en el arbol.
        """
        valor = self.entry_buscar.get().strip()
        if not valor:
            self._log("Ingrese un valor", "error")
            return
        
        tipo = self.tipo_buscar.get()
        nodo = self.arbol.buscar(valor, tipo)
        
        if nodo:
            self._log(f"Encontrado: {nodo.get_titulo()[:40]}", "exito")
            self._actualizar_vista(nodo.get_id())
            VentanaInfo(self, nodo, self.arbol)
            self.entry_buscar.delete(0, "end")
        else:
            self._log("Nodo no encontrado", "error")
    
    def _buscar_4a(self):
        """Busqueda 4a: positivas > negativas + neutras"""
        resultados = self.arbol.buscar_4a_positivas_mayores()
        self._log(f"4a: {len(resultados)} cursos cumplen el criterio")
        if resultados:
            VentanaResultados(self, resultados, self.arbol, 
                            "4a - Positivas > (Negativas + Neutras)")
    
    def _buscar_4b(self):
        """Busqueda 4b: fecha posterior
        
        Lee la fecha del campo de entrada y llama al metodo del arbol.
        Si no hay resultados, solo registra en el log sin abrir ventana.
        """
        fecha = self.entry_fecha.get().strip()
        resultados = self.arbol.buscar_4b_fecha_posterior(fecha)
        self._log(f"4b: {len(resultados)} cursos despues de {fecha}")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4b - Creados despues de {fecha}")
    
    def _buscar_4c(self):
        """Busqueda 4c: rango de clases
        
        Lee min y max de sus respectivos Entry, valida que sean enteros
        y llama al metodo del arbol con esos limites.
        """
        try:
            min_c = int(self.entry_min.get())
            max_c = int(self.entry_max.get())
        except:
            self._log("Rango invalido", "error")
            return
        
        resultados = self.arbol.buscar_4c_rango_clases(min_c, max_c)
        self._log(f"4c: {len(resultados)} cursos entre {min_c} y {max_c} clases")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4c - Entre {min_c} y {max_c} clases")
    
    def _buscar_4d(self):
        """Busqueda 4d: sobre promedio
        
        Lee el tipo de review del Combobox y llama al metodo del arbol.
        """
        tipo = self.combo_tipo.get()
        resultados = self.arbol.buscar_4d_sobre_promedio(tipo)
        self._log(f"4d: {len(resultados)} cursos con {tipo} sobre promedio")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4d - {tipo.capitalize()} sobre promedio")
    
    def _mostrar_recorrido(self):
        """Muestra ventana con recorrido por niveles
        
        Llama a recorrido_por_niveles() que implementa el BFS recursivo
        y muestra los IDs de cada nivel en un ScrolledText.
        El formato es: "Nivel 0:  id1  -  id2  -  ..."
        """
        niveles = self.arbol.recorrido_por_niveles()
        if not niveles:
            self._log("Arbol vacio", "error")
            return
        
        ventana = tk.Toplevel(self)
        ventana.title("Recorrido por Niveles (BFS Recursivo)")
        ventana.geometry("500x400")
        ventana.configure(bg=COLOR_PANEL)
        
        tk.Label(ventana, text="Recorrido por Niveles - BFS Recursivo",
                font=("Arial", 12, "bold"), bg=COLOR_PANEL, fg=COLOR_BOTON).pack(pady=10)
        
        txt = scrolledtext.ScrolledText(ventana, width=60, height=20,
                                       bg=COLOR_TARJETA, fg=COLOR_TEXTO)
        txt.pack(padx=10, pady=10)
        
        # Mostrar cada nivel en una linea separada con sus IDs unidos por " - "
        for i, nivel in enumerate(niveles):
            txt.insert("end", f"Nivel {i}:  ")
            txt.insert("end", "  -  ".join(nivel) + "\\n\\n")
        
        txt.configure(state="disabled")
        
        total_nodos = sum(len(n) for n in niveles)
        self._log(f"Recorrido: {len(niveles)} niveles, {total_nodos} nodos")
    
    def _acerca_de(self):
        """Muestra informacion del programa"""
        messagebox.showinfo("Acerca de",
            "Laboratorio 1 - Estructura de Datos II\\n"
            "Universidad del Norte\\n\\n"
            "Arbol AVL para gestion de cursos Udemy\\n"
            "Implementado con Python y tkinter")
    def _buscar_padre_ui(self):
        """Busca y muestra el padre de un nodo"""
        id_nodo = self.entry_familia.get().strip()
        if not id_nodo:
            self._log("Ingrese un ID de nodo", "error")
            return
        
        # Buscar el nodo en el árbol por ID
        nodo = self.arbol.buscar_por_id(self.arbol.raiz, id_nodo)
        if nodo is None:
            self._log(f"Nodo '{id_nodo}' no encontrado en el árbol", "error")
            return
        
        # Buscar su padre
        padre = buscar_padre(self.arbol.raiz, nodo)
        
        if padre:
            self._log(f"Padre de {id_nodo}: {padre.get_id()} - {padre.get_titulo()[:30]}", "exito")
            self._actualizar_vista(padre.get_id())  # Resaltar padre en amarillo
            VentanaInfo(self, padre, self.arbol)
        else:
            self._log(f"El nodo {id_nodo} es la RAÍZ (no tiene padre)", "alerta")
            messagebox.showinfo("Sin Padre", f"El nodo '{id_nodo}' es la raíz del árbol.")
    
    def _buscar_abuelo_ui(self):
        """Busca y muestra el abuelo de un nodo"""
        id_nodo = self.entry_familia.get().strip()
        if not id_nodo:
            self._log("Ingrese un ID de nodo", "error")
            return
        
        nodo = self.arbol.buscar_por_id(self.arbol.raiz, id_nodo)
        if nodo is None:
            self._log(f"Nodo '{id_nodo}' no encontrado en el árbol", "error")
            return
        
        # Buscar su abuelo
        abuelo = buscar_abuelo(self.arbol.raiz, nodo)
        
        if abuelo:
            self._log(f"Abuelo de {id_nodo}: {abuelo.get_id()} - {abuelo.get_titulo()[:30]}", "exito")
            self._actualizar_vista(abuelo.get_id())
            VentanaInfo(self, abuelo, self.arbol)
        else:
            self._log(f"El nodo {id_nodo} no tiene abuelo (está en nivel 0 o 1)", "alerta")
            messagebox.showinfo("Sin Abuelo", 
                              f"El nodo '{id_nodo}' no tiene abuelo.\n"
                              f"Nivel: {obtener_nivel(self.arbol.raiz, nodo)}")
    
    def _buscar_tio_ui(self):
        """Busca y muestra el tío de un nodo"""
        id_nodo = self.entry_familia.get().strip()
        if not id_nodo:
            self._log("Ingrese un ID de nodo", "error")
            return
        
        nodo = self.arbol.buscar_por_id(self.arbol.raiz, id_nodo)
        if nodo is None:
            self._log(f"Nodo '{id_nodo}' no encontrado en el árbol", "error")
            return
        
        # Buscar su tío
        tio = buscar_tio(self.arbol.raiz, nodo)
        
        if tio:
            self._log(f"Tío de {id_nodo}: {tio.get_id()} - {tio.get_titulo()[:30]}", "exito")
            self._actualizar_vista(tio.get_id())
            VentanaInfo(self, tio, self.arbol)
        else:
            padre = buscar_padre(self.arbol.raiz, nodo)
            if padre is None:
                msg = "El nodo es la raíz (no tiene padre, ni abuelo, ni tío)"
            else:
                abuelo = buscar_abuelo(self.arbol.raiz, nodo)
                if abuelo is None:
                    msg = "El padre del nodo es la raíz (no tiene abuelo, por tanto no tiene tío)"
                else:
                    msg = "El abuelo solo tiene un hijo (el padre del nodo), por tanto no hay tío"
            
            self._log(f"El nodo {id_nodo} no tiene tío", "alerta")
            messagebox.showinfo("Sin Tío", msg)

# PUNTO DE ENTRADA
# ============================================================
# Patron estandar de Python: solo ejecutar si este archivo es
# el script principal (no si es importado como modulo).
if __name__ == "__main__":
    app = AplicacionAVL()
    app.mainloop()   # Inicia el bucle de eventos de tkinter 