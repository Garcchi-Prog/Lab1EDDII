"""
AVL Tree — Cursos Udemy  |  Estructura de Datos II
Interfaz gráfica de escritorio — pantalla completa
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
import random
from datetime import datetime
from typing import Optional, List, Dict, Tuple

# ══════════════════════════════════════════════════════
#  TEMA DE COLORES
# ══════════════════════════════════════════════════════
C = {
    "bg"     : "#0E1117",
    "panel"  : "#161B22",
    "card"   : "#1C2128",
    "border" : "#2D333B",
    "blue"   : "#58A6FF",
    "green"  : "#3FB950",
    "red"    : "#F85149",
    "purple" : "#BC8CFF",
    "orange" : "#FFA657",
    "yellow" : "#E3B341",
    "t1"     : "#CDD9E5",
    "t2"     : "#768390",
    "t3"     : "#444C56",
    "dark"   : "#0E1117",
}

F = {
    "title" : ("Segoe UI", 14, "bold"),
    "head"  : ("Segoe UI", 10, "bold"),
    "body"  : ("Segoe UI",  9),
    "small" : ("Segoe UI",  8),
    "mono"  : ("Consolas",  9),
    "mono_s": ("Consolas",  8),
}

# ══════════════════════════════════════════════════════
#  NODO
# ══════════════════════════════════════════════════════
class Node:
    __slots__ = ("data","satis","izquierda","derecha","altura_nodo")

    def __init__(self, data: list):
        self.data        = data
        self.satis       = self._sat()
        self.izquierda   = None
        self.derecha     = None
        self.altura_nodo = 1

    def _sat(self) -> float:
        try:
            r  = float(self.data[3])
            p  = float(self.data[11])
            n  = float(self.data[12])
            ne = float(self.data[13])
            nr = float(self.data[4])
            if nr:
                return round(r*0.7 + ((5*p + n + 3*ne)/nr)*0.3, 5)
            return 0.0
        except Exception:
            return 0.0

    def _g(self, i, default=""):
        return self.data[i] if len(self.data) > i else default

    @property
    def id(self):                     return self._g(0)
    @property
    def title(self):                  return self._g(1)
    @property
    def url(self):                    return self._g(2)
    @property
    def rating(self):                 return self._g(3,"0")
    @property
    def num_reviews(self):            return self._g(4,"0")
    @property
    def num_published_lectures(self): return self._g(5,"0")
    @property
    def created(self):                return self._g(6)
    @property
    def last_update_date(self):       return self._g(7)
    @property
    def duration(self):               return self._g(8,"0")
    @property
    def instructors_id(self):         return self._g(9)
    @property
    def image(self):                  return self._g(10)
    @property
    def positive_reviews(self):       return self._g(11,"0")
    @property
    def negative_reviews(self):       return self._g(12,"0")
    @property
    def neutral_reviews(self):        return self._g(13,"0")


# ══════════════════════════════════════════════════════
#  FUNCIONES AVL
# ══════════════════════════════════════════════════════
def _h(n):  return n.altura_nodo if n else 0
def _uh(n): n.altura_nodo = 1 + max(_h(n.izquierda), _h(n.derecha))
def _eq(n): return (_h(n.izquierda) - _h(n.derecha)) if n else 0

def _rr(n):
    r = n.izquierda
    n.izquierda = r.derecha
    r.derecha = n
    _uh(n); _uh(r)
    return r

def _rl(n):
    r = n.derecha
    n.derecha = r.izquierda
    r.izquierda = n
    _uh(n); _uh(r)
    return r

def equilibrar(n):
    if n is None: return None
    _uh(n)
    e = _eq(n)
    if e > 1:
        if _eq(n.izquierda) < 0: n.izquierda = _rl(n.izquierda)
        return _rr(n)
    if e < -1:
        if _eq(n.derecha) > 0:   n.derecha = _rr(n.derecha)
        return _rl(n)
    return n

# ══════════════════════════════════════════════════════
#  FUNCIONES RECURSIVAS REQUERIDAS
# ══════════════════════════════════════════════════════
def BuscarPadre(raiz, nodo):
    if raiz is None: return None
    if raiz.izquierda is nodo or raiz.derecha is nodo: return raiz
    r = BuscarPadre(raiz.izquierda, nodo)
    return r if r else BuscarPadre(raiz.derecha, nodo)

def BuscarAbuelo(raiz, nodo):
    p = BuscarPadre(raiz, nodo)
    return BuscarPadre(raiz, p) if p else None

def BuscarTio(raiz, nodo):
    p = BuscarPadre(raiz, nodo)
    if p is None: return None
    ab = BuscarPadre(raiz, p)
    if ab is None: return None
    return ab.derecha if ab.izquierda is p else ab.izquierda

def obtener_nivel(raiz, nodo):
    if raiz is None: return -1
    if raiz is nodo: return 0
    lvl = obtener_nivel(raiz.izquierda, nodo)
    if lvl != -1: return lvl + 1
    lvl = obtener_nivel(raiz.derecha, nodo)
    return lvl + 1 if lvl != -1 else -1

# ══════════════════════════════════════════════════════
#  ÁRBOL AVL
# ══════════════════════════════════════════════════════
class AVLTree:
    def __init__(self):
        self.raiz: Optional[Node] = None
        self._dataset: Dict[str, list] = {}

    def cargar_dataset(self, path: str) -> str:
        try:
            self._dataset.clear()
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row:
                        while len(row) < 14: row.append("0")
                        self._dataset[row[0]] = row
            return f"Dataset cargado: {len(self._dataset):,} registros"
        except Exception as e:
            return f"Error: {e}"

    def add_node(self, node_id: str) -> Tuple[bool, str]:
        fila = self._dataset.get(node_id)
        if fila is None: return False, f"ID '{node_id}' no existe."
        nn = Node(fila)
        ok, msg, self.raiz = self._ins(self.raiz, nn)
        return ok, msg

    def _ins(self, n, nn):
        if n is None: return True, "Insertado.", nn
        if nn.satis < n.satis:
            ok, msg, n.izquierda = self._ins(n.izquierda, nn)
        elif nn.satis > n.satis:
            ok, msg, n.derecha = self._ins(n.derecha, nn)
        else:
            return False, "Satisfacción duplicada.", n
        return ok, msg, equilibrar(n)

    def delete_node(self, val: str, opt: str) -> Tuple[bool, str]:
        nd = self.search_node(val, opt)
        if nd is None: return False, "Nodo no encontrado."
        self.raiz = self._del(self.raiz, nd.satis)
        return True, f"ID {nd.id} eliminado."

    def _del(self, n, s):
        if n is None: return None
        if s < n.satis:   n.izquierda = self._del(n.izquierda, s)
        elif s > n.satis: n.derecha   = self._del(n.derecha, s)
        else:
            if n.izquierda is None: return n.derecha
            if n.derecha   is None: return n.izquierda
            suc = self._min(n.derecha)
            n.data = suc.data; n.satis = suc.satis
            n.derecha = self._del(n.derecha, suc.satis)
        return equilibrar(n)

    def _min(self, n):
        while n.izquierda: n = n.izquierda
        return n

    def search_node(self, val: str, opt: str) -> Optional[Node]:
        if opt == "id":    return self._bid(self.raiz, val)
        if opt == "satis":
            try:           return self._bsat(self.raiz, float(val))
            except:        return None
        return None

    def _bid(self, n, id_):
        if n is None: return None
        if n.data[0] == id_: return n
        r = self._bid(n.izquierda, id_)
        return r if r else self._bid(n.derecha, id_)

    def _bsat(self, n, s):
        if n is None: return None
        if s == n.satis: return n
        return self._bsat(n.izquierda, s) if s < n.satis else self._bsat(n.derecha, s)

    def todos(self) -> List[Node]:
        out = []
        def io(n):
            if n: io(n.izquierda); out.append(n); io(n.derecha)
        io(self.raiz); return out

    def total_nodos(self) -> int: return len(self.todos())

    @staticmethod
    def _f(v):
        try: return float(v)
        except: return 0.0

    @staticmethod
    def _i(v):
        try: return int(float(v))
        except: return 0

    def buscar_4a(self):
        return [n for n in self.todos()
                if self._f(n.positive_reviews) > self._f(n.negative_reviews)+self._f(n.neutral_reviews)]

    def buscar_4b(self, fecha_str: str):
        try:
            ref = None
            for fmt in ("%Y-%m-%d","%d/%m/%Y","%m/%d/%Y"):
                try: ref = datetime.strptime(fecha_str, fmt); break
                except: continue
            if ref is None: return []
            out = []
            for n in self.todos():
                try:
                    fn = datetime.strptime(n.created[:10], "%Y-%m-%d")
                    if fn > ref: out.append(n)
                except: pass
            return out
        except: return []

    def buscar_4c(self, mn, mx):
        return [n for n in self.todos() if mn <= self._i(n.num_published_lectures) <= mx]

    def buscar_4d(self, tipo: str):
        todos = self.todos()
        if not todos: return []
        mapa = {"positivas": lambda n: self._f(n.positive_reviews),
                "negativas":  lambda n: self._f(n.negative_reviews),
                "neutras":    lambda n: self._f(n.neutral_reviews)}
        fn   = mapa.get(tipo, mapa["positivas"])
        vals = [fn(n) for n in todos]
        prom = sum(vals) / len(vals)
        return [n for n, v in zip(todos, vals) if v > prom]

    def recorrido_niveles(self) -> List[List[str]]:
        res = []
        def bfs(nivel):
            if not nivel: return
            ids = [n.id for n in nivel if n]
            if ids: res.append(ids)
            sig = []
            for n in nivel:
                if n:
                    if n.izquierda: sig.append(n.izquierda)
                    if n.derecha:   sig.append(n.derecha)
            bfs(sig)
        if self.raiz: bfs([self.raiz])
        return res


# ══════════════════════════════════════════════════════
#  CANVAS DEL ÁRBOL
# ══════════════════════════════════════════════════════
class TreeCanvas(tk.Canvas):
    NR    = 28
    V_GAP = 80

    def __init__(self, parent, **kw):
        super().__init__(parent, bg=C["bg"], highlightthickness=0, **kw)
        self._tree = None
        self._hl   = None
        self._pos  = {}
        self._ox   = 0; self._oy = 50
        self._sc   = 1.0
        self._dx   = 0; self._dy = 0
        self.bind("<Configure>",     lambda _: self._draw())
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<B1-Motion>",     self._drag)
        self.bind("<MouseWheel>",    self._wheel)
        self.bind("<Button-4>",      self._wheel)
        self.bind("<Button-5>",      self._wheel)

    def set_tree(self, tree, hl=None):
        self._tree = tree; self._hl = hl; self._draw()

    def reset_view(self):
        self._ox=0; self._oy=50; self._sc=1.0; self._draw()

    def _press(self, e): self._dx=e.x; self._dy=e.y

    def _drag(self, e):
        self._ox += e.x-self._dx; self._oy += e.y-self._dy
        self._dx=e.x; self._dy=e.y; self._draw()

    def _wheel(self, e):
        f = 1.1 if (e.delta>0 or e.num==4) else 0.9
        self._sc = max(0.15, min(4.0, self._sc*f))
        self._draw()

    def _draw(self):
        self.delete("all")
        if not self._tree or not self._tree.raiz:
            w,h = self.winfo_width() or 600, self.winfo_height() or 400
            self.create_text(w//2, h//2,
                text="Árbol vacío  —  carga el dataset e inserta nodos",
                fill=C["t2"], font=F["body"])
            return
        self._pos.clear()
        w = self.winfo_width() or 800
        self._layout(self._tree.raiz, 0, 0, w)
        self._edges(self._tree.raiz)
        self._nodes(self._tree.raiz)

    def _layout(self, n, d, lo, hi):
        if n is None: return
        mid = (lo+hi)/2
        self._pos[n.id] = (int(mid+self._ox), int(d*self.V_GAP*self._sc+self._oy))
        self._layout(n.izquierda, d+1, lo, mid)
        self._layout(n.derecha,   d+1, mid, hi)

    def _edges(self, n):
        if n is None: return
        if n.id in self._pos:
            px,py = self._pos[n.id]
            for child in (n.izquierda, n.derecha):
                if child and child.id in self._pos:
                    cx,cy = self._pos[child.id]
                    self.create_line(px,py,cx,cy, fill=C["border"], width=1)
        self._edges(n.izquierda); self._edges(n.derecha)

    def _nodes(self, n):
        if n is None or n.id not in self._pos: return
        x,y = self._pos[n.id]
        r   = max(7, int(self.NR*self._sc))
        eq  = _eq(n)
        hl  = (n.id == self._hl)

        if hl:                   fill, ring = C["orange"], C["orange"]
        elif eq == 0:            fill, ring = C["card"],   C["green"]
        elif abs(eq) == 1:       fill, ring = C["card"],   C["blue"]
        else:                    fill, ring = C["card"],   C["red"]

        self.create_oval(x-r+2,y-r+2,x+r+2,y+r+2, fill="#00000055", outline="")
        self.create_oval(x-r,y-r,x+r,y+r, fill=fill, outline=ring,
                         width=2 if hl else 1)
        fs = max(5, int(8*self._sc))
        self.create_text(x, y-3, text=n.id[:7], fill=C["t1"],
                         font=("Consolas", fs, "bold"))
        self.create_text(x, y+fs, text=f"{n.satis:.3f}", fill=C["t2"],
                         font=("Consolas", max(5,fs-1)))
        self._nodes(n.izquierda); self._nodes(n.derecha)


# ══════════════════════════════════════════════════════
#  DIÁLOGO: INFO DEL NODO
# ══════════════════════════════════════════════════════
class NodeInfoDialog(tk.Toplevel):
    def __init__(self, parent, node: Node, tree: AVLTree):
        super().__init__(parent)
        self.title(f"Curso — {node.id}")
        self.configure(bg=C["panel"])
        self.geometry("660x560")
        self.resizable(True, True)

        padre  = BuscarPadre(tree.raiz, node)
        abuelo = BuscarAbuelo(tree.raiz, node)
        tio    = BuscarTio(tree.raiz, node)
        nivel  = obtener_nivel(tree.raiz, node)
        eq     = _eq(node)

        tk.Label(self, text=node.title, bg=C["panel"], fg=C["blue"],
                 font=F["head"], wraplength=630, justify="left",
                 padx=16, pady=8).pack(anchor="w")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=(0,12))

        # Tab datos
        t1 = tk.Frame(nb, bg=C["card"])
        nb.add(t1, text="  Datos del Curso  ")
        filas = [
            ("ID",            node.id),
            ("Satisfacción",  f"{node.satis:.5f}"),
            ("Rating",        node.rating),
            ("Nº Reseñas",    node.num_reviews),
            ("Reseñas +",     node.positive_reviews),
            ("Reseñas −",     node.negative_reviews),
            ("Reseñas ~",     node.neutral_reviews),
            ("Clases",        node.num_published_lectures),
            ("Duración",      node.duration),
            ("Creado",        node.created),
            ("Actualizado",   node.last_update_date),
            ("Instructor ID", node.instructors_id),
            ("URL",           node.url[:70]),
        ]
        for i,(k,v) in enumerate(filas):
            bg = C["card"] if i%2==0 else C["panel"]
            row = tk.Frame(t1, bg=bg); row.pack(fill="x")
            tk.Label(row, text=k, bg=bg, fg=C["t2"], font=F["small"],
                     width=16, anchor="e").pack(side="left", padx=(8,4), pady=3)
            tk.Label(row, text=v, bg=bg, fg=C["t1"], font=F["mono_s"],
                     anchor="w").pack(side="left", padx=4)

        # Tab árbol/familia
        t2 = tk.Frame(nb, bg=C["card"])
        nb.add(t2, text="  Árbol / Familia  ")
        arbol_rows = [
            ("Nivel",             str(nivel),                                          C["green"]),
            ("Factor Equilibrio", str(eq),                                             C["blue"]),
            ("Padre",   f"{padre.id} · {padre.title[:35]}"   if padre  else "Sin padre (raíz)", C["t1"]),
            ("Abuelo",  f"{abuelo.id} · {abuelo.title[:35]}" if abuelo else "Sin abuelo",       C["t1"]),
            ("Tío",     f"{tio.id} · {tio.title[:35]}"       if tio    else "Sin tío",          C["t1"]),
        ]
        for i,(k,v,col) in enumerate(arbol_rows):
            bg = C["card"] if i%2==0 else C["panel"]
            row = tk.Frame(t2, bg=bg); row.pack(fill="x")
            tk.Label(row, text=k, bg=bg, fg=C["t2"], font=F["small"],
                     width=18, anchor="e").pack(side="left", padx=(8,4), pady=5)
            tk.Label(row, text=v, bg=bg, fg=col, font=F["mono_s"],
                     anchor="w").pack(side="left", padx=4)

        tk.Button(self, text="Cerrar", command=self.destroy,
                  bg=C["blue"], fg=C["dark"], font=F["body"],
                  relief="flat", padx=24, pady=5, cursor="hand2").pack(pady=10)


# ══════════════════════════════════════════════════════
#  PANEL: RESULTADOS DE BÚSQUEDA
# ══════════════════════════════════════════════════════
class ResultsPanel(tk.Toplevel):
    def __init__(self, parent, nodos: List[Node], tree: AVLTree, title="Resultados"):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=C["panel"])
        self.geometry("820x480")

        hdr = tk.Frame(self, bg=C["panel"]); hdr.pack(fill="x", padx=14, pady=8)
        tk.Label(hdr, text=title, bg=C["panel"], fg=C["blue"],
                 font=F["head"]).pack(side="left")
        tk.Label(hdr, text=f"  {len(nodos)} resultado(s)", bg=C["panel"],
                 fg=C["t2"], font=F["small"]).pack(side="left")

        cols = ("id","titulo","satisfaccion","rating","reseñas","clases")
        tv   = ttk.Treeview(self, columns=cols, show="headings", selectmode="browse")
        for c,w,t in [("id",90,"ID"),("titulo",280,"Título"),
                      ("satisfaccion",110,"Satisfacción"),
                      ("rating",75,"Rating"),("reseñas",80,"Reseñas"),
                      ("clases",65,"Clases")]:
            tv.heading(c, text=t)
            tv.column(c, width=w, anchor="center" if c!="titulo" else "w")

        sb = ttk.Scrollbar(self, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side="left", fill="both", expand=True, padx=(14,0), pady=(0,14))
        sb.pack(side="left", fill="y", pady=(0,14), padx=(0,8))

        for n in nodos:
            tv.insert("","end", iid=n.id,
                      values=(n.id, n.title[:45], f"{n.satis:.5f}",
                              n.rating, n.num_reviews, n.num_published_lectures))

        def dbl(e):
            sel = tv.selection()
            if sel:
                nd = tree._bid(tree.raiz, sel[0])
                if nd: NodeInfoDialog(self, nd, tree)

        tv.bind("<Double-1>", dbl)
        tk.Label(self, text="Doble clic → información completa del curso",
                 bg=C["panel"], fg=C["t2"], font=F["small"]).pack(pady=(0,8))


# ══════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol AVL — Cursos Udemy  |  Estructura de Datos II")
        self.configure(bg=C["bg"])
        self.state("zoomed")
        try: self.attributes("-zoomed", True)
        except: pass

        self._tree = AVLTree()
        self._apply_styles()
        self._build()
        self._log("Bienvenido al sistema AVL — Cursos Udemy.", "info")
        self._log("Carga el CSV con el botón  ▸ Cargar CSV  en la pestaña Operaciones.", "info")

    def _apply_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", background=C["panel"], foreground=C["t1"],
                    font=F["body"], borderwidth=0)
        s.configure("TNotebook",      background=C["bg"],    borderwidth=0)
        s.configure("TNotebook.Tab",  background=C["card"],  foreground=C["t2"],
                    padding=[10,4],   font=F["small"])
        s.map("TNotebook.Tab",
              background=[("selected", C["panel"])],
              foreground=[("selected", C["t1"])])
        s.configure("TScrollbar",     background=C["border"], troughcolor=C["card"],
                    arrowcolor=C["t2"], relief="flat")
        s.configure("TCombobox",      fieldbackground=C["card"], background=C["card"],
                    foreground=C["t1"], arrowcolor=C["t2"])
        s.configure("Treeview",
            background=C["card"], fieldbackground=C["card"],
            foreground=C["t1"], rowheight=20, font=F["mono_s"])
        s.configure("Treeview.Heading",
            background=C["panel"], foreground=C["t2"], font=F["small"])
        s.map("Treeview", background=[("selected", C["blue"])])

    # ────────────────────────────────────────────────
    #  CONSTRUCCIÓN UI
    # ────────────────────────────────────────────────
    def _build(self):
        # Topbar
        top = tk.Frame(self, bg=C["panel"], height=42)
        top.pack(fill="x"); top.pack_propagate(False)
        tk.Label(top, text="🌳  AVL Tree — Udemy Courses",
                 bg=C["panel"], fg=C["blue"], font=F["title"],
                 padx=16).pack(side="left", pady=6)
        self._sv_nodes = tk.StringVar(value="Nodos: 0")
        self._sv_ds    = tk.StringVar(value="Sin dataset")
        tk.Label(top, textvariable=self._sv_ds,    bg=C["panel"], fg=C["t2"],    font=F["small"]).pack(side="right", padx=16)
        tk.Label(top, textvariable=self._sv_nodes, bg=C["panel"], fg=C["green"], font=F["body"]).pack(side="right", padx=8)
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x")

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)

        # Panel izquierdo — tabs
        left = tk.Frame(body, bg=C["panel"], width=330)
        left.pack(side="left", fill="y"); left.pack_propagate(False)
        self._build_left(left)

        # Centro — árbol
        mid = tk.Frame(body, bg=C["bg"])
        mid.pack(side="left", fill="both", expand=True)
        self._build_center(mid)

        # Derecha — log
        right = tk.Frame(body, bg=C["panel"], width=265)
        right.pack(side="right", fill="y"); right.pack_propagate(False)
        self._build_log(right)

    # ── Panel izquierdo ─────────────────────────────
    def _build_left(self, parent):
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True, padx=2, pady=2)

        t1 = self._scrollable_tab(nb, "Operaciones")
        t2 = self._scrollable_tab(nb, "Buscar")
        t3 = self._scrollable_tab(nb, "Especiales")
        t4 = self._scrollable_tab(nb, "Árbol")

        self._tab_ops(t1)
        self._tab_buscar(t2)
        self._tab_especiales(t3)
        self._tab_arbol(t4)

    def _scrollable_tab(self, nb, text):
        outer  = tk.Frame(nb, bg=C["panel"])
        nb.add(outer, text=f" {text} ")
        cnv    = tk.Canvas(outer, bg=C["panel"], highlightthickness=0)
        sb     = ttk.Scrollbar(outer, orient="vertical", command=cnv.yview)
        inner  = tk.Frame(cnv, bg=C["panel"])
        inner.bind("<Configure>",
            lambda e: cnv.configure(scrollregion=cnv.bbox("all")))
        cnv.create_window((0,0), window=inner, anchor="nw")
        cnv.configure(yscrollcommand=sb.set)
        sb.pack(side="right",  fill="y")
        cnv.pack(side="left",  fill="both", expand=True)

        def _mw(e):
            d = int(-1*(e.delta/120)) if e.delta else (-1 if e.num==4 else 1)
            cnv.yview_scroll(d, "units")
        cnv.bind("<MouseWheel>", _mw)
        cnv.bind("<Button-4>",   _mw)
        cnv.bind("<Button-5>",   _mw)
        return inner

    # ── Tab Operaciones ─────────────────────────────
    def _tab_ops(self, p):
        # Dataset
        self._sec(p, "📂 Dataset")
        self._btn(p, "▸  Cargar CSV", self._cargar_dataset, C["blue"]).pack(
            fill="x", padx=10, pady=(3,1))
        self._ds_lbl = tk.Label(p, text="Sin dataset cargado",
                                 bg=C["panel"], fg=C["t2"],
                                 font=F["small"], wraplength=290, justify="left")
        self._ds_lbl.pack(anchor="w", padx=12, pady=(0,6))

        # Insertar simple
        self._sec(p, "➕ Insertar Nodo")
        self._ins_id = self._entry(p, "ID del curso:")
        self._btn(p, "Insertar", self._insertar, C["green"]).pack(fill="x", padx=10, pady=2)

        # Insertar múltiple
        tk.Label(p, text="Múltiples IDs (separados por coma):",
                 bg=C["panel"], fg=C["t2"], font=F["small"]).pack(
                     anchor="w", padx=12, pady=(6,1))
        self._ins_multi = tk.Text(p, height=3, bg=C["card"], fg=C["t1"],
                                   font=F["mono_s"], relief="flat",
                                   insertbackground=C["blue"], wrap="word")
        self._ins_multi.pack(fill="x", padx=10, pady=2)
        self._btn(p, "Insertar Lista", self._insertar_multi, C["green"]).pack(
            fill="x", padx=10, pady=2)

        # Insertar aleatorio
        row = tk.Frame(p, bg=C["panel"]); row.pack(fill="x", padx=10, pady=4)
        tk.Label(row, text="Insertar N aleatorios:",
                 bg=C["panel"], fg=C["t2"], font=F["small"]).pack(side="left")
        self._rand_n = tk.Entry(row, width=5, bg=C["card"], fg=C["t1"],
                                 font=F["mono_s"], relief="flat",
                                 insertbackground=C["blue"])
        self._rand_n.insert(0,"10"); self._rand_n.pack(side="left", padx=6)
        self._btn(row, "▶ Insertar", self._insertar_random, C["green"]).pack(side="left")

        # Eliminar
        self._sec(p, "🗑  Eliminar Nodo")
        self._del_val = self._entry(p, "ID o valor de satisfacción:")
        self._del_opt = tk.StringVar(value="id")
        row2 = tk.Frame(p, bg=C["panel"]); row2.pack(fill="x", padx=10, pady=2)
        for txt, val in [("Por ID","id"),("Por Satisfacción","satis")]:
            tk.Radiobutton(row2, text=txt, variable=self._del_opt, value=val,
                           bg=C["panel"], fg=C["t1"], selectcolor=C["card"],
                           activebackground=C["panel"],
                           font=F["small"]).pack(side="left", padx=4)
        self._btn(p, "Eliminar", self._eliminar, C["red"]).pack(fill="x", padx=10, pady=3)

    # ── Tab Buscar ──────────────────────────────────
    def _tab_buscar(self, p):
        self._sec(p, "🔍 Buscar Nodo")
        self._sch_val = self._entry(p, "ID o valor de satisfacción:")
        self._sch_opt = tk.StringVar(value="id")
        row = tk.Frame(p, bg=C["panel"]); row.pack(fill="x", padx=10, pady=2)
        for txt,val in [("Por ID","id"),("Por Satisfacción","satis")]:
            tk.Radiobutton(row, text=txt, variable=self._sch_opt, value=val,
                           bg=C["panel"], fg=C["t1"], selectcolor=C["card"],
                           activebackground=C["panel"],
                           font=F["small"]).pack(side="left", padx=4)
        self._btn(p, "Buscar", self._buscar, C["blue"]).pack(fill="x", padx=10, pady=3)
        tk.Label(p, text="El nodo encontrado se resalta en el árbol\ny se abre su ventana de información.",
                 bg=C["panel"], fg=C["t2"], font=F["small"],
                 justify="left").pack(anchor="w", padx=14, pady=6)

    # ── Tab Especiales ──────────────────────────────
    def _tab_especiales(self, p):
        self._sec(p, "🔎 Búsquedas Especiales")

        self._btn(p, "4a)  Positivas > Neg + Neutras",
                  self._buscar_4a, C["purple"]).pack(fill="x", padx=10, pady=3)

        tk.Label(p, text="4b)  Creados después de (AAAA-MM-DD):",
                 bg=C["panel"], fg=C["t2"], font=F["small"]).pack(anchor="w", padx=12, pady=(6,1))
        rb = tk.Frame(p, bg=C["panel"]); rb.pack(fill="x", padx=10, pady=2)
        self._fecha = tk.Entry(rb, width=12, bg=C["card"], fg=C["t1"],
                               font=F["mono_s"], relief="flat",
                               insertbackground=C["blue"])
        self._fecha.insert(0,"2020-01-01"); self._fecha.pack(side="left")
        self._btn(rb, "Buscar", self._buscar_4b, C["purple"]).pack(side="left", padx=8)

        tk.Label(p, text="4c)  Clases dentro de un rango:",
                 bg=C["panel"], fg=C["t2"], font=F["small"]).pack(anchor="w", padx=12, pady=(6,1))
        rc = tk.Frame(p, bg=C["panel"]); rc.pack(fill="x", padx=10, pady=2)
        tk.Label(rc,text="Min:",bg=C["panel"],fg=C["t2"],font=F["small"]).pack(side="left")
        self._rmin = tk.Entry(rc,width=5,bg=C["card"],fg=C["t1"],font=F["mono_s"],
                              relief="flat",insertbackground=C["blue"])
        self._rmin.insert(0,"10"); self._rmin.pack(side="left",padx=4)
        tk.Label(rc,text="Max:",bg=C["panel"],fg=C["t2"],font=F["small"]).pack(side="left")
        self._rmax = tk.Entry(rc,width=5,bg=C["card"],fg=C["t1"],font=F["mono_s"],
                              relief="flat",insertbackground=C["blue"])
        self._rmax.insert(0,"100"); self._rmax.pack(side="left",padx=4)
        self._btn(rc,"Buscar",self._buscar_4c,C["purple"]).pack(side="left",padx=6)

        tk.Label(p, text="4d)  Reseñas sobre el promedio:",
                 bg=C["panel"], fg=C["t2"], font=F["small"]).pack(anchor="w", padx=12, pady=(6,1))
        rd = tk.Frame(p, bg=C["panel"]); rd.pack(fill="x", padx=10, pady=2)
        self._rtipo = ttk.Combobox(rd, values=["positivas","negativas","neutras"],
                                    width=11, state="readonly")
        self._rtipo.current(0); self._rtipo.pack(side="left")
        self._btn(rd,"Buscar",self._buscar_4d,C["purple"]).pack(side="left",padx=8)

    # ── Tab Árbol ───────────────────────────────────
    def _tab_arbol(self, p):
        self._sec(p, "📊 Recorrido")
        self._btn(p, "Recorrido por Niveles (BFS)",
                  self._mostrar_niveles, C["orange"]).pack(fill="x", padx=10, pady=3)

        self._sec(p, "⚙  Controles")
        self._btn(p, "Resetear Vista", self._reset_view, C["t2"]).pack(fill="x", padx=10, pady=2)
        self._btn(p, "Limpiar Árbol",  self._limpiar,    C["red"]).pack(fill="x", padx=10, pady=2)

        self._sec(p, "🗺  Leyenda")
        for color, label in [
            (C["green"],  "Equilibrado  eq = 0"),
            (C["blue"],   "Casi bal.  |eq| = 1"),
            (C["red"],    "Desbalanceado"),
            (C["orange"], "Nodo resaltado"),
        ]:
            r = tk.Frame(p, bg=C["panel"]); r.pack(anchor="w", padx=14, pady=2)
            tk.Canvas(r, width=11, height=11, bg=color,
                      highlightthickness=0).pack(side="left", padx=(0,6))
            tk.Label(r, text=label, bg=C["panel"], fg=C["t2"],
                     font=F["small"]).pack(side="left")

        self._sec(p, "🖱  Controles del Canvas")
        tk.Label(p, text="Arrastrar  →  mover árbol\nRueda      →  zoom in/out",
                 bg=C["panel"], fg=C["t2"], font=F["small"],
                 justify="left").pack(anchor="w", padx=14, pady=4)

    # ── Canvas central ──────────────────────────────
    def _build_center(self, parent):
        hdr = tk.Frame(parent, bg=C["bg"]); hdr.pack(fill="x", padx=10, pady=4)
        tk.Label(hdr, text="Visualización del Árbol AVL",
                 bg=C["bg"], fg=C["t1"], font=F["head"]).pack(side="left")
        tk.Label(hdr, text="  arrastra para mover  ·  rueda para zoom",
                 bg=C["bg"], fg=C["t2"], font=F["small"]).pack(side="left")

        self._canvas = TreeCanvas(parent)
        self._canvas.pack(fill="both", expand=True, padx=8, pady=(0,8))

    # ── Log ─────────────────────────────────────────
    def _build_log(self, parent):
        tk.Label(parent, text="Registro de Operaciones",
                 bg=C["panel"], fg=C["purple"], font=F["head"],
                 padx=10, pady=6).pack(anchor="w")
        tk.Frame(parent, bg=C["border"], height=1).pack(fill="x")

        self._log_txt = tk.Text(parent, bg=C["card"], fg=C["t1"],
                                 font=F["mono_s"], relief="flat",
                                 state="disabled", wrap="word",
                                 padx=6, pady=4)
        sb = ttk.Scrollbar(parent, orient="vertical", command=self._log_txt.yview)
        self._log_txt.configure(yscrollcommand=sb.set)
        self._log_txt.pack(side="left",  fill="both", expand=True, padx=(8,0), pady=8)
        sb.pack(side="right", fill="y", pady=8, padx=(0,4))

        self._log_txt.tag_configure("ok",   foreground=C["green"])
        self._log_txt.tag_configure("err",  foreground=C["red"])
        self._log_txt.tag_configure("info", foreground=C["blue"])
        self._log_txt.tag_configure("warn", foreground=C["yellow"])

    # ════════════════════════════════════════════════
    #  HELPERS
    # ════════════════════════════════════════════════
    def _sec(self, p, txt):
        tk.Frame(p, bg=C["border"], height=1).pack(fill="x", padx=8, pady=(10,3))
        tk.Label(p, text=txt, bg=C["panel"], fg=C["purple"],
                 font=F["head"], padx=10).pack(anchor="w")

    def _entry(self, p, label):
        tk.Label(p, text=label, bg=C["panel"], fg=C["t2"],
                 font=F["small"]).pack(anchor="w", padx=12, pady=(4,0))
        e = tk.Entry(p, bg=C["card"], fg=C["t1"], font=F["mono_s"],
                     relief="flat", insertbackground=C["blue"])
        e.pack(fill="x", padx=10, pady=2)
        return e

    def _btn(self, parent, text, cmd, color=None):
        color = color or C["blue"]
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=C["dark"], font=F["small"],
                      relief="flat", padx=8, pady=4, cursor="hand2",
                      activebackground=color, activeforeground=C["dark"])
        b.bind("<Enter>", lambda e: b.configure(relief="groove"))
        b.bind("<Leave>", lambda e: b.configure(relief="flat"))
        return b

    def _log(self, msg: str, tag="info"):
        self._log_txt.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self._log_txt.insert("end", f"[{ts}] {msg}\n", tag)
        self._log_txt.see("end"); self._log_txt.configure(state="disabled")

    def _refresh(self, hl=None):
        self._canvas.set_tree(self._tree, hl)
        self._sv_nodes.set(f"Nodos: {self._tree.total_nodos()}")

    # ════════════════════════════════════════════════
    #  ACCIONES
    # ════════════════════════════════════════════════
    def _cargar_dataset(self):
        path = filedialog.askopenfilename(
            title="Seleccionar CSV",
            filetypes=[("CSV","*.csv"),("Todos","*.*")])
        if not path: return
        msg = self._tree.cargar_dataset(path)
        n   = len(self._tree._dataset)
        self._ds_lbl.configure(text=f"{os.path.basename(path)}  ({n:,} reg.)")
        self._sv_ds.set(f"Dataset: {n:,} reg.")
        self._log(msg, "ok")

    def _insertar(self):
        v = self._ins_id.get().strip()
        if not v: self._log("Escribe un ID.", "err"); return
        ok, msg = self._tree.add_node(v)
        self._log(msg, "ok" if ok else "err")
        if ok: self._refresh(v)
        self._ins_id.delete(0,"end")

    def _insertar_multi(self):
        txt = self._ins_multi.get("1.0","end").strip()
        ids = [i.strip() for i in txt.replace("\n",",").split(",") if i.strip()]
        if not ids: self._log("Sin IDs.", "err"); return
        ok_c = 0
        for id_ in ids:
            ok, msg = self._tree.add_node(id_)
            if ok: ok_c += 1
            else:  self._log(f"  {id_}: {msg}", "warn")
        self._log(f"{ok_c}/{len(ids)} nodos insertados.", "ok")
        self._refresh(); self._ins_multi.delete("1.0","end")

    def _insertar_random(self):
        if not self._tree._dataset:
            self._log("Carga un dataset primero.", "err"); return
        try: n = int(self._rand_n.get())
        except: n = 10
        ids  = random.sample(list(self._tree._dataset.keys()),
                             min(n, len(self._tree._dataset)))
        ok_c = sum(1 for id_ in ids if self._tree.add_node(id_)[0])
        self._log(f"{ok_c} nodos aleatorios insertados.", "ok")
        self._refresh()

    def _eliminar(self):
        v = self._del_val.get().strip()
        if not v: self._log("Escribe un valor.", "err"); return
        ok, msg = self._tree.delete_node(v, self._del_opt.get())
        self._log(msg, "ok" if ok else "err")
        if ok: self._refresh()
        self._del_val.delete(0,"end")

    def _buscar(self):
        v = self._sch_val.get().strip()
        if not v: self._log("Escribe un valor.", "err"); return
        nd = self._tree.search_node(v, self._sch_opt.get())
        if nd is None:
            self._log(f"'{v}' no encontrado.", "err")
        else:
            self._log(f"Encontrado: {nd.id} · {nd.title[:32]} · Satis={nd.satis:.5f}", "ok")
            self._refresh(nd.id)
            NodeInfoDialog(self, nd, self._tree)
        self._sch_val.delete(0,"end")

    def _buscar_4a(self):
        ns = self._tree.buscar_4a()
        self._log(f"4a: {len(ns)} nodos (positivas > neg+neutras)", "ok")
        ResultsPanel(self, ns, self._tree, "4a — Positivas > Neg+Neutras") if ns \
            else self._log("Sin resultados.", "warn")

    def _buscar_4b(self):
        f  = self._fecha.get().strip()
        ns = self._tree.buscar_4b(f)
        self._log(f"4b: {len(ns)} nodos creados después de {f}", "ok")
        ResultsPanel(self, ns, self._tree, f"4b — Posterior a {f}") if ns \
            else self._log("Sin resultados o fecha inválida.", "warn")

    def _buscar_4c(self):
        try: mn,mx = int(self._rmin.get()), int(self._rmax.get())
        except: self._log("Rango inválido.", "err"); return
        ns = self._tree.buscar_4c(mn, mx)
        self._log(f"4c: {len(ns)} nodos con clases {mn}–{mx}", "ok")
        ResultsPanel(self, ns, self._tree, f"4c — Clases {mn}–{mx}") if ns \
            else self._log("Sin resultados.", "warn")

    def _buscar_4d(self):
        t  = self._rtipo.get()
        ns = self._tree.buscar_4d(t)
        self._log(f"4d: {len(ns)} nodos con {t} sobre el promedio", "ok")
        ResultsPanel(self, ns, self._tree, f"4d — {t.capitalize()} sobre promedio") if ns \
            else self._log("Sin resultados.", "warn")

    def _mostrar_niveles(self):
        niveles = self._tree.recorrido_niveles()
        if not niveles: self._log("Árbol vacío.", "warn"); return
        win = tk.Toplevel(self)
        win.title("Recorrido por Niveles — BFS Recursivo")
        win.configure(bg=C["panel"]); win.geometry("700x520")
        tk.Label(win, text="Recorrido por Niveles  (BFS Recursivo)",
                 bg=C["panel"], fg=C["blue"], font=F["head"], pady=10).pack()
        txt = tk.Text(win, bg=C["card"], fg=C["t1"], font=F["mono_s"],
                      relief="flat", padx=12, pady=8)
        sb2 = ttk.Scrollbar(win, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb2.set)
        txt.pack(side="left", fill="both", expand=True, padx=(16,0), pady=(0,16))
        sb2.pack(side="right", fill="y", pady=(0,16), padx=(0,8))
        txt.tag_configure("lvl", foreground=C["purple"], font=("Consolas",9,"bold"))
        for i, ids in enumerate(niveles):
            txt.insert("end", f"Nivel {i:>2}:  ", "lvl")
            txt.insert("end", "  ·  ".join(ids)+"\n")
        txt.configure(state="disabled")
        self._log(f"Niveles: {len(niveles)}  ·  Total nodos: {self._tree.total_nodos()}", "info")

    def _reset_view(self): self._canvas.reset_view()

    def _limpiar(self):
        if messagebox.askyesno("Confirmar", "¿Limpiar el árbol por completo?",
                               icon="warning"):
            self._tree.raiz = None
            self._refresh()
            self._log("Árbol limpiado.", "warn")


# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    App().mainloop()
