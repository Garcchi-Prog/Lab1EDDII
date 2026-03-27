import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import csv
import os
import random
from datetime import datetime

# Configuración de colores para la interfaz
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


class Nodo:
    """
    Representamos cada curso como un nodo del árbol AVL.
    Almacenamos los datos completos del CSV y calculamos la satisfacción
    según la fórmula que nos dieron en el laboratorio.
    """
    def __init__(self, datos):
        self.datos = datos
        self.satisfaccion = self.calcular_satisfaccion()
        self.izquierda = None
        self.derecha = None
        self.altura = 1
    
    def calcular_satisfaccion(self):
        """
        Implementamos la fórmula: rating * 0.7 + ((5*positivas + negativas + 3*neutras) / total_reviews) * 0.3
        Redondeamos a 5 decimales como nos solicitaron.
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


def rotacion_simple_derecha(nodo):
    """
    Realizamos rotación simple a la derecha cuando el árbol está desbalanceado
    hacia la izquierda con el hijo izquierdo balanceado o con desbalance hacia la izquierda.
    """
    n_raiz = nodo.izquierda
    nodo.izquierda = n_raiz.derecha
    n_raiz.derecha = nodo
    return n_raiz


def rotacion_simple_izquierda(nodo):
    """
    Realizamos rotación simple a la izquierda cuando el árbol está desbalanceado
    hacia la derecha con el hijo derecho balanceado o con desbalance hacia la derecha.
    """
    n_raiz = nodo.derecha
    nodo.derecha = n_raiz.izquierda
    n_raiz.izquierda = nodo
    return n_raiz


def rotacion_doble_izquierda_derecha(nodo):
    """
    Aplicamos rotación doble izquierda-derecha cuando el desbalance es izquierda-derecha.
    Primero rotamos a la izquierda el hijo izquierdo, luego rotamos a la derecha el nodo.
    """
    nodo.izquierda = rotacion_simple_izquierda(nodo.izquierda)
    n_raiz = rotacion_simple_derecha(nodo)
    return n_raiz


def rotacion_doble_derecha_izquierda(nodo):
    """
    Aplicamos rotación doble derecha-izquierda cuando el desbalance es derecha-izquierda.
    Primero rotamos a la derecha el hijo derecho, luego rotamos a la izquierda el nodo.
    """
    nodo.derecha = rotacion_simple_derecha(nodo.derecha)
    n_raiz = rotacion_simple_izquierda(nodo)
    return n_raiz


def altura(nodo):
    """
    Calculamos la altura de un nodo de forma recursiva.
    """
    if nodo is None:
        return 0
    return 1 + max(altura(nodo.izquierda), altura(nodo.derecha))


def obtener_equilibrio(nodo):
    """
    Obtenemos el factor de equilibrio como altura_derecha - altura_izquierda.
    """
    if nodo is None:
        return 0
    return altura(nodo.derecha) - altura(nodo.izquierda)


def equilibrar(nodo):
    """
    Verificamos el factor de equilibrio y aplicamos la rotación correspondiente.
    """
    if nodo is None:
        return nodo
    
    equilibrio = obtener_equilibrio(nodo)
    
    # Caso de desbalance hacia la izquierda (equilibrio > 1)
    if equilibrio > 1:
        if obtener_equilibrio(nodo.izquierda) >= 0:
            return rotacion_simple_derecha(nodo)
        else:
            return rotacion_doble_izquierda_derecha(nodo)
    
    # Caso de desbalance hacia la derecha (equilibrio < -1)
    if equilibrio < -1:
        if obtener_equilibrio(nodo.derecha) <= 0:
            return rotacion_simple_izquierda(nodo)
        else:
            return rotacion_doble_derecha_izquierda(nodo)
    
    return nodo


# ============================================================
# Funciones recursivas para obtener relaciones familiares
# ============================================================

def buscar_padre(raiz, nodo):
    """
    Buscamos el padre de un nodo de forma recursiva.
    Retornamos None si no tiene padre (es la raíz).
    """
    if raiz is None:
        return None
    
    if raiz.izquierda is nodo or raiz.derecha is nodo:
        return raiz
    
    padre_izq = buscar_padre(raiz.izquierda, nodo)
    if padre_izq is not None:
        return padre_izq
    
    return buscar_padre(raiz.derecha, nodo)


def buscar_abuelo(raiz, nodo):
    """
    Encontramos el abuelo buscando primero el padre y luego el padre del padre.
    """
    padre = buscar_padre(raiz, nodo)
    if padre is None:
        return None
    return buscar_padre(raiz, padre)


def buscar_tio(raiz, nodo):
    """
    Encontramos el tío como el hermano del padre.
    """
    padre = buscar_padre(raiz, nodo)
    if padre is None:
        return None
    
    abuelo = buscar_padre(raiz, padre)
    if abuelo is None:
        return None
    
    if abuelo.izquierda is padre:
        return abuelo.derecha
    else:
        return abuelo.izquierda


def obtener_nivel(raiz, nodo, nivel_actual=0):
    """
    Calculamos la profundidad de un nodo. La raíz está en nivel 0.
    """
    if raiz is None:
        return -1
    if raiz is nodo:
        return nivel_actual
    
    nivel_izq = obtener_nivel(raiz.izquierda, nodo, nivel_actual + 1)
    if nivel_izq != -1:
        return nivel_izq
    
    return obtener_nivel(raiz.derecha, nodo, nivel_actual + 1)


# ============================================================
# Clase ArbolAVL - Implementación completa del árbol
# ============================================================

class ArbolAVL:
    """
    Implementamos el árbol AVL con auto-balanceo después de cada inserción y eliminación.
    Usamos la satisfacción como clave de ordenamiento.
    """
    
    def __init__(self):
        self.raiz = None
        self.dataset = {}  # Diccionario para acceder rápido a los datos por ID
    
    def cargar_dataset(self, ruta_archivo):
        """
        Cargamos el archivo CSV y lo almacenamos en el diccionario.
        """
        try:
            self.dataset.clear()
            with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector)  # Saltamos el encabezado
                for fila in lector:
                    if fila and len(fila) > 0:
                        # Aseguramos que tenga 14 campos
                        while len(fila) < 14:
                            fila.append("0")
                        self.dataset[fila[0]] = fila
            return True, f"Dataset cargado: {len(self.dataset)} registros"
        except Exception as e:
            return False, f"Error al cargar: {str(e)}"
    
    def _existe_satisfaccion(self, nodo, satisfaccion):
        """
        Verificamos si ya existe un nodo con la misma satisfacción para evitar duplicados.
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
        Insertamos recursivamente usando la satisfacción como clave de comparación.
        Luego balanceamos el árbol.
        """
        if nodo is None:
            return nuevo
        
        if nuevo.satisfaccion < nodo.satisfaccion:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, nuevo)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, nuevo)
        
        # Actualizamos altura y balanceamos
        nodo.altura = altura(nodo)
        nodo = equilibrar(nodo)
        
        return nodo
    
    def insertar(self, id_curso):
        """
        Insertamos un nodo por su ID. Buscamos los datos en el dataset.
        """
        if id_curso not in self.dataset:
            return False, f"El ID '{id_curso}' no existe en el dataset"
        
        datos = self.dataset[id_curso]
        nuevo_nodo = Nodo(datos)
        
        if self._existe_satisfaccion(self.raiz, nuevo_nodo.satisfaccion):
            return False, "Ya existe un curso con esa misma satisfaccion"
        
        self.raiz = self._insertar_recursivo(self.raiz, nuevo_nodo)
        return True, f"Curso '{nuevo_nodo.get_titulo()[:30]}' insertado"
    
    def buscar_por_id(self, nodo, id_buscar):
        """
        Buscamos un nodo por su ID recorriendo todo el árbol.
        """
        if nodo is None:
            return None
        if nodo.get_id() == id_buscar:
            return nodo
        
        izq = self.buscar_por_id(nodo.izquierda, id_buscar)
        if izq:
            return izq
        return self.buscar_por_id(nodo.derecha, id_buscar)
    
    def buscar_por_satisfaccion(self, nodo, sat_buscar):
        """
        Buscamos por satisfacción aprovechando la propiedad de BST.
        """
        if nodo is None:
            return None
        if nodo.satisfaccion == sat_buscar:
            return nodo
        if sat_buscar < nodo.satisfaccion:
            return self.buscar_por_satisfaccion(nodo.izquierda, sat_buscar)
        else:
            return self.buscar_por_satisfaccion(nodo.derecha, sat_buscar)
    
    def buscar(self, valor, tipo):
        """
        Método público para buscar por ID o por satisfacción.
        """
        if tipo == "id":
            return self.buscar_por_id(self.raiz, valor)
        else:
            try:
                return self.buscar_por_satisfaccion(self.raiz, float(valor))
            except:
                return None
    
    def _minimo(self, nodo):
        """
        Encontramos el nodo con valor mínimo en un subárbol.
        """
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    
    def _eliminar_recursivo(self, nodo, satisfaccion):
        """
        Eliminamos recursivamente y balanceamos después de la eliminación.
        """
        if nodo is None:
            return None
        
        if satisfaccion < nodo.satisfaccion:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, satisfaccion)
        elif satisfaccion > nodo.satisfaccion:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, satisfaccion)
        else:
            # Caso 1: sin hijos o un hijo
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            
            # Caso 2: dos hijos - reemplazamos con el sucesor inorden
            sucesor = self._minimo(nodo.derecha)
            nodo.datos = sucesor.datos
            nodo.satisfaccion = sucesor.satisfaccion
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.satisfaccion)
        
        nodo.altura = altura(nodo)
        nodo = equilibrar(nodo)
        
        return nodo
    
    def eliminar(self, valor, tipo):
        """
        Eliminamos un nodo por ID o por satisfacción.
        """
        nodo_a_eliminar = None
        
        if tipo == "id":
            nodo_a_eliminar = self.buscar_por_id(self.raiz, valor)
        else:
            try:
                sat = float(valor)
                nodo_a_eliminar = self.buscar_por_satisfaccion(self.raiz, sat)
            except:
                return False, "Valor de satisfaccion invalido"
        
        if nodo_a_eliminar is None:
            return False, "Nodo no encontrado"
        
        self.raiz = self._eliminar_recursivo(self.raiz, nodo_a_eliminar.satisfaccion)
        return True, f"Nodo {nodo_a_eliminar.get_id()} eliminado"
    
    def _inorden(self, nodo, lista):
        """
        Recorrido inorden recursivo.
        """
        if nodo:
            self._inorden(nodo.izquierda, lista)
            lista.append(nodo)
            self._inorden(nodo.derecha, lista)
    
    def recorrido_inorden(self):
        """
        Retornamos todos los nodos en orden ascendente por satisfacción.
        """
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado
    
    def _bfs_recursivo(self, nivel_actual, resultado):
        """
        Implementamos el recorrido por niveles de forma recursiva.
        """
        if not nivel_actual:
            return
        
        ids_nivel = [nodo.get_id() for nodo in nivel_actual]
        resultado.append(ids_nivel)
        
        siguiente_nivel = []
        for nodo in nivel_actual:
            if nodo.izquierda:
                siguiente_nivel.append(nodo.izquierda)
            if nodo.derecha:
                siguiente_nivel.append(nodo.derecha)
        
        self._bfs_recursivo(siguiente_nivel, resultado)
    
    def recorrido_por_niveles(self):
        """
        Mostramos el recorrido por niveles (BFS) de forma recursiva.
        Retornamos solo los identificadores como solicitaron.
        """
        if self.raiz is None:
            return []
        
        resultado = []
        self._bfs_recursivo([self.raiz], resultado)
        return resultado
    
    def contar_nodos(self):
        """
        Contamos la cantidad total de nodos en el árbol.
        """
        return len(self.recorrido_inorden())
    
    def buscar_4a_positivas_mayores(self):
        """
        Criterio 4a: reviews positivas > (negativas + neutras)
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
        Criterio 4b: fecha de creación posterior a la fecha dada.
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
        Criterio 4c: cantidad de clases dentro del rango [min, max]
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
        Criterio 4d: reviews positivas, negativas o neutras superiores al promedio.
        tipo puede ser "positivas", "negativas" o "neutras"
        """
        todos = self.recorrido_inorden()
        if not todos:
            return []
        
        if tipo == "positivas":
            valores = [float(n.get_positivas()) for n in todos]
        elif tipo == "negativas":
            valores = [float(n.get_negativas()) for n in todos]
        else:
            valores = [float(n.get_neutras()) for n in todos]
        
        promedio = sum(valores) / len(valores)
        
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
# Clase VisualizadorArbol - Para dibujar el árbol gráficamente
# ============================================================

class VisualizadorArbol(tk.Canvas):
    """
    Dibujamos el árbol gráficamente usando Canvas de tkinter.
    Cada nodo muestra su ID y su nivel de satisfacción.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", highlightthickness=1, **kwargs)
        self.arbol = None
        self.nodo_resaltado = None
        self.posiciones = {}
        self.config(scrollregion=(0, 0, 2000, 1500))
    
    def _calcular_posiciones(self, nodo, x, y, separacion):
        """
        Calculamos las coordenadas de cada nodo para el dibujo.
        """
        if nodo is None:
            return
        
        self.posiciones[nodo.get_id()] = (x, y)
        
        if nodo.izquierda:
            self._calcular_posiciones(nodo.izquierda, x - separacion, y + 80, separacion // 2)
        
        if nodo.derecha:
            self._calcular_posiciones(nodo.derecha, x + separacion, y + 80, separacion // 2)
    
    def _dibujar_conexiones(self, nodo):
        """
        Dibujamos las líneas que conectan los nodos.
        """
        if nodo is None or nodo.get_id() not in self.posiciones:
            return
        
        x, y = self.posiciones[nodo.get_id()]
        
        if nodo.izquierda and nodo.izquierda.get_id() in self.posiciones:
            x_izq, y_izq = self.posiciones[nodo.izquierda.get_id()]
            self.create_line(x, y + 20, x_izq, y_izq - 20, fill="#7f8c8d", width=2)
            self._dibujar_conexiones(nodo.izquierda)
        
        if nodo.derecha and nodo.derecha.get_id() in self.posiciones:
            x_der, y_der = self.posiciones[nodo.derecha.get_id()]
            self.create_line(x, y + 20, x_der, y_der - 20, fill="#7f8c8d", width=2)
            self._dibujar_conexiones(nodo.derecha)
    
    def _dibujar_nodos(self, nodo):
        """
        Dibujamos cada nodo como un círculo con su ID y satisfacción.
        """
        if nodo is None or nodo.get_id() not in self.posiciones:
            return
        
        x, y = self.posiciones[nodo.get_id()]
        
        if self.nodo_resaltado == nodo.get_id():
            color_borde = COLOR_ALERTA
            color_relleno = "#fff3cd"
        else:
            color_borde = COLOR_EXITO
            color_relleno = "#d5f4e6"
        
        radio = 25
        self.create_oval(x - radio, y - radio, x + radio, y + radio,
                         fill=color_relleno, outline=color_borde, width=2)
        
        id_texto = nodo.get_id()[:8]
        self.create_text(x, y - 5, text=id_texto, font=("Arial", 9, "bold"))
        self.create_text(x, y + 10, text=f"{nodo.satisfaccion:.3f}", 
                        font=("Arial", 7), fill="#555")
        
        self._dibujar_nodos(nodo.izquierda)
        self._dibujar_nodos(nodo.derecha)
    
    def dibujar_arbol(self, arbol, nodo_resaltado=None):
        """
        Método principal para dibujar el árbol completo.
        """
        self.delete("all")
        self.arbol = arbol
        self.nodo_resaltado = nodo_resaltado
        self.posiciones = {}
        
        if arbol is None or arbol.raiz is None:
            self.create_text(400, 300, text="Arbol vacio", font=("Arial", 16))
            return
        
        self._calcular_posiciones(arbol.raiz, 400, 50, 200)
        self._dibujar_conexiones(arbol.raiz)
        self._dibujar_nodos(arbol.raiz)


# ============================================================
# Clase VentanaInfo - Muestra información completa del curso
# ============================================================

class VentanaInfo(tk.Toplevel):
    """
    Ventana emergente que muestra toda la información de un curso seleccionado.
    También muestra nivel, factor de balance, padre, abuelo y tío.
    """
    
    def __init__(self, parent, nodo, arbol):
        super().__init__(parent)
        self.title(f"Informacion del Curso - {nodo.get_id()}")
        self.geometry("550x500")
        self.configure(bg=COLOR_PANEL)
        self.resizable(True, True)
        
        frame = tk.Frame(self, bg=COLOR_PANEL)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_titulo = tk.Label(frame, text=nodo.get_titulo(), 
                             font=("Arial", 12, "bold"),
                             bg=COLOR_PANEL, fg=COLOR_BOTON, wraplength=500)
        lbl_titulo.pack(anchor="w", pady=(0, 10))
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
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
        
        tab2 = tk.Frame(notebook, bg=COLOR_TARJETA)
        notebook.add(tab2, text="En el Arbol")
        
        padre = buscar_padre(arbol.raiz, nodo)
        abuelo = buscar_abuelo(arbol.raiz, nodo)
        tio = buscar_tio(arbol.raiz, nodo)
        nivel = obtener_nivel(arbol.raiz, nodo)
        balance = obtener_equilibrio(nodo)
        
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
        
        btn_cerrar = tk.Button(frame, text="Cerrar", command=self.destroy,
                              bg=COLOR_BOTON, fg="white", width=15)
        btn_cerrar.pack(pady=15)


# ============================================================
# Clase VentanaResultados - Muestra resultados de búsquedas
# ============================================================

class VentanaResultados(tk.Toplevel):
    """
    Ventana que muestra los resultados de las búsquedas especiales en forma de tabla.
    Permite seleccionar un nodo y ver su información completa.
    """
    
    def __init__(self, parent, nodos, arbol, titulo="Resultados"):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("700x400")
        self.configure(bg=COLOR_PANEL)
        
        self.arbol = arbol
        self.nodos = {n.get_id(): n for n in nodos}
        
        header = tk.Frame(self, bg=COLOR_PANEL)
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text=titulo, font=("Arial", 11, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(side="left")
        tk.Label(header, text=f"  ({len(nodos)} resultados)",
                bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC).pack(side="left")
        
        columnas = ("id", "titulo", "satisfaccion", "rating", "reviews", "clases")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        
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
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="left", fill="y", pady=10, padx=(0, 10))
        
        for nodo in nodos:
            self.tabla.insert("", "end", iid=nodo.get_id(), values=(
                nodo.get_id(),
                nodo.get_titulo()[:40],
                f"{nodo.satisfaccion:.5f}",
                nodo.get_rating(),
                nodo.get_reviews(),
                nodo.get_clases()
            ))
        
        self.tabla.bind("<Double-1>", self._mostrar_info)
        
        tk.Label(self, text="Doble clic en una fila para ver informacion completa",
                bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC, font=("Arial", 9)).pack(pady=(0, 10))
    
    def _mostrar_info(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            nodo_id = seleccion[0]
            if nodo_id in self.nodos:
                VentanaInfo(self, self.nodos[nodo_id], self.arbol)


# ============================================================
# Clase AplicacionAVL - Ventana principal
# ============================================================

class AplicacionAVL(tk.Tk):
    """
    Ventana principal que contiene todos los controles.
    Integra todas las operaciones requeridas.
    """
    
    def __init__(self):
        super().__init__()
        self.title("Laboratorio 1 - Arbol AVL (Cursos Udemy)")
        self.geometry("1200x750")
        self.configure(bg=COLOR_FONDO)
        
        self.arbol = ArbolAVL()
        
        self._crear_menu()
        self._crear_panel_izquierdo()
        self._crear_panel_central()
        self._crear_panel_derecho()
        
        self._log("Sistema iniciado. Cargue un dataset para comenzar.")
    
    def _crear_menu(self):
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
        panel = tk.Frame(self, bg=COLOR_PANEL, width=300)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        panel.pack_propagate(False)
        
        tk.Label(panel, text="Operaciones", font=("Arial", 12, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(pady=10)
        
        self._crear_seccion(panel, "Dataset")
        tk.Button(panel, text="Cargar CSV", command=self._cargar_dataset,
                 bg=COLOR_BOTON, fg="white", width=25).pack(pady=5)
        self.lbl_dataset = tk.Label(panel, text="Sin dataset cargado",
                                   bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC, wraplength=280)
        self.lbl_dataset.pack(pady=5)
        
        self._crear_seccion(panel, "Insertar Nodo")
        tk.Label(panel, text="ID del curso:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=20)
        self.entry_insertar = tk.Entry(panel, width=30)
        self.entry_insertar.pack(pady=5)
        tk.Button(panel, text="Insertar", command=self._insertar,
                 bg=COLOR_EXITO, fg="white", width=25).pack(pady=5)
        
        tk.Label(panel, text="IDs separados por coma:", bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC).pack(anchor="w", padx=20, pady=(10,0))
        self.entry_multi = tk.Text(panel, height=3, width=30)
        self.entry_multi.pack(pady=5)
        tk.Button(panel, text="Insertar Multiples", command=self._insertar_multi,
                 bg=COLOR_EXITO, fg="white", width=25).pack(pady=5)
        
        frame_rand = tk.Frame(panel, bg=COLOR_PANEL)
        frame_rand.pack(pady=5)
        tk.Label(frame_rand, text="Cantidad:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left")
        self.entry_rand = tk.Entry(frame_rand, width=5)
        self.entry_rand.insert(0, "5")
        self.entry_rand.pack(side="left", padx=5)
        tk.Button(frame_rand, text="Aleatorios", command=self._insertar_random,
                 bg=COLOR_EXITO, fg="white").pack(side="left")
        
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
        panel = tk.Frame(self, bg=COLOR_FONDO)
        panel.pack(side="left", fill="both", expand=True, pady=10)
        
        header = tk.Frame(panel, bg=COLOR_FONDO)
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="Visualizacion del Arbol AVL", 
                font=("Arial", 11, "bold"),
                bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left")
        self.lbl_contador = tk.Label(header, text="Nodos: 0",
                                    bg=COLOR_FONDO, fg=COLOR_EXITO)
        self.lbl_contador.pack(side="right")
        
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
        panel = tk.Frame(self, bg=COLOR_PANEL, width=300)
        panel.pack(side="right", fill="y", padx=10, pady=10)
        panel.pack_propagate(False)
        
        tk.Label(panel, text="Busquedas Especiales", font=("Arial", 12, "bold"),
                bg=COLOR_PANEL, fg=COLOR_ALERTA).pack(pady=10)
        
        tk.Button(panel, text="4a) Positivas > Neg + Neutras",
                 command=self._buscar_4a, bg="#9b59b6", fg="white",
                 width=30).pack(pady=5)
        
        tk.Label(panel, text="4b) Fecha posterior a (AAAA-MM-DD):",
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10,0))
        self.entry_fecha = tk.Entry(panel, width=15)
        self.entry_fecha.insert(0, "2020-01-01")
        self.entry_fecha.pack(pady=5)
        tk.Button(panel, text="Buscar por Fecha", command=self._buscar_4b,
                 bg="#9b59b6", fg="white", width=30).pack(pady=5)
        
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
        
        tk.Label(panel, text="4d) Tipo de reviews sobre promedio:",
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10,0))
        self.combo_tipo = ttk.Combobox(panel, values=["positivas", "negativas", "neutras"],
                                       width=15, state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(pady=5)
        tk.Button(panel, text="Buscar sobre Promedio", command=self._buscar_4d,
                 bg="#9b59b6", fg="white", width=30).pack(pady=5)
        
        self._crear_seccion(panel, "Recorrido")
        tk.Button(panel, text="Mostrar Recorrido por Niveles",
                 command=self._mostrar_recorrido, bg=COLOR_ALERTA, fg="white",
                 width=30).pack(pady=5)
        
        self._crear_seccion(panel, "Registro de Operaciones")
        self.txt_log = scrolledtext.ScrolledText(panel, width=35, height=12,
                                                bg=COLOR_TARJETA, fg=COLOR_TEXTO)
        self.txt_log.pack(padx=5, pady=5)
        self.txt_log.configure(state="disabled")
    
    def _crear_seccion(self, parent, titulo):
        tk.Frame(parent, bg=COLOR_BORDE, height=2).pack(fill="x", padx=10, pady=15)
        tk.Label(parent, text=titulo, font=("Arial", 10, "bold"),
                bg=COLOR_PANEL, fg=COLOR_BOTON).pack(anchor="w", padx=10)
    
    def _log(self, mensaje, tipo="info"):
        self.txt_log.configure(state="normal")
        hora = datetime.now().strftime("%H:%M:%S")
        
        if tipo == "error":
            tag = "error"
            self.txt_log.tag_configure("error", foreground=COLOR_ERROR)
        elif tipo == "exito":
            tag = "exito"
            self.txt_log.tag_configure("exito", foreground=COLOR_EXITO)
        else:
            tag = "info"
            self.txt_log.tag_configure("info", foreground=COLOR_TEXTO)
        
        self.txt_log.insert("end", f"[{hora}] {mensaje}\n", tag)
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")
    
    def _actualizar_vista(self, resaltar_id=None):
        self.canvas.dibujar_arbol(self.arbol, resaltar_id)
        self.lbl_contador.configure(text=f"Nodos: {self.arbol.contar_nodos()}")
    
    def _cargar_dataset(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")]
        )
        if ruta:
            exito, mensaje = self.arbol.cargar_dataset(ruta)
            if exito:
                nombre = os.path.basename(ruta)
                self.lbl_dataset.configure(text=f"{nombre}\n{mensaje}")
                self._log(mensaje, "exito")
            else:
                self._log(mensaje, "error")
    
    def _insertar(self):
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
        resultados = self.arbol.buscar_4a_positivas_mayores()
        self._log(f"4a: {len(resultados)} cursos cumplen el criterio")
        if resultados:
            VentanaResultados(self, resultados, self.arbol, 
                            "4a - Positivas > (Negativas + Neutras)")
    
    def _buscar_4b(self):
        fecha = self.entry_fecha.get().strip()
        resultados = self.arbol.buscar_4b_fecha_posterior(fecha)
        self._log(f"4b: {len(resultados)} cursos despues de {fecha}")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4b - Creados despues de {fecha}")
    
    def _buscar_4c(self):
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
        tipo = self.combo_tipo.get()
        resultados = self.arbol.buscar_4d_sobre_promedio(tipo)
        self._log(f"4d: {len(resultados)} cursos con {tipo} sobre promedio")
        if resultados:
            VentanaResultados(self, resultados, self.arbol,
                            f"4d - {tipo.capitalize()} sobre promedio")
    
    def _mostrar_recorrido(self):
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
            txt.insert("end", "  -  ".join(nivel) + "\n\n")
        
        txt.configure(state="disabled")
        
        total_nodos = sum(len(n) for n in niveles)
        self._log(f"Recorrido: {len(niveles)} niveles, {total_nodos} nodos")
    
    def _acerca_de(self):
        messagebox.showinfo("Acerca de",
            "Laboratorio 1 - Estructura de Datos II\n"
            "Universidad del Norte\n\n"
            "Arbol AVL para gestion de cursos Udemy\n"
            "Implementado con Python y tkinter")


if __name__ == "__main__":
    app = AplicacionAVL()
    app.mainloop()