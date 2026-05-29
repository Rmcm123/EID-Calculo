from modulo_rut import AnalizadorRut, DigitoVerificador

class creador_ecuacion:
    def __init__(self, rut):
        self.rut = AnalizadorRut(rut)
        self.digitos = self.rut.obtener_digitos()
        self.calculo = DigitoVerificador.calcular(self.rut.cuerpo)
        self.v = self.rut.variable_v(self.calculo["dv_esperado"])
        self.es_valido = self.rut.es_valido(self.calculo)
        self.A, self.B, self.C, self.D, self.E, self.pasos_coeficientes = self.construir_coeficientes()
        self.tipo = self.clasificar_conica()

    def construir_coeficientes(self):
        d1, d2, d3, d4, d5, d6, d7, d8 = self.digitos
        v = self.v
        A = (d1 + d2) / v
        B = (d3 + d4) / v
        C = -(d5 + d6)
        D = -(d7 + d8)
        E = d1 + d3 + d5 + d7

        pasos = []
        pasos.append(f"A = (d1+d2)/v = ({d1}+{d2})/{v} = {A}")
        pasos.append(f"B = (d3+d4)/v = ({d3}+{d4})/{v} = {B}")
        pasos.append(f"C = -(d5+d6) = -({d5}+{d6}) = {C}")
        pasos.append(f"D = -(d7+d8) = -({d7}+{d8}) = {D}")
        pasos.append(f"E = d1+d3+d5+d7 = {d1}+{d3}+{d5}+{d7} = {E}")

        if d8 % 2 != 0:
            B = -B
            pasos.append(f"si d8 = {d8} es impar, B es reemplazado por -B = {B}")

        if d1 == d2:
            B = A
            pasos.append(f"d1 = d2 = {d1}, se impone B = A = {A}")

        if (d5 + d6) % 3 == 0:
            if d7 % 2 == 0:
                B = 0
                pasos.append(f"si (d5+d6) = {d5+d6} es múltiplo de 3 y d7 = {d7} es par, B = 0 (parábola vertical)")
            else:
                A = 0
                pasos.append(f"si (d5+d6) = {d5+d6} es múltiplo de 3 y d7 = {d7} es impar, A = 0 (parábola horizontal)")

        pasos.append(f"Ecuación general: {A}x² + {B}y² + ({C})x + ({D})y + {E} = 0")
        return A, B, C, D, E, pasos

    def clasificar_conica(self):
        A, B = self.A, self.B
        if A == B and A != 0:
            return "circunferencia"
        elif A != 0 and B != 0 and A != B:
            if (A > 0 and B > 0) or (A < 0 and B < 0):
                return "elipse"
            else:
                return "hiperbola"
        elif A == 0 or B == 0:
            return "parabola"

    def sqrt_manual(self, n):
        if n <= 0:
            return 0
        x = n
        for _ in range(100):
            x = (x + n / x) / 2
        return x

    def a_forma_canonica(self):
        A, B, C, D, E = self.A, self.B, self.C, self.D, self.E
        pasos = []
        pasos.append(f"Partimos de: {A}x² + {B}y² + ({C})x + ({D})y + {E} = 0")

        h = -C / (2 * A) if A != 0 else None
        k = -D / (2 * B) if B != 0 else None

        lado_derecho = 0
        if A != 0:
            termino_x = (C**2) / (4 * A)
            lado_derecho += termino_x
            pasos.append(f"Completar cuadrado en x: A(x + {-C/(2*A)})², se suma {termino_x} al lado derecho")
        if B != 0:
            termino_y = (D**2) / (4 * B)
            lado_derecho += termino_y
            pasos.append(f"Completar cuadrado en y: B(y + {-D/(2*B)})², se suma {termino_y} al lado derecho")

        lado_derecho -= E
        pasos.append(f"Restando E = {E}: lado derecho = {lado_derecho}")

        return h, k, lado_derecho, pasos

    def calcular_elementos(self):
        h, k, lado_derecho, pasos_canonicos = self.a_forma_canonica()
        tipo = self.tipo
        resultado = {"tipo": tipo, "pasos_canonicos": pasos_canonicos}

        if tipo == "circunferencia":
            r = self.sqrt_manual(lado_derecho / self.A)
            resultado["centro"] = (h, k)
            resultado["radio"] = r
            pasos_canonicos.append(f"Forma canónica: (x - {h})² + (y - {k})² = {round(r,4)}²")

        elif tipo == "elipse":
            a2 = lado_derecho / self.A
            b2 = lado_derecho / self.B
            if a2 >= b2:
                c = self.sqrt_manual(a2 - b2)
                focos = [(h + c, k), (h - c, k)]
                pasos_canonicos.append(f"Eje mayor horizontal: a² = {a2}, b² = {b2}")
            else:
                c = self.sqrt_manual(b2 - a2)
                focos = [(h, k + c), (h, k - c)]
                pasos_canonicos.append(f"Eje mayor vertical: a²={b2}, b²={a2}")
            resultado.update({"centro": (h, k), "a2": a2, "b2": b2, "c": c, "focos": focos})
            pasos_canonicos.append(f"Forma canónica: (x-{h})²/{a2} + (y-{k})²/{b2} = 1")

        elif tipo == "hiperbola":
            a2 = lado_derecho / self.A
            b2 = -(lado_derecho / self.B)
            c = self.sqrt_manual(a2 + b2)
            focos = [(h + c, k), (h - c, k)]
            resultado.update({"centro": (h, k), "a2": a2, "b2": b2, "c": c, "focos": focos})
            pasos_canonicos.append(f"Forma canónica: (x-{h})²/{a2} - (y-{k})²/{b2} = 1")

        elif tipo == "parabola":
            if self.A == 0:
                p = -self.D / (2 * self.B) if self.B != 0 else 0
                resultado.update({"vertice": (h, k), "p": p})
                pasos_canonicos.append(f"Parábola horizontal. Vértice: ({h}, {k})")
            else:
                p = -self.D / (2 * self.A) if self.A != 0 else 0
                resultado.update({"vertice": (h, k), "p": p})
                pasos_canonicos.append(f"Parábola vertical. Vértice: ({h}, {k})")

        return resultado

    def procedimiento_inverso(self, elementos):
        pasos = ["Procedimiento inverso: canónica a general"]
        tipo = self.tipo

        if tipo in ("circunferencia", "elipse"):
            h, k = elementos["centro"]
            pasos.append(f"Partimos de la forma canónica con centro ({h},{k})")
            pasos.append(f"Expandiendo (x-{h})²: x² - {2*h}x + {h**2}")
            pasos.append(f"Expandiendo (y-{k})²: y² - {2*k}y + {k**2}")
            pasos.append(f"Multiplicando por A={self.A} y B={self.B} respectivamente y reordenando:")
            pasos.append(f"Se obtiene: {self.A}x² + {self.B}y² + ({self.C})x + ({self.D})y + {self.E} = 0")

        elif tipo == "hiperbola":
            h, k = elementos["centro"]
            pasos.append(f"Partimos de la forma canónica hipérbola con centro ({h},{k})")
            pasos.append(f"Expandiendo y multiplicando por A = {self.A} y B = {self.B}:")
            pasos.append(f"Se obtiene: {self.A}x² + {self.B}y² + ({self.C})x + ({self.D})y + {self.E} = 0")

        elif tipo == "parabola":
            pasos.append(f"Expandiendo la forma canónica de la parábola:")
            pasos.append(f"Se obtiene: {self.A}x² + {self.B}y² + ({self.C})x + ({self.D})y + {self.E} = 0")

        return pasos
    
    def imprimir(self):
        elementos = self.calcular_elementos()
        print(f"RUT válido: {self.es_valido}")
        print(f"Tipo de cónica: {self.tipo}")
        print()
        print("Pasos construcción de coeficientes")
        for paso in self.pasos_coeficientes:
            print(" ", paso)
        print()
        elementos = self.calcular_elementos()
        print("Elementos geométricos")
        for clave, valor in elementos.items():
            if clave != "pasos_canonicos":
                print(f"  {clave}: {valor}")
        print()
        print("Pasos forma canónica")
        for paso in elementos["pasos_canonicos"]:
            print(" ", paso)
        print()
        print("Procedimiento inverso")
        for paso in self.procedimiento_inverso(elementos):
            print(" ", paso)

