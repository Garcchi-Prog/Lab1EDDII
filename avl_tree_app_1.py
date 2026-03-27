import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import csv
import os
import random
from datetime import datetime

# ============================================================
# COLORES GLOBALES (simples, definidos como variables sueltas)
# ============================================================
COLOR_FONDO = "#2c3e50"
COLOR_PANEL = "#34495e"
COLOR_TARJETA = "#1C2128"
COLOR_BORDE = "#7f8c8d"
COLOR_BOTON = "#3498db"
COLOR_EXITO = "#2ecc71"
COLOR_ERROR = "#e74c3c"
COLOR_ALERTA = "#f39c12"
COLOR_TEXTO = "#ecf0f1"
COLOR_TEXTO_SEC = "#bdc3c7"

# ============================================================
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
        self.satisfaccion = self.calcular_satisfaccion()
        self.izquierda = None
        self.derecha = None
        self.altura = 1  # altura inicial
    
    def calcular_satisfaccion(self):
        """
        Formula: rating * 0.7 + ((5*positivas + negativas + 3*neutras) / total) * 0.3
        Resultado redondeado a 5 decimales
        """
        try:
    # Los convierte a float para evitar problemas de formato          
            rating = float(self.datos[3])
            positivas = float(self.datos[11])
            negativas = float(self.datos[12])
            neutras = float(self.datos[13])
            total_reviews = float(self.datos[4])
            
            if total_reviews > 0:
                valor = rating * 0.7 + ((5 * positivas + negativas + 3 * neutras) / total_reviews) * 0.3
                return round(valor, 5)
            return 0.0
        # tira error si algun campo no es convertible a float, en ese caso retornamos 0.0
        except:
            return 0.0
    
    # Metodos para acceder a los campos facilmente
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

# ============================================================
# FUNCIONES AUXILIARES DEL AVL
# ============================================================

def obtener_altura(nodo):
    """Devuelve la altura de un nodo (0 si es None)"""
    if nodo is None:
        return 0
    return nodo.altura

def actualizar_altura(nodo):
    """Actualiza la altura de un nodo basado en sus hijos"""
    if nodo is not None:
        alt_izq = obtener_altura(nodo.izquierda)
        alt_der = obtener_altura(nodo.derecha)
        nodo.altura = 1 + max(alt_izq, alt_der)

def obtener_balance(nodo):
    """Calcula el factor de balance: altura izq - altura der"""
    if nodo is None:
        return 0
    return obtener_altura(nodo.izquierda) - obtener_altura(nodo.derecha)

def rotacion_derecha(y):
    """
    Rotacion simple a la derecha.
    y es el nodo desbalanceado, x es su hijo izquierdo.
    """
    x = y.izquierda
    temp = x.derecha
    
    # Realizar rotacion
    x.derecha = y
    y.izquierda = temp
    
    # Actualizar alturas
    actualizar_altura(y)
    actualizar_altura(x)
    
    return x

def rotacion_izquierda(x):
    """
    Rotacion simple a la izquierda.
    x es el nodo desbalanceado, y es su hijo derecho.
    """
    y = x.derecha
    temp = y.izquierda
    
    # Realizar rotacion
    y.izquierda = x
    x.derecha = temp
    
    # Actualizar alturas
    actualizar_altura(x)
    actualizar_altura(y)
    
    return y

# ============================================================
# FUNCIONES RECURSIVAS REQUERIDAS POR EL LABORATORIO
# ============================================================

def buscar_padre(raiz, nodo):
    """
    Busca el padre de un nodo de forma recursiva.
    Retorna el nodo padre o None si no tiene.
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
    
    # Buscar en subarbol derecho
    return buscar_padre(raiz.derecha, nodo)

def buscar_abuelo(raiz, nodo):
    """
    Busca el abuelo de un nodo.
    Primero encuentra el padre, luego el padre del padre.
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
    
    # El tio es el otro hijo del abuelo
    if abuelo.izquierda is padre:
        return abuelo.derecha
    else:
        return abuelo.izquierda

def obtener_nivel(raiz, nodo, nivel_actual=0):
    """
    Obtiene el nivel (profundidad) de un nodo.
    La raiz es nivel 0.
    """
    if raiz is None:
        return -1
    if raiz is nodo:
        return nivel_actual
    
    # Buscar en izquierda
    nivel_izq = obtener_nivel(raiz.izquierda, nodo, nivel_actual + 1)
    if nivel_izq != -1:
        return nivel_izq
    
    # Buscar en derecha
    return obtener_nivel(raiz.derecha, nodo, nivel_actual + 1)

# ============================================================
# CLASE ARBOL AVL
# ============================================================

class ArbolAVL:
    """
    Implementacion del arbol AVL con operaciones basicas.
    Se auto-balancea despues de cada insercion o eliminacion.
    """
    
    def __init__(self):
        self.raiz = None
        self.dataset = {}  # diccionario para guardar los datos del CSV
    
    def cargar_dataset(self, ruta_archivo):
        """
        Carga el archivo CSV en memoria.
        Retorna mensaje de exito o error.
        """
        try:
            self.dataset.clear()
            with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector)  # saltar encabezado
                for fila in lector:
                    if fila and len(fila) > 0:
                        # Asegurar que tenga 14 campos
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
        """
        if id_curso not in self.dataset:
            return False, f"El ID '{id_curso}' no existe en el dataset"
        
        datos = self.dataset[id_curso]
        nuevo_nodo = Nodo(datos)
        
        # Verificar si ya existe un nodo con esa satisfaccion
        if self._existe_satisfaccion(self.raiz, nuevo_nodo.satisfaccion):
            return False, "Ya existe un curso con esa misma satisfaccion"
        
        self.raiz = self._insertar_recursivo(self.raiz, nuevo_nodo)
        return True, f"Curso '{nuevo_nodo.get_titulo()[:30]}' insertado"
    
    def _existe_satisfaccion(self, nodo, satisfaccion):
        """Verifica si ya existe un nodo con esa satisfaccion"""
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
        Insercion recursiva con balanceo.
        """
        # Caso base: llegamos a una hoja
        if nodo is None:
            return nuevo
        
        # Insertar segun valor de satisfaccion
        if nuevo.satisfaccion < nodo.satisfaccion:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, nuevo)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, nuevo)
        
        # Actualizar altura del nodo actual
        actualizar_altura(nodo)
        
        # Obtener factor de balance
        balance = obtener_balance(nodo)
        
        # Caso 1: Desbalance hacia la izquierda (Left Left)
        if balance > 1 and nuevo.satisfaccion < nodo.izquierda.satisfaccion:
            return rotacion_derecha(nodo)
        
        # Caso 2: Desbalance hacia la derecha (Right Right)
        if balance < -1 and nuevo.satisfaccion > nodo.derecha.satisfaccion:
            return rotacion_izquierda(nodo)
        
        # Caso 3: Left Right
        if balance > 1 and nuevo.satisfaccion > nodo.izquierda.satisfaccion:
            nodo.izquierda = rotacion_izquierda(nodo.izquierda)
            return rotacion_derecha(nodo)
        
        # Caso 4: Right Left
        if balance < -1 and nuevo.satisfaccion < nodo.derecha.satisfaccion:
            nodo.derecha = rotacion_derecha(nodo.derecha)
            return rotacion_izquierda(nodo)
        
        return nodo
    
    def eliminar(self, valor, tipo):
        """
        Elimina un nodo por ID o por satisfaccion.
        tipo: "id" o "satis"
        """
        nodo_a_eliminar = None
        
        if tipo == "id":
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
        """Busqueda recursiva por ID (recorre todo el arbol)"""
        if nodo is None:
            return None
        if nodo.get_id() == id_buscar:
            return nodo
        
        # Buscar en ambos subarboles
        izq = self.buscar_por_id(nodo.izquierda, id_buscar)
        if izq:
            return izq
        return self.buscar_por_id(nodo.derecha, id_buscar)
    
    def buscar_por_satisfaccion(self, nodo, sat_buscar):
        """Busqueda por satisfaccion (aprovecha el orden del BST)"""
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
        Eliminacion recursiva con balanceo.
        """
        if nodo is None:
            return None
        
        # Buscar el nodo
        if satisfaccion < nodo.satisfaccion:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, satisfaccion)
        elif satisfaccion > nodo.satisfaccion:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, satisfaccion)
        else:
            # Nodo encontrado - 3 casos
            
            # Caso 1: sin hijos o un hijo
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            
            # Caso 2: dos hijos - buscar sucesor
            sucesor = self._minimo(nodo.derecha)
            nodo.datos = sucesor.datos
            nodo.satisfaccion = sucesor.satisfaccion
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.satisfaccion)
        
        # Actualizar altura
        actualizar_altura(nodo)
        
        # Balancear
        balance = obtener_balance(nodo)
        
        # Left Left
        if balance > 1 and obtener_balance(nodo.izquierda) >= 0:
            return rotacion_derecha(nodo)
        
        # Left Right
        if balance > 1 and obtener_balance(nodo.izquierda) < 0:
            nodo.izquierda = rotacion_izquierda(nodo.izquierda)
            return rotacion_derecha(nodo)
        
        # Right Right
        if balance < -1 and obtener_balance(nodo.derecha) <= 0:
            return rotacion_izquierda(nodo)
        
        # Right Left
        if balance < -1 and obtener_balance(nodo.derecha) > 0:
            nodo.derecha = rotacion_derecha(nodo.derecha)
            return rotacion_izquierda(nodo)
        
        return nodo
    
    def _minimo(self, nodo):
        """Encuentra el nodo con valor minimo en un subarbol"""
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    
    def buscar(self, valor, tipo):
        """Metodo publico para buscar"""
        if tipo == "id":
            return self.buscar_por_id(self.raiz, valor)
        else:
            try:
                return self.buscar_por_satisfaccion(self.raiz, float(valor))
            except:
                return None
    
    def recorrido_inorden(self):
        """Retorna lista de nodos en orden"""
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado
    
    def _inorden(self, nodo, lista):
        if nodo:
            self._inorden(nodo.izquierda, lista)
            lista.append(nodo)
            self._inorden(nodo.derecha, lista)
    
    def recorrido_por_niveles(self):
        """
        Recorrido BFS (por niveles) implementado recursivamente.
        Retorna lista de listas, donde cada sublista es un nivel.
        """
        if self.raiz is None:
            return []
        
        resultado = []
        self._bfs_recursivo([self.raiz], resultado)
        return resultado
    
    def _bfs_recursivo(self, nivel_actual, resultado):
        """Funcion auxiliar recursiva para BFS"""
        if not nivel_actual:
            return
        
        # Guardar IDs del nivel actual
        ids_nivel = [nodo.get_id() for nodo in nivel_actual]
        resultado.append(ids_nivel)
        
        # Construir siguiente nivel
        siguiente_nivel = []
        for nodo in nivel_actual:
            if nodo.izquierda:
                siguiente_nivel.append(nodo.izquierda)
            if nodo.derecha:
                siguiente_nivel.append(nodo.derecha)
        
        # Llamada recursiva
        self._bfs_recursivo(siguiente_nivel, resultado)
    
    def contar_nodos(self):
        """Cuenta total de nodos en el arbol"""
        return len(self.recorrido_inorden())
    
    # ============================================================
    # BUSQUEDAS ESPECIALES (punto 4 del laboratorio)
    # ============================================================
    
    def buscar_4a_positivas_mayores(self):
        """
        4a: Reviews positivas > (negativas + neutras)
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
        """
        try:
            fecha_ref = datetime.strptime(fecha_str, "%Y-%m-%d")
            resultado = []
            todos = self.recorrido_inorden()
            
            for nodo in todos:
                try:
                    fecha_nodo = datetime.strptime(nodo.get_fecha_creacion()[:10], "%Y-%m-%d")
                    if fecha_nodo > fecha_ref:
                        resultado.append(nodo)
                except:
                    continue
            
            return resultado
        except:
            return []
    
    def buscar_4c_rango_clases(self, min_clases, max_clases):
        """
        4c: Cantidad de clases dentro de un rango [min, max]
        """
        resultado = []
        todos = self.recorrido_inorden()
        
        for nodo in todos:
            try:
                clases = int(nodo.get_clases())
                if min_clases <= clases <= max_clases:
                    resultado.append(nodo)
            except:
                continue
        
        return resultado
    
    def buscar_4d_sobre_promedio(self, tipo):
        """
        4d: Reviews positivas, negativas o neutras superiores al promedio.
        tipo: "positivas", "negativas" o "neutras"
        """
        todos = self.recorrido_inorden()
        if not todos:
            return []
        
        # Calcular promedio segun el tipo
        if tipo == "positivas":
            valores = [float(n.get_positivas()) for n in todos]
        elif tipo == "negativas":
            valores = [float(n.get_negativas()) for n in todos]
        else:  # neutras
            valores = [float(n.get_neutras()) for n in todos]
        
        promedio = sum(valores) / len(valores)
        
        # Filtrar los que estan sobre el promedio
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

# ============================================================
# VISUALIZACION CON CANVAS
# ============================================================

class VisualizadorArbol(tk.Canvas):
    """
    Canvas personalizado para dibujar el arbol AVL.
    Usa circulos para nodos y lineas para conexiones.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", highlightthickness=1, **kwargs)
        self.arbol = None
        self.nodo_resaltado = None
        self.posiciones = {}
        
        # Configurar scroll
        self.config(scrollregion=(0, 0, 2000, 1500))
    
    def dibujar_arbol(self, arbol, nodo_resaltado=None):
        """Dibuja el arbol completo"""
        self.delete("all")
        self.arbol = arbol
        self.nodo_resaltado = nodo_resaltado
        self.posiciones = {}
        
        if arbol is None or arbol.raiz is None:
            self.create_text(400, 300, text="Arbol vacio", font=("Arial", 16))
            return
        
        # Calcular posiciones
        self._calcular_posiciones(arbol.raiz, 400, 50, 200)
        
        # Dibujar conexiones primero (para que queden detras)
        self._dibujar_conexiones(arbol.raiz)
        
        # Dibujar nodos
        self._dibujar_nodos(arbol.raiz)
    
    def _calcular_posiciones(self, nodo, x, y, separacion):
        """Calcula las coordenadas de cada nodo"""
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
        """Dibuja las lineas entre nodos"""
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
        """Dibuja los circulos de los nodos"""
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
        
        # Dibujar circulo
        radio = 25
        self.create_oval(x - radio, y - radio, x + radio, y + radio,
                          fill=color_relleno, outline=color_borde, width=2)
        
        # Dibujar ID (truncado si es muy largo)
        id_texto = nodo.get_id()[:8]
        self.create_text(x, y - 5, text=id_texto, font=("Arial", 9, "bold"))
        
        # Dibujar satisfaccion (3 decimales)
        self.create_text(x, y + 10, text=f"{nodo.satisfaccion:.3f}", 
                        font=("Arial", 7), fill="#555")
        
        # Recursivamente dibujar hijos
        self._dibujar_nodos(nodo.izquierda)
        self._dibujar_nodos(nodo.derecha)

# ============================================================
# VENTANA DE INFORMACION DEL NODO
# ============================================================

class VentanaInfo(tk.Toplevel):
    """Ventana emergente que muestra toda la informacion de un curso"""
    
    def __init__(self, parent, nodo, arbol):
        super().__init__(parent)
        self.title(f"Informacion del Curso - {nodo.get_id()}")
        self.geometry("550x500")
        self.configure(bg=COLOR_PANEL)
        self.resizable(True, True)
        
        # Frame principal
        frame = tk.Frame(self, bg=COLOR_PANEL)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Titulo del curso
        lbl_titulo = tk.Label(frame, text=nodo.get_titulo(), 
                             font=("Arial", 12, "bold"),
                             bg=COLOR_PANEL, fg=COLOR_BOTON, wraplength=500)
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        # Notebook (pestanas)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # Pestaña 1: Datos del curso
        tab1 = tk.Frame(notebook, bg=COLOR_TARJETA)
        notebook.add(tab1, text="Datos del Curso")
        
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
        
        # Buscar relaciones
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

# ============================================================
# VENTANA DE RESULTADOS DE BUSQUEDA
# ============================================================

class VentanaResultados(tk.Toplevel):
    """Muestra los resultados de busqueda avanzada en una tabla"""
    
    def __init__(self, parent, nodos, arbol, titulo="Resultados"):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("700x400")
        self.configure(bg=COLOR_PANEL)
        
        self.arbol = arbol
        self.nodos = {n.get_id(): n for n in nodos}  # diccionario para acceso rapido
        
        # Header
        header = tk.Frame(self, bg=COLOR_PANEL)
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text=titulo, font=("Arial", 11, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(side="left")
        tk.Label(header, text=f"  ({len(nodos)} resultados)",
                bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC).pack(side="left")
        
        # Tabla (Treeview)
        columnas = ("id", "titulo", "satisfaccion", "rating", "reviews", "clases")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        
        # Configurar columnas
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
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="left", fill="y", pady=10, padx=(0, 10))
        
        # Insertar datos
        for nodo in nodos:
            self.tabla.insert("", "end", iid=nodo.get_id(), values=(
                nodo.get_id(),
                nodo.get_titulo()[:40],
                f"{nodo.satisfaccion:.5f}",
                nodo.get_rating(),
                nodo.get_reviews(),
                nodo.get_clases()
            ))
        
        # Evento doble clic
        self.tabla.bind("<Double-1>", self._mostrar_info)
        
        # Label instruccion
        tk.Label(self, text="Doble clic en una fila para ver informacion completa",
                bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC, font=("Arial", 9)).pack(pady=(0, 10))
    
    def _mostrar_info(self, event):
        """Abre ventana de info al hacer doble clic"""
        seleccion = self.tabla.selection()
        if seleccion:
            nodo_id = seleccion[0]
            if nodo_id in self.nodos:
                VentanaInfo(self, self.nodos[nodo_id], self.arbol)

# ============================================================
# APLICACION PRINCIPAL
# ============================================================

class AplicacionAVL(tk.Tk):
    """Ventana principal de la aplicacion"""
    
    def __init__(self):
        super().__init__()
        self.title("Laboratorio 1 - Arbol AVL (Cursos Udemy)")
        self.geometry("1200x750")
        self.configure(bg=COLOR_FONDO)
        
        # Inicializar arbol
        self.arbol = ArbolAVL()
        
        # Crear interfaz
        self._crear_menu()
        self._crear_panel_izquierdo()
        self._crear_panel_central()
        self._crear_panel_derecho()
        
        # Mensaje inicial
        self._log("Sistema iniciado. Cargue un dataset para comenzar.")
    
    def _crear_menu(self):
        """Crea la barra de menu"""
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
        """Panel con controles de operaciones"""
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
        
        # Insertar multiples
        tk.Label(panel, text="IDs separados por coma:", bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC).pack(anchor="w", padx=20, pady=(10,0))
        self.entry_multi = tk.Text(panel, height=3, width=30)
        self.entry_multi.pack(pady=5)
        tk.Button(panel, text="Insertar Multiples", command=self._insertar_multi,
                 bg=COLOR_EXITO, fg="white", width=25).pack(pady=5)
        
        # Insertar aleatorios
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
        """Panel con la visualizacion del arbol"""
        panel = tk.Frame(self, bg=COLOR_FONDO)
        panel.pack(side="left", fill="both", expand=True, pady=10)
        
        # Header
        header = tk.Frame(panel, bg=COLOR_FONDO)
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="Visualizacion del Arbol AVL", 
                font=("Arial", 11, "bold"),
                bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left")
        self.lbl_contador = tk.Label(header, text="Nodos: 0",
                                    bg=COLOR_FONDO, fg=COLOR_EXITO)
        self.lbl_contador.pack(side="right")
        
        # Canvas con scrollbars
        frame_canvas = tk.Frame(panel, bg="white")
        frame_canvas.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.canvas = VisualizadorArbol(frame_canvas, width=800, height=600)
        hbar = ttk.Scrollbar(frame_canvas, orient="horizontal", command=self.canvas.xview)
        vbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="ew")
        
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
    
    def _crear_panel_derecho(self):
        """Panel con busquedas especiales y log"""
        panel = tk.Frame(self, bg=COLOR_PANEL, width=300)
        panel.pack(side="right", fill="y", padx=10, pady=10)
        panel.pack_propagate(False)
        
        # Titulo
        tk.Label(panel, text="Busquedas Especiales", font=("Arial", 12, "bold"),
                bg=COLOR_PANEL, fg=COLOR_ALERTA).pack(pady=10)
        
        # 4a
        tk.Button(panel, text="4a) Positivas > Neg + Neutras",
                 command=self._buscar_4a, bg="#9b59b6", fg="white",
                 width=30).pack(pady=5)
        
        # 4b
        tk.Label(panel, text="4b) Fecha posterior a (AAAA-MM-DD):",
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10,0))
        self.entry_fecha = tk.Entry(panel, width=15)
        self.entry_fecha.insert(0, "2020-01-01")
        self.entry_fecha.pack(pady=5)
        tk.Button(panel, text="Buscar por Fecha", command=self._buscar_4b,
                 bg="#9b59b6", fg="white", width=30).pack(pady=5)
        
        # 4c
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
        
        # 4d
        tk.Label(panel, text="4d) Tipo de reviews sobre promedio:",
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10,0))
        self.combo_tipo = ttk.Combobox(panel, values=["positivas", "negativas", "neutras"],
                                       width=15, state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=5)
        tk.Button(panel, text="Buscar sobre Promedio", command=self._buscar_4d,
                 bg="#9b59b6", fg="white", width=30).pack(pady=5)
        
        # Recorrido por niveles
        self._crear_seccion(panel, "Recorrido")
        tk.Button(panel, text="Mostrar Recorrido por Niveles",
                 command=self._mostrar_recorrido, bg=COLOR_ALERTA, fg="white",
                 width=30).pack(pady=5)
        
        # Log
        self._crear_seccion(panel, "Registro de Operaciones")
        self.txt_log = scrolledtext.ScrolledText(panel, width=35, height=12,
                                                bg=COLOR_TARJETA, fg=COLOR_TEXTO)
        self.txt_log.pack(padx=5, pady=5)
        self.txt_log.configure(state="disabled")
    
    def _crear_seccion(self, parent, titulo):
        """Crea un separador visual con titulo"""
        tk.Frame(parent, bg=COLOR_BORDE, height=2).pack(fill="x", padx=10, pady=15)
        tk.Label(parent, text=titulo, font=("Arial", 10, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(anchor="w", padx=10)
    
    def _log(self, mensaje, tipo="info"):
        """Agrega mensaje al log"""
        self.txt_log.configure(state="normal")
        import datetime
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        
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
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")
    
    def _actualizar_vista(self, resaltar_id=None):
        """Redibuja el arbol y actualiza contadores"""
        self.canvas.dibujar_arbol(self.arbol, resaltar_id)
        self.lbl_contador.configure(text=f"Nodos: {self.arbol.contar_nodos()}")
    
    # ============================================================
    # ACCIONES DE LOS BOTONES
    # ============================================================
    
    def _cargar_dataset(self):
        """Carga el archivo CSV"""
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
        """Inserta un solo nodo"""
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
        """Inserta multiples nodos"""
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
        """Inserta nodos aleatorios del dataset"""
        if not self.arbol.dataset:
            self._log("Cargue un dataset primero", "error")
            return
        
        try:
            cantidad = int(self.entry_rand.get())
        except:
            cantidad = 5
        
        ids_disponibles = list(self.arbol.dataset.keys())
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
        """Elimina un nodo"""
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
        """Busca un nodo y muestra su info"""
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
        """Busqueda 4b: fecha posterior"""
        fecha = self.entry_fecha.get().strip()
        resultados = self.arbol.buscar_4b_fecha_posterior(fecha)
        self._log(f"4b: {len(resultados)} cursos despues de {fecha}")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4b - Creados despues de {fecha}")
    
    def _buscar_4c(self):
        """Busqueda 4c: rango de clases"""
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
        """Busqueda 4d: sobre promedio"""
        tipo = self.combo_tipo.get()
        resultados = self.arbol.buscar_4d_sobre_promedio(tipo)
        self._log(f"4d: {len(resultados)} cursos con {tipo} sobre promedio")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4d - {tipo.capitalize()} sobre promedio")
    
    def _mostrar_recorrido(self):
        """Muestra ventana con recorrido por niveles"""
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

# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    app = AplicacionAVL()
    app.mainloop()