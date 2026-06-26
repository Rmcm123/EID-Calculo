class DigitoVerificador:

    @staticmethod
    def calcular(rut: str) -> dict:
        suma_total = 0
        multiplicador = 2
        desglose_operacion = []
        for digito in reversed(rut):
            producto = int(digito) * multiplicador
            desglose_operacion.append((int(digito), multiplicador, producto))
            suma_total += producto
            multiplicador = 2 if multiplicador == 7 else multiplicador +1

        resto = suma_total % 11
        resultado_resta = 11 - resto

        dv_esperado = DigitoVerificador._determinar_dv(resultado_resta)

        return {
            "desglose": desglose_operacion,
            "suma_total": suma_total,
            "resto": resto,
            "resultado_resta": resultado_resta,
            "dv_esperado": dv_esperado
        }

  
    @staticmethod
    def _determinar_dv(resultado_resta: int) -> str:
        if resultado_resta == 11:
            return "0"
        elif resultado_resta == 10:
            return "K"
        return str(resultado_resta)
    

class AnalizadorRut:
    def __init__(self, rut_completo: str):
        self.rut_completo = rut_completo.strip()
        if "-" in self.rut_completo:
            partes = self.rut_completo.split("-")
            if len(partes) != 2 or len(partes[1].strip()) != 1:
                raise ValueError("Debe haber un digito o 'K' despues del guion.")
                
        self.rut_limpio = self._limpiar_rut(self.rut_completo).replace(" ", "")
        self.cuerpo, self.dv_ingresado = self._split_rut()
        self.validar_cuerpo()
    
    def _limpiar_rut(self, rut: str) -> str:
        return rut.replace(".", "").replace("-", "").upper()
    
    def _split_rut(self) -> tuple[str, str]:
        if len(self.rut_limpio) < 6:
            raise ValueError("El RUT ingresado es demasiado corto.")
        elif len(self.rut_limpio) > 9:
            raise ValueError("El RUT ingresado es demasiado largo.")
        return self.rut_limpio[:-1].zfill(8), self.rut_limpio[-1]

    def validar_cuerpo(self) -> None:
        if not self.cuerpo.isdigit():
            raise ValueError("El cuerpo del RUT debe contener solo digitos.")
    
    def obtener_digitos(self) -> list[int]:
        return [int(d) for d in self.cuerpo]
    
    def es_valido(self, resultado_calculo: dict) -> bool:
        return resultado_calculo["dv_esperado"] == self.dv_ingresado
    
    def variable_v(self, dv_esperado: str) -> int:
        if dv_esperado == "K":
            return 10
        elif dv_esperado == "0":
            return 11
        return int(dv_esperado)
