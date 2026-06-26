import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PI = 3.141592653589793

def raiz_cuadrada(n):
    if n <= 0:
        return 0
    x = n
    for i in range(100):
        x = (x + n / x) / 2
    return x

def valor_absoluto(n):
    if n < 0:
        return -n
    return n

def exponencial(x):
    resultado = 1.0
    termino = 1.0
    for i in range(1, 80):
        termino = termino * x / i
        resultado = resultado + termino
    return resultado

def coseno_hiperbola(x):
    return (exponencial(x) + exponencial(-x)) / 2

def seno_hiperbola(x):
    return (exponencial(x) - exponencial(-x)) / 2

def seno(x):
    while x > PI:
        x = x - 2 * PI
    while x < -PI:
        x = x + 2 * PI
    resultado = 0.0
    termino = x
    for i in range(1, 40):
        resultado = resultado + termino
        termino = -termino * x * x / ((2 * i) * (2 * i + 1))
    return resultado

def coseno(x):
    while x > PI:
        x = x - 2 * PI
    while x < -PI:
        x = x + 2 * PI
    resultado = 0.0
    termino = 1.0
    for i in range(1, 40):
        resultado = resultado + termino
        termino = -termino * x * x / ((2 * i - 1) * (2 * i))
    return resultado


class GraficoConicas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figura = Figure(figsize=(5, 5), dpi=100)
        self.ejes = self.figura.add_subplot(111)
        self.lienzo = FigureCanvasTkAgg(self.figura, master=self)
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.ejes.clear()
        self.lienzo.draw()

    def marcar_punto(self, punto, color, texto):
        if punto is None:
            return

        x, y = punto
        self.ejes.plot(x, y, "o", color=color, markersize=6)
        self.ejes.annotate(texto, (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)

    def marcar_puntos(self, puntos, color, texto):
        if not puntos:
            return

        for i, punto in enumerate(puntos, start=1):
            self.marcar_punto(punto, color, f"{texto}{i}")

    def dibujar_directriz(self, directriz):
        if not directriz or directriz.startswith("No aplica"):
            return

        partes = directriz.split("=")
        if len(partes) != 2:
            return

        variable = partes[0].strip()
        try:
            valor = float(partes[1].strip())
        except ValueError:
            return

        if variable == "x":
            self.ejes.axvline(x=valor, color="purple", linestyle="--", linewidth=1, label="Directriz")
        elif variable == "y":
            self.ejes.axhline(y=valor, color="purple", linestyle="--", linewidth=1, label="Directriz")

    def dibujar_asintotas(self, centro_x, centro_y, a2, b2):
        semieje_a = raiz_cuadrada(valor_absoluto(a2))
        semieje_b = raiz_cuadrada(valor_absoluto(b2))

        if semieje_a == 0:
            return

        pendiente = semieje_b / semieje_a
        puntos_x = [centro_x - 10 + i * 20 / 200 for i in range(201)]
        asintota_1 = [centro_y + pendiente * (x - centro_x) for x in puntos_x]
        asintota_2 = [centro_y - pendiente * (x - centro_x) for x in puntos_x]

        self.ejes.plot(puntos_x, asintota_1, color="gray", linestyle="--", linewidth=1, label="Asintotas")
        self.ejes.plot(puntos_x, asintota_2, color="gray", linestyle="--", linewidth=1)

    def dibujar(self, conica, elementos):
        self.ejes.clear()
        tipo = conica.tipo

        if tipo == "circunferencia":
            centro_x, centro_y = elementos["centro"]
            radio = elementos["radio"]

            if elementos.get("sin_grafica_real"):
                self.ejes.annotate("No real", (centro_x, centro_y), textcoords="offset points", xytext=(8, -12), fontsize=8)
                self.ejes.set_xlim(centro_x - 5, centro_x + 5)
                self.ejes.set_ylim(centro_y - 5, centro_y + 5)
            elif radio > 0:
                angulos = [2 * PI * i / 200 for i in range(201)]
                puntos_x = [centro_x + radio * coseno(angulo) for angulo in angulos]
                puntos_y = [centro_y + radio * seno(angulo) for angulo in angulos]
                self.ejes.plot(puntos_x, puntos_y, "b-", linewidth=2)
            else:
                self.ejes.annotate("Radio 0", (centro_x, centro_y), textcoords="offset points", xytext=(8, -12), fontsize=8)
                self.ejes.set_xlim(centro_x - 5, centro_x + 5)
                self.ejes.set_ylim(centro_y - 5, centro_y + 5)

            self.marcar_punto((centro_x, centro_y), "red", "Centro")

        elif tipo == "elipse":
            centro_x, centro_y = elementos["centro"]
            semieje_a = raiz_cuadrada(valor_absoluto(elementos["a2"])) or 1
            semieje_b = raiz_cuadrada(valor_absoluto(elementos["b2"])) or 1
            angulos = [2 * PI * i / 200 for i in range(201)]
            puntos_x = [centro_x + semieje_a * coseno(angulo) for angulo in angulos]
            puntos_y = [centro_y + semieje_b * seno(angulo) for angulo in angulos]
            self.ejes.plot(puntos_x, puntos_y, "g-", linewidth=2)
            self.marcar_punto((centro_x, centro_y), "red", "Centro")
            self.marcar_puntos(elementos.get("focos"), "purple", "F")

            if elementos["a2"] >= elementos["b2"]:
                vertices = [(centro_x + semieje_a, centro_y), (centro_x - semieje_a, centro_y)]
                covertices = [(centro_x, centro_y + semieje_b), (centro_x, centro_y - semieje_b)]
            else:
                vertices = [(centro_x, centro_y + semieje_b), (centro_x, centro_y - semieje_b)]
                covertices = [(centro_x + semieje_a, centro_y), (centro_x - semieje_a, centro_y)]

            self.marcar_puntos(vertices, "orange", "V")
            self.marcar_puntos(covertices, "brown", "C")

        elif tipo == "hiperbola":
            centro_x, centro_y = elementos["centro"]
            semieje_a = raiz_cuadrada(valor_absoluto(elementos["a2"])) or 1
            semieje_b = raiz_cuadrada(valor_absoluto(elementos["b2"])) or 1
            parametro_t = [i * 0.015 for i in range(-150, 151)]

            if conica.A > 0:
                # ramas izquierda y derecha
                rama_der_x = [centro_x + semieje_a * coseno_hiperbola(t) for t in parametro_t]
                rama_der_y = [centro_y + semieje_b * seno_hiperbola(t) for t in parametro_t]
                rama_izq_x = [centro_x - semieje_a * coseno_hiperbola(t) for t in parametro_t]
                rama_izq_y = [centro_y + semieje_b * seno_hiperbola(t) for t in parametro_t]
            else:
                # ramas superior e inferior
                rama_der_x = [centro_x + semieje_a * seno_hiperbola(t) for t in parametro_t]
                rama_der_y = [centro_y + semieje_b * coseno_hiperbola(t) for t in parametro_t]
                rama_izq_x = [centro_x + semieje_a * seno_hiperbola(t) for t in parametro_t]
                rama_izq_y = [centro_y - semieje_b * coseno_hiperbola(t) for t in parametro_t]

            self.ejes.plot(rama_der_x, rama_der_y, "m-", linewidth=2)
            self.ejes.plot(rama_izq_x, rama_izq_y, "m-", linewidth=2)
            self.marcar_punto((centro_x, centro_y), "red", "Centro")
            self.marcar_puntos(elementos.get("focos"), "purple", "F")
            self.marcar_puntos(elementos.get("vertices"), "orange", "V")
            self.dibujar_asintotas(centro_x, centro_y, elementos.get("a2"), elementos.get("b2"))

        elif tipo == "parabola":
            coef_A, coef_B, coef_C, coef_D, coef_E = conica.A, conica.B, conica.C, conica.D, conica.E
            valores = [i * 0.05 for i in range(-200, 201)]
            if coef_A != 0 and coef_B == 0 and coef_D != 0:
                puntos_x = valores
                puntos_y = [-(coef_A * x**2 + coef_C * x + coef_E) / coef_D for x in puntos_x]
                self.ejes.plot(puntos_x, puntos_y, color="orange", linewidth=2)
            elif coef_B != 0 and coef_A == 0 and coef_C != 0:
                puntos_y = valores
                puntos_x = [-(coef_B * y**2 + coef_D * y + coef_E) / coef_C for y in puntos_y]
                self.ejes.plot(puntos_x, puntos_y, color="orange", linewidth=2)

            self.marcar_punto(elementos.get("vertice"), "red", "Vertice")
            self.marcar_punto(elementos.get("foco"), "purple", "Foco")
            self.dibujar_directriz(elementos.get("directriz"))

        self.ejes.set_title(tipo.capitalize())
        self.ejes.set_aspect("equal", adjustable="datalim")
        self.ejes.grid(True, linestyle="--", alpha=0.4)
        self.ejes.axhline(0, color="gray", linewidth=0.5)
        self.ejes.axvline(0, color="gray", linewidth=0.5)
        etiquetas = self.ejes.get_legend_handles_labels()
        if etiquetas[0]:
            self.ejes.legend(loc="best", fontsize=8)
        self.figura.tight_layout()
        self.lienzo.draw()


class GraficoTramos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figura = Figure(figsize=(5, 5), dpi=100)
        self.ejes = self.figura.add_subplot(111)
        self.lienzo = FigureCanvasTkAgg(self.figura, master=self)
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.ejes.clear()
        self.lienzo.draw()

    def dibujar(self, analizador, resultado):
        self.ejes.clear()
        punto_critico = resultado["a"]
        caso = resultado["caso"]
        rango = 5

        if caso == "removible":
            puntos_x = [punto_critico + (i - 200) * rango / 200
                        for i in range(400)
                        if valor_absoluto((i - 200) * rango / 200) > 0.01]
            puntos_y = [analizador.evaluar(x) for x in puntos_x]
            self.ejes.plot(puntos_x, puntos_y, "b-", linewidth=2)
            valor_limite = punto_critico + analizador.d1
            self.ejes.plot(punto_critico, valor_limite, "o", color="white", markersize=8,
                          markeredgecolor="red", markeredgewidth=2)

        elif caso == "salto":
            puntos_x_izquierda = [punto_critico - rango + i * rango / 200 for i in range(200)]
            puntos_x_derecha = [punto_critico + i * rango / 200 for i in range(200)]
            valores_izquierda = [analizador.evaluar(x) for x in puntos_x_izquierda]
            valores_derecha = [analizador.evaluar(x) for x in puntos_x_derecha]
            self.ejes.plot(puntos_x_izquierda, valores_izquierda, "b-", linewidth=2)
            self.ejes.plot(puntos_x_derecha, valores_derecha, "g-", linewidth=2)
            #punto hueco
            limite_izquierda = punto_critico + analizador.d2
            self.ejes.plot(punto_critico, limite_izquierda, "o", color="white", markersize=8,
                          markeredgecolor="blue", markeredgewidth=2)
            #punto lleno
            valor_en_a = punto_critico + analizador.d4
            self.ejes.plot(punto_critico, valor_en_a, "go", markersize=8)

        elif caso == "infinita":
            puntos_x_izquierda = [punto_critico - rango + i * (rango - 0.1) / 200 for i in range(200)]
            puntos_x_derecha = [punto_critico + 0.1 + i * (rango - 0.1) / 200 for i in range(200)]
            valores_izquierda = [analizador.evaluar(x) for x in puntos_x_izquierda]
            valores_derecha = [analizador.evaluar(x) for x in puntos_x_derecha]
           
            #filtra valores muy grandes para que la grafica no se distorsione
            limite_visual = 50
            valores_izquierda = [y if y is not None and valor_absoluto(y) < limite_visual else None for y in valores_izquierda]
            valores_derecha = [y if y is not None and valor_absoluto(y) < limite_visual else None for y in valores_derecha]
            self.ejes.plot(puntos_x_izquierda, valores_izquierda, "b-", linewidth=2)
            self.ejes.plot(puntos_x_derecha, valores_derecha, "b-", linewidth=2)
            #linea de la asintota vertical
            self.ejes.axvline(x=punto_critico, color="red", linestyle="--", linewidth=1)

        self.ejes.set_title(resultado["nombre_caso"])
        self.ejes.grid(True, linestyle="--", alpha=0.4)
        self.ejes.axhline(0, color="gray", linewidth=0.5)
        self.ejes.axvline(0, color="gray", linewidth=0.5)
        self.figura.tight_layout()
        self.lienzo.draw()
