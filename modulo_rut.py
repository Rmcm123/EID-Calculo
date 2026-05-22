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
    def _determinar_dv(resultado_resta):
        if resultado_resta == 11:
            return 0
        elif resultado_resta == 10:
            return "K"
        return str(resultado_resta)
    
