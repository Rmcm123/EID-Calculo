import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from modulo_conicas import creador_ecuacion
from modulo_funciones_tramos import AnalizadorFuncionTramos
from modulo_rut import AnalizadorRut, DigitoVerificador

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AplicacionCalculo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Cálculo - Analizador de RUT")
        self.geometry("1000x700")
        
        # --- TOP FRAME: Ingreso de RUT ---
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(pady=10, padx=10, fill="x")
        
        self.lbl_rut = ctk.CTkLabel(self.frame_top, text="Ingrese RUT (Ej: 12345678-9):", font=("Arial", 14, "bold"))
        self.lbl_rut.pack(side="left", padx=10)
        
        self.ent_rut = ctk.CTkEntry(self.frame_top, width=200)
        self.ent_rut.pack(side="left", padx=10)
        
        self.btn_analizar = ctk.CTkButton(self.frame_top, text="Analizar", command=self.analizar_rut)
        self.btn_analizar.pack(side="left", padx=10)
        
        self.lbl_estado = ctk.CTkLabel(self.frame_top, text="", text_color="red")
        self.lbl_estado.pack(side="left", padx=10)
        
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_conicas = self.tabs.add("Secciones Cónicas")
        self.tab_tramos = self.tabs.add("Funciones por Tramos")
        
        self._setup_tab_conicas()
        self._setup_tab_tramos()

    def _setup_tab_conicas(self):
        self.tab_conicas.columnconfigure(0, weight=1)
        self.tab_conicas.rowconfigure(0, weight=1)
        
        # Panel Izquierdo: Pasos
        self.txt_pasos_conicas = ctk.CTkTextbox(self.tab_conicas, wrap="word", font=("Arial", 14))
        self.txt_pasos_conicas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def _setup_tab_tramos(self):
        self.tab_tramos.columnconfigure(0, weight=1)
        self.tab_tramos.rowconfigure(0, weight=1)
        
        # Panel Izquierdo: Pasos y tabla
        self.txt_pasos_tramos = ctk.CTkTextbox(self.tab_tramos, wrap="word", font=("Arial", 14))
        self.txt_pasos_tramos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def limpiar_campos(self):
        self.txt_pasos_conicas.delete(1.0, "end")
        self.txt_pasos_tramos.delete(1.0, "end")

    def analizar_rut(self):
        rut_input = self.ent_rut.get()
        self.lbl_estado.configure(text="")
        self.limpiar_campos()
        
        try:
            # === CÓNICAS ===
            conica = creador_ecuacion(rut_input)
            
            if not conica.es_valido:
                self.lbl_estado.configure(text="RUT Inválido: DV incorrecto", text_color="red")
                return
            
            self.lbl_estado.configure(text="RUT Válido ✅", text_color="green")
            
            # Formatear texto cónicas para mostrar procedimiento
            texto_conica = "=== VALIDACIÓN RUT ===\n"
            calculo = DigitoVerificador.calcular(conica.rut.cuerpo)
            for d, m, p in calculo["desglose"]:
                texto_conica += f"{d} x {m} = {p}\n"
            texto_conica += f"Suma total = {calculo['suma_total']}\n"
            texto_conica += f"Resto = {calculo['resto']}\n"
            texto_conica += f"DV Esperado = {calculo['dv_esperado']}\n\n"
            
            texto_conica += "=== PASOS COEFICIENTES ===\n"
            for paso in conica.pasos_coeficientes:
                texto_conica += paso + "\n"
                
            texto_conica += "\n=== CONSTRUCCIÓN CANÓNICA ===\n"
            elementos = conica.calcular_elementos()
            for paso in elementos["pasos_canonicos"]:
                texto_conica += paso + "\n"
                
            texto_conica += "\n=== PROCEDIMIENTO INVERSO ===\n"
            for paso in conica.procedimiento_inverso(elementos):
                texto_conica += paso + "\n"

            self.txt_pasos_conicas.insert(1.0, texto_conica)
            
            # === FUNCIONES POR TRAMOS ===
            analizador_tramos = AnalizadorFuncionTramos(conica.digitos)
            res_tramos = analizador_tramos.analizar()
            
            texto_tramos = f"Caso Seleccionado: {res_tramos['nombre_caso']}\n"
            texto_tramos += f"Regla (d8 % 3 = {res_tramos['residuo_d8_mod_3']})\n\n"
            texto_tramos += f"Función generada en torno a x = {res_tramos['a']}:\n"
            texto_tramos += f"{res_tramos['funcion']}\n\n"
            
            texto_tramos += "=== TABLA DE VALORES (EVIDENCIA COMPUTACIONAL) ===\n"
            texto_tramos += "x\t\tLado\t\tf(x)\n"
            texto_tramos += "-"*40 + "\n"
            for fila in res_tramos['tabla_valores']:
                texto_tramos += f"{fila['x']}\t{fila['lado']}\t{fila['f(x)']}\n"
                
            self.txt_pasos_tramos.insert(1.0, texto_tramos)

        except Exception as e:
            self.lbl_estado.configure(text=f"Error al procesar: {str(e)}", text_color="red")
            
if __name__ == "__main__":
    app = AplicacionCalculo()
    app.mainloop()

