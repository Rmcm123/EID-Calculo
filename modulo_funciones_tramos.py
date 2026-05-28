class AnalizadorFuncionTramos:
    def __init__(self, digitos):
        self.digitos = self.validar_digitos(digitos)

        self.d1 = self.digitos[0]
        self.d2 = self.digitos[1]
        self.d3 = self.digitos[2]
        self.d4 = self.digitos[3]
        self.d5 = self.digitos[4]
        self.d8 = self.digitos[7]

        self.a = self.d3
        self.residuo = self.d8 % 3
        self.caso = self.seleccionar_caso()

    def validar_digitos(self, digitos):
        if len(digitos) != 8:
            raise ValueError("La funcion por tramos necesita exactamente 8 digitos del RUT.")

        for digito in digitos:
            if not isinstance(digito, int):
                raise ValueError("Todos los digitos del RUT deben ser numeros enteros.")
            if digito < 0 or digito > 9:
                raise ValueError("Cada digito del RUT debe estar entre 0 y 9.")

        return digitos

    def seleccionar_caso(self):
        if self.residuo == 0:
            return "removible"
        elif self.residuo == 1:
            return "salto"
        else:
            return "infinita"

    def analizar(self):
        if self.caso == "removible":
            resultado = self.analizar_removible()
        elif self.caso == "salto":
            resultado = self.analizar_salto()
        else:
            resultado = self.analizar_infinita()

        resultado["digitos"] = self.digitos
        resultado["a"] = self.a
        resultado["d8"] = self.d8
        resultado["residuo_d8_mod_3"] = self.residuo
        resultado["regla_seleccion"] = self.texto_regla_seleccion()
        resultado["tabla_valores"] = self.generar_tabla_valores()
        resultado["puntos_criticos"] = self.obtener_puntos_criticos()

        return resultado

    def analizar_removible(self):
        limite = self.a + self.d1

        return {
            "caso": "removible",
            "nombre_caso": "Discontinuidad removible",
            "funcion": "f(x) = ((x - {a})(x + {d1})) / (x - {a}), con x != {a}".format(
                a=self.a,
                d1=self.d1
            ),
            "funcion_simplificada": "f(x) = x + {d1}, con x != {a}".format(
                d1=self.d1,
                a=self.a
            ),
            "limite_izquierda": limite,
            "limite_derecha": limite,
            "limite_existe": True,
            "limite": limite,
            "valor_en_a": None,
            "funcion_definida_en_a": False,
            "es_continua": False,
            "tipo_discontinuidad": "Discontinuidad removible",
            "justificacion": (
                "El factor (x - a) aparece arriba y abajo. "
                "Si x es distinto de a, se puede simplificar y queda x + d1. "
                "Por eso el limite por ambos lados vale {limite}, "
                "pero la funcion original no esta definida en x = {a}."
            ).format(limite=limite, a=self.a)
        }

    def analizar_salto(self):
        limite_izquierda = self.a + self.d2
        limite_derecha = self.a + self.d4
        valor_en_a = limite_derecha

        limite_existe = limite_izquierda == limite_derecha
        es_continua = limite_existe and valor_en_a == limite_izquierda

        if limite_existe:
            tipo = "No presenta discontinuidad en el punto critico"
            justificacion = (
                "El modelo elegido es el de salto, pero en este caso los dos tramos "
                "llegan al mismo valor. El limite por izquierda, el limite por derecha "
                "y f(a) valen {limite}."
            ).format(limite=limite_izquierda)
        else:
            tipo = "Discontinuidad de salto"
            justificacion = (
                "Por la izquierda la funcion se acerca a a + d2 = {izquierda}. "
                "Por la derecha se acerca a a + d4 = {derecha}. "
                "Como esos valores son distintos, el limite no existe."
            ).format(izquierda=limite_izquierda, derecha=limite_derecha)

        return {
            "caso": "salto",
            "nombre_caso": "Discontinuidad de salto",
            "funcion": "f(x) = x + {d2}, si x < {a}; f(x) = x + {d4}, si x >= {a}".format(
                d2=self.d2,
                d4=self.d4,
                a=self.a
            ),
            "limite_izquierda": limite_izquierda,
            "limite_derecha": limite_derecha,
            "limite_existe": limite_existe,
            "limite": limite_izquierda if limite_existe else None,
            "valor_en_a": valor_en_a,
            "funcion_definida_en_a": True,
            "es_continua": es_continua,
            "tipo_discontinuidad": tipo,
            "justificacion": justificacion
        }

    def analizar_infinita(self):
        numerador = self.d5 + 1

        return {
            "caso": "infinita",
            "nombre_caso": "Discontinuidad infinita",
            "funcion": "f(x) = ({numerador}) / (x - {a})".format(
                numerador=numerador,
                a=self.a
            ),
            "limite_izquierda": "-infinito",
            "limite_derecha": "+infinito",
            "limite_existe": False,
            "limite": None,
            "valor_en_a": None,
            "funcion_definida_en_a": False,
            "es_continua": False,
            "tipo_discontinuidad": "Discontinuidad infinita",
            "asintota_vertical": "x = {a}".format(a=self.a),
            "justificacion": (
                "El denominador x - a se hace cero cuando x = {a}. "
                "Como d5 + 1 = {numerador}, al acercarse por la izquierda "
                "la funcion baja sin limite y por la derecha sube sin limite. "
                "Por eso hay una asintota vertical en x = {a}."
            ).format(a=self.a, numerador=numerador)
        }

    def evaluar(self, x):
        if self.caso == "removible":
            return self.evaluar_removible(x)
        elif self.caso == "salto":
            return self.evaluar_salto(x)
        else:
            return self.evaluar_infinita(x)

    def evaluar_removible(self, x):
        if self.son_iguales(x, self.a):
            return None
        return x + self.d1

    def evaluar_salto(self, x):
        if x < self.a:
            return x + self.d2
        else:
            return x + self.d4

    def evaluar_infinita(self, x):
        if self.son_iguales(x, self.a):
            return None
        return (self.d5 + 1) / (x - self.a)

    def generar_tabla_valores(self):
        desplazamientos = [-1, -0.1, -0.01, -0.001, 0.001, 0.01, 0.1, 1]
        tabla = []

        for desplazamiento in desplazamientos:
            x = self.a + desplazamiento

            fila = {
                "x": self.redondear(x),
                "lado": "izquierda" if x < self.a else "derecha",
                "f(x)": self.formatear_valor(self.evaluar(x))
            }

            tabla.append(fila)

        return tabla

    def obtener_puntos_criticos(self):
        if self.caso == "removible":
            motivo = "El denominador se anula y la funcion original no esta definida."
        elif self.caso == "salto":
            motivo = "En este punto cambia la definicion del tramo."
        else:
            motivo = "El denominador se anula y aparece una asintota vertical."

        return [{
            "x": self.a,
            "motivo": motivo
        }]

    def texto_regla_seleccion(self):
        if self.residuo == 0:
            conclusion = "se genera el caso de discontinuidad removible"
        elif self.residuo == 1:
            conclusion = "se genera el caso de discontinuidad de salto"
        else:
            conclusion = "se genera el caso de discontinuidad infinita"

        return "Como d8 = {d8} y {d8} mod 3 = {residuo}, {conclusion}.".format(
            d8=self.d8,
            residuo=self.residuo,
            conclusion=conclusion
        )

    def formatear_valor(self, valor):
        if valor is None:
            return "No definida"
        return self.redondear(valor)

    def redondear(self, valor):
        valor_redondeado = round(valor, 6)

        if int(valor_redondeado) == valor_redondeado:
            return int(valor_redondeado)

        return valor_redondeado

    def son_iguales(self, x, y):
        diferencia = x - y

        if diferencia < 0:
            diferencia = diferencia * -1

        return diferencia < 0.0000001
