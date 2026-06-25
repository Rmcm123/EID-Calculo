DESPLAZAMIENTOS = [-1, -0.1, -0.01, -0.001, 0.001, 0.01, 0.1, 1]
TOLERANCIA = 0.0000001


class AnalizadorFuncionTramos:
    def __init__(self, digitos):
        self.digitos = self.validar_digitos(digitos)

        self.d1, self.d2, self.d3, self.d4, self.d5 = self.digitos[:5]
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

        resultado.update({
            "digitos": self.digitos,
            "a": self.a,
            "d8": self.d8,
            "residuo_d8_mod_3": self.residuo,
            "regla_seleccion": self.texto_regla_seleccion(),
            "tabla_valores": self.generar_tabla_valores(),
            "puntos_criticos": self.obtener_puntos_criticos()
        })

        return resultado

    def pasos_inicio(self, funcion):
        return [
            self.texto_regla_seleccion(),
            f"El punto de analisis es a = d3 = {self.a}.",
            f"La funcion generada es {funcion}."
        ]

    def analizar_removible(self):
        limite = self.a + self.d1
        funcion_original = f"f(x) = ((x - {self.a})(x + {self.d1})) / (x - {self.a}), con x != {self.a}"
        funcion_simplificada = f"f(x) = x + {self.d1}, con x != {self.a}"

        procedimiento = self.pasos_inicio(funcion_original) + [
            f"Para x distinto de {self.a}, se cancela el factor comun (x - {self.a}).",
            f"La expresion simplificada queda {funcion_simplificada}.",
            f"Limite por izquierda = a + d1 = {self.a} + {self.d1} = {limite}.",
            f"Limite por derecha = a + d1 = {self.a} + {self.d1} = {limite}.",
            f"Como ambos limites laterales son iguales, el limite existe y vale {limite}.",
            f"La funcion original no esta definida en x = {self.a}, por eso no es continua en el punto.",
            "La discontinuidad es removible porque el limite existe, pero f(a) no existe."
        ]

        return {
            "caso": "removible",
            "nombre_caso": "Discontinuidad removible",
            "funcion": funcion_original,
            "funcion_simplificada": funcion_simplificada,
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
                f"Por eso el limite por ambos lados vale {limite}, "
                f"pero la funcion original no esta definida en x = {self.a}."
            ),
            "procedimiento": procedimiento
        }

    def analizar_salto(self):
        limite_izquierda = self.a + self.d2
        limite_derecha = self.a + self.d4
        valor_en_a = limite_derecha
        funcion = f"f(x) = x + {self.d2}, si x < {self.a}; f(x) = x + {self.d4}, si x >= {self.a}"

        limite_existe = limite_izquierda == limite_derecha
        es_continua = limite_existe and valor_en_a == limite_izquierda

        if limite_existe:
            tipo = "No presenta discontinuidad en el punto critico"
            justificacion = (
                "El modelo elegido es el de salto, pero en este caso los dos tramos "
                "llegan al mismo valor. El limite por izquierda, el limite por derecha "
                f"y f(a) valen {limite_izquierda}."
            )
            conclusion_limite = "Como ambos limites laterales son iguales, el limite existe."
            conclusion_continuidad = f"Como f(a) coincide con el limite, la funcion es continua en x = {self.a}."
        else:
            tipo = "Discontinuidad de salto"
            justificacion = (
                f"Por la izquierda la funcion se acerca a a + d2 = {limite_izquierda}. "
                f"Por la derecha se acerca a a + d4 = {limite_derecha}. "
                "Como esos valores son distintos, el limite no existe."
            )
            conclusion_limite = "Como los limites laterales son distintos, el limite no existe."
            conclusion_continuidad = f"Como el limite no existe, la funcion no es continua en x = {self.a}."

        procedimiento = self.pasos_inicio(funcion) + [
            f"Para x < {self.a}, se usa f(x) = x + d2.",
            f"Limite por izquierda = a + d2 = {self.a} + {self.d2} = {limite_izquierda}.",
            f"Para x >= {self.a}, se usa f(x) = x + d4.",
            f"Limite por derecha = a + d4 = {self.a} + {self.d4} = {limite_derecha}.",
            conclusion_limite,
            f"f(a) = a + d4 = {self.a} + {self.d4} = {valor_en_a}.",
            conclusion_continuidad,
            f"Clasificacion: {tipo}."
        ]

        return {
            "caso": "salto",
            "nombre_caso": tipo,
            "modelo_generado": "Discontinuidad de salto",
            "funcion": funcion,
            "limite_izquierda": limite_izquierda,
            "limite_derecha": limite_derecha,
            "limite_existe": limite_existe,
            "limite": limite_izquierda if limite_existe else None,
            "valor_en_a": valor_en_a,
            "funcion_definida_en_a": True,
            "es_continua": es_continua,
            "tipo_discontinuidad": tipo,
            "justificacion": justificacion,
            "procedimiento": procedimiento
        }

    def analizar_infinita(self):
        numerador = self.d5 + 1
        funcion = f"f(x) = ({numerador}) / (x - {self.a})"

        procedimiento = self.pasos_inicio(funcion) + [
            f"Al evaluar x = {self.a}, el denominador x - a queda igual a cero.",
            f"Como d5 + 1 = {numerador}, el numerador es positivo y no se anula.",
            f"Cuando x se acerca a {self.a} por la izquierda, x - a es negativo y tiende a 0.",
            "Por eso el limite por izquierda es -infinito.",
            f"Cuando x se acerca a {self.a} por la derecha, x - a es positivo y tiende a 0.",
            "Por eso el limite por derecha es +infinito.",
            "Como los limites laterales son infinitos y no coinciden como numero real, el limite no existe.",
            f"La funcion no esta definida en x = {self.a}, por eso no es continua en el punto.",
            f"La discontinuidad es infinita y la asintota vertical es x = {self.a}."
        ]

        return {
            "caso": "infinita",
            "nombre_caso": "Discontinuidad infinita",
            "funcion": funcion,
            "limite_izquierda": "-infinito",
            "limite_derecha": "+infinito",
            "limite_existe": False,
            "limite": None,
            "valor_en_a": None,
            "funcion_definida_en_a": False,
            "es_continua": False,
            "tipo_discontinuidad": "Discontinuidad infinita",
            "asintota_vertical": f"x = {self.a}",
            "justificacion": (
                f"El denominador x - a se hace cero cuando x = {self.a}. "
                f"Como d5 + 1 = {numerador}, al acercarse por la izquierda "
                "la funcion baja sin limite y por la derecha sube sin limite. "
                f"Por eso hay una asintota vertical en x = {self.a}."
            ),
            "procedimiento": procedimiento
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
        tabla = []

        for desplazamiento in DESPLAZAMIENTOS:
            x = self.a + desplazamiento
            valor = self.evaluar(x)
            valor_formateado = self.formatear_valor(valor)

            fila = {
                "x": self.redondear(x),
                "valor": valor,
                "valor_formateado": valor_formateado,
                "lado": "izquierda" if x < self.a else "derecha",
                "f(x)": valor_formateado
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

        return diferencia < TOLERANCIA