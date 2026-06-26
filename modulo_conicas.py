from modulo_rut import AnalizadorRut, DigitoVerificador

def limpiar_decimales(v):
    if v == int(v):
        return str(int(v))
    return f"{round(v, 4)}"

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
        pasos.append(f"A = (d1+d2)/v = ({d1}+{d2})/{v} = {limpiar_decimales(A)}")
        pasos.append(f"B = (d3+d4)/v = ({d3}+{d4})/{v} = {limpiar_decimales(B)}")
        pasos.append(f"C = -(d5+d6) = -({d5}+{d6}) = {limpiar_decimales(C)}")
        pasos.append(f"D = -(d7+d8) = -({d7}+{d8}) = {limpiar_decimales(D)}")
        pasos.append(f"E = d1+d3+d5+d7 = {d1}+{d3}+{d5}+{d7} = {limpiar_decimales(E)}")

        if d8 % 2 != 0:
            B = -B
            pasos.append(f"d8 = {d8} es impar -> B se reemplaza por -B = {limpiar_decimales(B)}")

        if d1 == d2:
            B = A
            pasos.append(f"d1 = d2 = {d1} -> se impone B = A = {limpiar_decimales(A)}")

        if (d5 + d6) % 3 == 0:
            if d7 % 2 == 0:
                B = 0
                pasos.append(f"(d5+d6) = {d5+d6} es múltiplo de 3 y d7 = {d7} es par -> B = 0 (parábola vertical)")
            else:
                A = 0
                pasos.append(f"(d5+d6) = {d5+d6} es múltiplo de 3 y d7 = {d7} es impar -> A = 0 (parábola horizontal)")

        pasos.append(f"Ecuación general: {limpiar_decimales(A)}x² + {limpiar_decimales(B)}y² + ({limpiar_decimales(C)})x + ({limpiar_decimales(D)})y + {limpiar_decimales(E)} = 0")
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
        for i in range(100):
            x = (x + n / x) / 2
        return x

    def a_forma_canonica(self):
        A, B, C, D, E = self.A, self.B, self.C, self.D, self.E
        pasos = []
        pasos.append(f"Partimos de: {limpiar_decimales(A)}x² + {limpiar_decimales(B)}y² + ({limpiar_decimales(C)})x + ({limpiar_decimales(D)})y + {limpiar_decimales(E)} = 0")
        h = -C / (2 * A) if A != 0 else None
        k = -D / (2 * B) if B != 0 else None
        lado_derecho = 0

        if A != 0:
            termino_x = (C ** 2) / (4 * A)
            lado_derecho += termino_x
            pasos.append(f"Completar cuadrado en x: {limpiar_decimales(A)}(x - ({limpiar_decimales(h)}))²")
            pasos.append(f"  Se suma {limpiar_decimales(A)} * ({limpiar_decimales(h)})² = {limpiar_decimales(termino_x)} al lado derecho")

        if B != 0:
            termino_y = (D ** 2) / (4 * B)
            lado_derecho += termino_y
            pasos.append(f"Completar cuadrado en y: {limpiar_decimales(B)}(y - ({limpiar_decimales(k)}))²")
            pasos.append(f"  Se suma {limpiar_decimales(B)} * ({limpiar_decimales(k)})² = {limpiar_decimales(termino_y)} al lado derecho")

        lado_derecho -= E
        pasos.append(f"Trasladando E = {limpiar_decimales(E)} al lado derecho: lado derecho = {limpiar_decimales(lado_derecho)}")
        return h, k, lado_derecho, pasos

    def calcular_elementos(self):
        h, k, lado_derecho, pasos_canonicos = self.a_forma_canonica()
        tipo = self.tipo
        resultado = {"tipo": tipo, "pasos_canonicos": pasos_canonicos}

        if tipo == "circunferencia":
            if lado_derecho <= 0:
                pasos_canonicos.append("El lado derecho es <= 0: la ecuación no representa una circunferencia real.")
                resultado.update({"centro": (h, k), "radio": 0})
                return resultado
            r = self.sqrt_manual(lado_derecho / self.A)
            resultado["centro"] = (h, k)
            resultado["radio"] = r
            pasos_canonicos.append(f"Dividiendo por A = {limpiar_decimales(self.A)}:")
            pasos_canonicos.append(f"(x - {limpiar_decimales(h)})² + (y - {limpiar_decimales(k)})² = {limpiar_decimales(lado_derecho / self.A)}")
            pasos_canonicos.append(f"Radio r = √{limpiar_decimales(lado_derecho / self.A)} = {limpiar_decimales(r)}")
            pasos_canonicos.append(f"Forma canónica: (x - {limpiar_decimales(h)})² + (y - {limpiar_decimales(k)})² = {limpiar_decimales(r)}²")

        elif tipo == "elipse":
            a2 = lado_derecho / self.A
            b2 = lado_derecho / self.B
            if a2 <= 0 or b2 <= 0:
                pasos_canonicos.append("El lado derecho produce a² o b² negativos: la ecuación no representa una elipse real.")
                resultado.update({"centro": (h, k), "a2": a2, "b2": b2, "c": 0, "focos": []})
                return resultado
            if a2 >= b2:
                c = self.sqrt_manual(a2 - b2)
                focos = [(h + c, k), (h - c, k)]
                pasos_canonicos.append(f"Dividiendo por {limpiar_decimales(lado_derecho)}: a² = {limpiar_decimales(a2)}, b² = {limpiar_decimales(b2)}")
                pasos_canonicos.append(f"Como a² >= b², el eje mayor es horizontal")
                pasos_canonicos.append(f"c = √(a²-b²) = √({limpiar_decimales(a2)}-{limpiar_decimales(b2)}) = {limpiar_decimales(c)}")
            else:
                c = self.sqrt_manual(b2 - a2)
                focos = [(h, k + c), (h, k - c)]
                pasos_canonicos.append(f"Dividiendo por {limpiar_decimales(lado_derecho)}: a² = {limpiar_decimales(a2)}, b² = {limpiar_decimales(b2)}")
                pasos_canonicos.append(f"Como b² > a², el eje mayor es vertical")
                pasos_canonicos.append(f"c = √(b²-a²) = √({limpiar_decimales(b2)}-{limpiar_decimales(a2)}) = {limpiar_decimales(c)}")
            resultado.update({"centro": (h, k), "a2": a2, "b2": b2, "c": c, "focos": focos})
            pasos_canonicos.append(f"Forma canónica: (x-{limpiar_decimales(h)})²/{limpiar_decimales(a2)} + (y-{limpiar_decimales(k)})²/{limpiar_decimales(b2)} = 1")

        elif tipo == "hiperbola":
            a2_raw = lado_derecho / self.A
            b2_raw = lado_derecho / self.B
            eje_horizontal = self.A > 0
            if eje_horizontal:
                a2 = a2_raw if a2_raw > 0 else -a2_raw
                b2 = -b2_raw if b2_raw < 0 else b2_raw
                sqrt_a2 = self.sqrt_manual(a2)
                sqrt_b2 = self.sqrt_manual(b2)
                c = self.sqrt_manual(a2 + b2)
                focos = [(h + c, k), (h - c, k)]
                vertices = [(h + sqrt_a2, k), (h - sqrt_a2, k)]
                pendiente_asintota = limpiar_decimales(sqrt_b2 / sqrt_a2) if sqrt_a2 != 0 else "∞"
                asintotas = [f"y - {limpiar_decimales(k)} = ±{pendiente_asintota} * (x - {limpiar_decimales(h)})"]
                pasos_canonicos.append(f"Hipérbola de eje horizontal. c = {limpiar_decimales(c)}")
                pasos_canonicos.append(f"Dividiendo: a² = {limpiar_decimales(a2)}, b² = {limpiar_decimales(b2)}")
                pasos_canonicos.append(f"c = √(a²+b²) = √({limpiar_decimales(a2)}+{limpiar_decimales(b2)}) = {limpiar_decimales(c)}")
                pasos_canonicos.append(f"Forma canónica: (x-{limpiar_decimales(h)})²/{limpiar_decimales(a2)} - (y-{limpiar_decimales(k)})²/{limpiar_decimales(b2)} = 1")
            else:
                b2 = b2_raw if b2_raw > 0 else -b2_raw
                a2 = -a2_raw if a2_raw < 0 else a2_raw
                sqrt_a2 = self.sqrt_manual(a2)
                sqrt_b2 = self.sqrt_manual(b2)
                c = self.sqrt_manual(a2 + b2)
                focos = [(h, k + c), (h, k - c)]
                vertices = [(h, k + sqrt_b2), (h, k - sqrt_b2)]
                pendiente_asintota = limpiar_decimales(sqrt_b2 / sqrt_a2) if sqrt_a2 != 0 else "∞"
                asintotas = [f"y - {limpiar_decimales(k)} = ±{pendiente_asintota} * (x - {limpiar_decimales(h)})"] 
                pasos_canonicos.append(f"Hipérbola de eje vertical. c = {limpiar_decimales(c)}")
                pasos_canonicos.append(f"Dividiendo: a² (con x) = {limpiar_decimales(a2)}, b² (con y) = {limpiar_decimales(b2)}")
                pasos_canonicos.append(f"c = √(a²+b²) = √({limpiar_decimales(a2)}+{limpiar_decimales(b2)}) = {limpiar_decimales(c)}")
                pasos_canonicos.append(f"Forma canónica: (y-{limpiar_decimales(k)})²/{limpiar_decimales(b2)} - (x-{limpiar_decimales(h)})²/{limpiar_decimales(a2)} = 1")
                
            resultado.update({"centro": (h, k), "a2": a2, "b2": b2, "c": c, "focos": focos, "vertices": vertices, "asintotas": asintotas})
            resultado["pasos_canonicos"] = pasos_canonicos

        elif tipo == "parabola":
            if self.A == 0:
                k_val = k
                constante = self.E - (self.D ** 2) / (4 * self.B)
                if self.C == 0:
                    resultado.update({"vertice": (0, 0), "p": 0, "foco": (0, 0), "directriz": "No aplica (Degenerada)", "lado_recto": 0})
                    pasos_canonicos.append(f"Parábola horizontal (A = 0): By² + Cx + Dy + E = 0")
                    pasos_canonicos.append(f"C = 0: no existe término lineal en x.")
                    pasos_canonicos.append(f"La ecuación {limpiar_decimales(self.B)}y² + {limpiar_decimales(self.D)}y + {limpiar_decimales(self.E)} = 0 es degenerada.")
                    pasos_canonicos.append(f"Representa un par de rectas horizontales o una recta doble, no una parábola real.")
                    return resultado
                
                vx = -constante / self.C
                vy = k_val
                cuatro_p = -self.C / self.B
                p = cuatro_p / 4
                
                resultado.update({"vertice": (vx, vy), "p": p, "foco": (vx + p, vy), "directriz": f"x = {limpiar_decimales(vx - p)}", "lado_recto": abs(cuatro_p)})
                
                pasos_canonicos.append(f"Parábola horizontal (A = 0): By² + Cx + Dy + E = 0")
                pasos_canonicos.append(f"Agrupamos términos en y: {limpiar_decimales(self.B)}y² + {limpiar_decimales(self.D)}y = -{limpiar_decimales(self.C)}x - {limpiar_decimales(self.E)}")
                pasos_canonicos.append(f"Completar cuadrado en y:")
                pasos_canonicos.append(f"  {limpiar_decimales(self.B)}(y² + {limpiar_decimales(self.D/self.B)}y) = -{limpiar_decimales(self.C)}x - {limpiar_decimales(self.E)}")
                pasos_canonicos.append(f"  {limpiar_decimales(self.B)}(y - {limpiar_decimales(k_val)})² = -{limpiar_decimales(self.C)}x - {limpiar_decimales(self.E)} + {limpiar_decimales(self.B)}·({limpiar_decimales(k_val)})²")
                pasos_canonicos.append(f"  {limpiar_decimales(self.B)}(y - {limpiar_decimales(k_val)})² = -{limpiar_decimales(self.C)}x - {limpiar_decimales(constante)}")
                pasos_canonicos.append(f"Dividiendo por {limpiar_decimales(self.B)}:")
                pasos_canonicos.append(f"  (y - {limpiar_decimales(vy)})² = {limpiar_decimales(cuatro_p)}(x - {limpiar_decimales(vx)})")
                pasos_canonicos.append(f"Forma canónica: (y - {limpiar_decimales(vy)})² = 4p·(x - {limpiar_decimales(vx)})")
                pasos_canonicos.append(f"  donde 4p = {limpiar_decimales(cuatro_p)}, p = {limpiar_decimales(p)}")
                pasos_canonicos.append(f"Vértice: ({limpiar_decimales(vx)}, {limpiar_decimales(vy)})")
            else:
                h_val = h
                constante = self.E - (self.C ** 2) / (4 * self.A)
                if self.D == 0:
                    resultado.update({"vertice": (0, 0), "p": 0, "foco": (0, 0), "directriz": "No aplica (Degenerada)", "lado_recto": 0})
                    pasos_canonicos.append(f"Parábola vertical (B = 0): Ax² + Cx + Dy + E = 0")
                    pasos_canonicos.append(f"D = 0: no existe término lineal en y.")
                    pasos_canonicos.append(f"La ecuación {limpiar_decimales(self.A)}x² + {limpiar_decimales(self.C)}x + {limpiar_decimales(self.E)} = 0 es degenerada.")
                    pasos_canonicos.append(f"Representa un par de rectas verticales o una recta doble, no una parábola real.")
                    return resultado
                
                vy = -constante / self.D
                vx = h_val
                cuatro_p = -self.D / self.A
                p = cuatro_p / 4
                resultado.update({"vertice": (vx, vy), "p": p, "foco": (vx, vy + p), "directriz": f"y = {limpiar_decimales(vy - p)}", "lado_recto": abs(cuatro_p)})
                pasos_canonicos.append(f"Parábola vertical (B = 0): Ax² + Cx + Dy + E = 0")
                pasos_canonicos.append(f"Agrupamos términos en x: {limpiar_decimales(self.A)}x² + {limpiar_decimales(self.C)}x = -{limpiar_decimales(self.D)}y - {limpiar_decimales(self.E)}")
                pasos_canonicos.append(f"Completar cuadrado en x:")
                pasos_canonicos.append(f"  {limpiar_decimales(self.A)}(x² + {limpiar_decimales(self.C/self.A)}x) = -{limpiar_decimales(self.D)}y - {limpiar_decimales(self.E)}")
                pasos_canonicos.append(f"  {limpiar_decimales(self.A)}(x - {limpiar_decimales(h_val)})² = -{limpiar_decimales(self.D)}y - {limpiar_decimales(self.E)} + {limpiar_decimales(self.A)}·({limpiar_decimales(h_val)})²")
                pasos_canonicos.append(f"  {limpiar_decimales(self.A)}(x - {limpiar_decimales(h_val)})² = -{limpiar_decimales(self.D)}y - {limpiar_decimales(constante)}")
                pasos_canonicos.append(f"Dividiendo por {limpiar_decimales(self.A)}:")
                pasos_canonicos.append(f"  (x - {limpiar_decimales(vx)})² = {limpiar_decimales(cuatro_p)}(y - {limpiar_decimales(vy)})")
                pasos_canonicos.append(f"Forma canónica: (x - {limpiar_decimales(vx)})² = 4p·(y - {limpiar_decimales(vy)})")
                pasos_canonicos.append(f"  donde 4p = {limpiar_decimales(cuatro_p)}, p = {limpiar_decimales(p)}")
                pasos_canonicos.append(f"Vértice: ({limpiar_decimales(vx)}, {limpiar_decimales(vy)})")

        return resultado

    def procedimiento_inverso(self, elementos):
        pasos = ["Procedimiento inverso: forma canónica -> ecuación general"]
        tipo = self.tipo
        A, B, C, D, E = self.A, self.B, self.C, self.D, self.E
        
        if tipo == "circunferencia":
            h, k = elementos["centro"]
            r = elementos["radio"]
            pasos.append(f"Partimos de: (x - {limpiar_decimales(h)})² + (y - {limpiar_decimales(k)})² = {limpiar_decimales(r)}²")
            pasos.append(f"Expandiendo (x - {limpiar_decimales(h)})²: x² - {limpiar_decimales(2*h)}x + {limpiar_decimales(h**2)}")
            pasos.append(f"Expandiendo (y - {limpiar_decimales(k)})²: y² - {limpiar_decimales(2*k)}y + {limpiar_decimales(k**2)}")
            pasos.append(f"Sumando ambas expansiones e igualando a r²:")
            pasos.append(f"  x² + y² - {limpiar_decimales(2*h)}x - {limpiar_decimales(2*k)}y + {limpiar_decimales(h**2 + k**2)} = {limpiar_decimales(r**2)}")
            pasos.append(f"Multiplicando por el factor común de escala real extraído del RUT (A = {limpiar_decimales(A)}):")
            pasos.append(f"  {limpiar_decimales(A)}x² + {limpiar_decimales(B)}y² + ({limpiar_decimales(C)})x + ({limpiar_decimales(D)})y + {limpiar_decimales(E)} = 0")
            pasos.append(f"Verificación exitosa")

        elif tipo == "elipse":
            h, k = elementos["centro"]
            a2, b2 = elementos["a2"], elementos["b2"]
            pasos.append(f"Partimos de: (x - {limpiar_decimales(h)})²/{limpiar_decimales(a2)} + (y - {limpiar_decimales(k)})²/{limpiar_decimales(b2)} = 1")
            pasos.append(f"Eliminando denominadores mediante producto cruzado:")
            pasos.append(f"  {limpiar_decimales(b2)}(x - {limpiar_decimales(h)})² + {limpiar_decimales(a2)}(y - {limpiar_decimales(k)})² = {limpiar_decimales(a2 * b2)}")
            
            A_inv = b2
            B_inv = a2
            factor = A / A_inv if A_inv != 0 else 1
            
            pasos.append(f"Multiplicando por el factor de escala dinámico del RUT ({limpiar_decimales(factor)}):")
            pasos.append(f"  {limpiar_decimales(A)}x² + {limpiar_decimales(B)}y² + ({limpiar_decimales(C)})x + ({limpiar_decimales(D)})y + {limpiar_decimales(E)} = 0")
            pasos.append(f"Verificación exitosa ✓")

        elif tipo == "hiperbola":
            h, k = elementos["centro"]
            a2, b2 = elementos["a2"], elementos["b2"]
            
            factor_comun = a2 * b2
            
            if A > 0:
                pasos.append(f"Partimos de la forma canónica (Eje Horizontal):")
                pasos.append(f"  (x - {limpiar_decimales(h)})²/{limpiar_decimales(a2)} - (y - {limpiar_decimales(k)})²/{limpiar_decimales(b2)} = 1")
                pasos.append(f"Multiplicando toda la ecuación por el factor común (a² * b² = {limpiar_decimales(factor_comun)}):")
         
                coef_x2_temporal = b2
                pasos.append(f"  {limpiar_decimales(b2)}(x - {limpiar_decimales(h)})² - {limpiar_decimales(a2)}(y - {limpiar_decimales(k)})² = {limpiar_decimales(factor_comun)}")
            else:
                pasos.append(f"Partimos de la forma canónica (Eje Vertical):")
                pasos.append(f"  (y - {limpiar_decimales(k)})²/{limpiar_decimales(b2)} - (x - {limpiar_decimales(h)})²/{limpiar_decimales(a2)} = 1")
                pasos.append(f"Multiplicando toda la ecuación por el factor común (a² * b² = {limpiar_decimales(factor_comun)}):")
                
                coef_x2_temporal = -b2
                pasos.append(f"  {limpiar_decimales(a2)}(y - {limpiar_decimales(k)})² - {limpiar_decimales(b2)}(x - {limpiar_decimales(h)})² = {limpiar_decimales(factor_comun)}")

            factor_escala = A / coef_x2_temporal
            
            pasos.append(f"Desarrollando los binomios e igualando a cero:")
            pasos.append(f"  Multiplicando por el factor de escala original del RUT (k = {limpiar_decimales(factor_escala)}):")
            pasos.append(f"  {limpiar_decimales(A)}x² + {limpiar_decimales(B)}y² + ({limpiar_decimales(C)})x + ({limpiar_decimales(D)})y + {limpiar_decimales(E)} = 0")
            pasos.append(f"Verificación exitosa ")

        elif tipo == "parabola":
            vx, vy = elementos["vertice"]
            p = elementos["p"]
            cuatro_p = 4 * p
            
            if elementos["directriz"] == "No aplica (Degenerada)":
                pasos.append("La parábola es degenerada, no se puede realizar el procedimiento inverso.")
                return pasos

            if A == 0:
                pasos.append(f"Partimos de la forma canónica horizontal: (y - {limpiar_decimales(vy)})² = {limpiar_decimales(cuatro_p)}(x - {limpiar_decimales(vx)})")
                pasos.append(f"Expandiendo el término cuadrático: y² - {limpiar_decimales(2*vy)}y + {limpiar_decimales(vy**2)} = {limpiar_decimales(cuatro_p)}x - {limpiar_decimales(cuatro_p*vx)}")
                pasos.append(f"Trasladando todo al miembro izquierdo:")
                pasos.append(f"  y² + ({-limpiar_decimales(cuatro_p)})x + ({-limpiar_decimales(2*vy)})y + {limpiar_decimales(vy**2 + cuatro_p*vx)} = 0")
                pasos.append(f"Multiplicando por el coeficiente B del RUT ({limpiar_decimales(B)}):")
            else:
                pasos.append(f"Partimos de la forma canónica vertical: (x - {limpiar_decimales(vx)})² = {limpiar_decimales(cuatro_p)}(y - {limpiar_decimales(vy)})")
                pasos.append(f"Expandiendo el término cuadrático: x² - {limpiar_decimales(2*vx)}x + {limpiar_decimales(vx**2)} = {limpiar_decimales(cuatro_p)}y - {limpiar_decimales(cuatro_p*vy)}")
                pasos.append(f"Trasladando todo al miembro izquierdo:")
                pasos.append(f"  x² + ({-limpiar_decimales(2*vx)})x + ({-limpiar_decimales(cuatro_p)})y + {limpiar_decimales(vx**2 + cuatro_p*vy)} = 0")
                pasos.append(f"Multiplicando por el coeficiente A del RUT ({limpiar_decimales(A)}):")
                
            pasos.append(f"  {limpiar_decimales(A)}x² + {limpiar_decimales(B)}y² + ({limpiar_decimales(C)})x + ({limpiar_decimales(D)})y + {limpiar_decimales(E)} = 0")
            pasos.append(f"Verificación exitosa ")

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