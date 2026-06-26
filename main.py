import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from modulo_conicas import creador_ecuacion
from modulo_funciones_tramos import AnalizadorFuncionTramos
from modulo_rut import AnalizadorRut, DigitoVerificador
from grafico import GraficoConicas, GraficoTramos

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
        self.tab_conicas.columnconfigure(1, weight=1)
        self.tab_conicas.rowconfigure(0, weight=1)
        
        # contenedor izquierdo para boton + textbox
        self.frame_izq_conicas = ctk.CTkFrame(self.tab_conicas)
        self.frame_izq_conicas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_izq_conicas.rowconfigure(1, weight=1)
        self.frame_izq_conicas.columnconfigure(0, weight=1)

        # boton para mostrar/ocultar procedimientos
        self.procedimientos_visibles = False
        self.btn_toggle_procedimientos = ctk.CTkButton(
            self.frame_izq_conicas,
            text="Mostrar Procedimientos",
            command=self._toggle_procedimientos,
            font=("Arial", 13, "bold"),
            height=38
        )
        # no se muestra hasta que se analice un RUT

        # pasos (oculto por defecto)
        self.txt_pasos_conicas = ctk.CTkTextbox(self.frame_izq_conicas, wrap="word", font=("Arial", 12))
        self._configurar_estilos(self.txt_pasos_conicas)

        # grafica
        self.grafico_conicas = GraficoConicas(self.tab_conicas)
        self.grafico_conicas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def _toggle_procedimientos(self):
        if self.procedimientos_visibles:
            self.txt_pasos_conicas.grid_forget()
            self.btn_toggle_procedimientos.configure(text="Mostrar Procedimientos")
            self.procedimientos_visibles = False
        else:
            self.txt_pasos_conicas.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
            self.btn_toggle_procedimientos.configure(text="Ocultar Procedimientos")
            self.procedimientos_visibles = True

    def _setup_tab_tramos(self):
        self.tab_tramos.columnconfigure(0, weight=1)
        self.tab_tramos.columnconfigure(1, weight=1)
        self.tab_tramos.rowconfigure(0, weight=1)
        
        # pasos y tabla
        self.txt_pasos_tramos = ctk.CTkTextbox(self.tab_tramos, wrap="word", font=("Arial", 12))
        self.txt_pasos_tramos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self._configurar_estilos(self.txt_pasos_tramos)

        # grafica
        self.grafico_tramos = GraficoTramos(self.tab_tramos)
        self.grafico_tramos.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # campos vacios para completar manualmente
        self.frame_respuestas_tramos = ctk.CTkFrame(self.tab_tramos)
        self.frame_respuestas_tramos.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))

        for columna in range(4):
            self.frame_respuestas_tramos.columnconfigure(columna, weight=1)

        ctk.CTkLabel(self.frame_respuestas_tramos, text="Analisis manual", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=8, pady=(6, 2)
        )

        ctk.CTkLabel(self.frame_respuestas_tramos, text="Limite izquierda").grid(row=1, column=0, padx=5, sticky="w")
        ctk.CTkLabel(self.frame_respuestas_tramos, text="Limite derecha").grid(row=1, column=1, padx=5, sticky="w")
        ctk.CTkLabel(self.frame_respuestas_tramos, text="Existe limite").grid(row=1, column=2, padx=5, sticky="w")
        ctk.CTkLabel(self.frame_respuestas_tramos, text="f(a)").grid(row=1, column=3, padx=5, sticky="w")

        self.ent_limite_izq = ctk.CTkEntry(self.frame_respuestas_tramos)
        self.ent_limite_der = ctk.CTkEntry(self.frame_respuestas_tramos)
        self.ent_existe_limite = ctk.CTkEntry(self.frame_respuestas_tramos)
        self.ent_valor_a = ctk.CTkEntry(self.frame_respuestas_tramos)

        self.ent_limite_izq.grid(row=2, column=0, padx=5, pady=3, sticky="ew")
        self.ent_limite_der.grid(row=2, column=1, padx=5, pady=3, sticky="ew")
        self.ent_existe_limite.grid(row=2, column=2, padx=5, pady=3, sticky="ew")
        self.ent_valor_a.grid(row=2, column=3, padx=5, pady=3, sticky="ew")

        ctk.CTkLabel(self.frame_respuestas_tramos, text="Continuidad").grid(row=3, column=0, padx=5, sticky="w")
        ctk.CTkLabel(self.frame_respuestas_tramos, text="Tipo").grid(row=3, column=1, padx=5, sticky="w")
        ctk.CTkLabel(self.frame_respuestas_tramos, text="Justificacion").grid(row=3, column=2, columnspan=2, padx=5, sticky="w")

        self.ent_continuidad = ctk.CTkEntry(self.frame_respuestas_tramos)
        self.ent_tipo_discontinuidad = ctk.CTkEntry(self.frame_respuestas_tramos)
        self.ent_justificacion_limites = ctk.CTkEntry(self.frame_respuestas_tramos)

        self.ent_continuidad.grid(row=4, column=0, padx=5, pady=(3, 8), sticky="ew")
        self.ent_tipo_discontinuidad.grid(row=4, column=1, padx=5, pady=(3, 8), sticky="ew")
        self.ent_justificacion_limites.grid(row=4, column=2, columnspan=2, padx=5, pady=(3, 8), sticky="ew")

    def _configurar_estilos(self, textbox):
        tw = textbox._textbox
        tw.tag_configure("titulo", font=("Arial", 15, "bold"), foreground="#4FC3F7",
                         spacing1=10, spacing3=4)
        tw.tag_configure("subtitulo", font=("Arial", 13, "bold"), foreground="#81C784",
                         spacing1=6, spacing3=3)
        tw.tag_configure("separador", font=("Arial", 6), foreground="#555555")
        tw.tag_configure("normal", font=("Arial", 12), foreground="#D0D0D0",
                         spacing1=1, lmargin1=10, lmargin2=10)
        tw.tag_configure("math", font=("Consolas", 11), foreground="#FFD54F",
                         spacing1=1, lmargin1=10, lmargin2=10)
        tw.tag_configure("resultado", font=("Arial", 12, "bold"), foreground="#FF8A65",
                         spacing1=3, spacing3=2, lmargin1=10)
        tw.tag_configure("tabla_header", font=("Consolas", 11, "bold"), foreground="#90CAF9",
                         spacing1=2, lmargin1=10, lmargin2=10)
        tw.tag_configure("tabla_fila", font=("Consolas", 11), foreground="#B0BEC5",
                         lmargin1=10, lmargin2=10)
        tw.tag_configure("info", font=("Arial", 11), foreground="#80CBC4",
                         spacing1=1, lmargin1=10, lmargin2=10)

    def limpiar_campos(self):
        self.txt_pasos_conicas.delete(1.0, "end")
        self.txt_pasos_tramos.delete(1.0, "end")
        self.grafico_conicas.limpiar()
        self.grafico_tramos.limpiar()
        # ocultar boton y procedimientos al limpiar
        self.btn_toggle_procedimientos.grid_forget()
        self.txt_pasos_conicas.grid_forget()
        self.procedimientos_visibles = False
        self.btn_toggle_procedimientos.configure(text="Mostrar Procedimientos")

        campos_respuestas = [
            self.ent_limite_izq,
            self.ent_limite_der,
            self.ent_existe_limite,
            self.ent_valor_a,
            self.ent_continuidad,
            self.ent_tipo_discontinuidad,
            self.ent_justificacion_limites
        ]

        for campo in campos_respuestas:
            campo.delete(0, "end")

    def analizar_rut(self):
        rut_input = self.ent_rut.get()
        self.lbl_estado.configure(text="")
        self.limpiar_campos()
        
        try:
            # === CONICAS ===
            conica = creador_ecuacion(rut_input)
            
            if not conica.es_valido:
                self.lbl_estado.configure(text="RUT Inválido: DV incorrecto", text_color="red")
                return
            
            self.lbl_estado.configure(text="RUT Válido", text_color="green")
            
            # mostrar boton de procedimientos
            self.btn_toggle_procedimientos.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 5))
            
            # Formatear texto conicas con estilos visuales
            txt = self.txt_pasos_conicas
            
            txt.insert("end", " VALIDACION DEL RUT\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            
            calculo = DigitoVerificador.calcular(conica.rut.cuerpo)
            txt.insert("end", " Desglose de multiplicaciones:\n", "subtitulo")
            for d, m, p in calculo["desglose"]:
                txt.insert("end", f"   {d}  x  {m}  =  {p}\n", "tabla_fila")
            
            txt.insert("end", "\n", "normal")
            txt.insert("end", f" Suma total = {calculo['suma_total']}\n", "resultado")
            txt.insert("end", f" Resto = {calculo['resto']}\n", "resultado")
            txt.insert("end", f" DV Esperado = {calculo['dv_esperado']}\n\n", "resultado")
            
            txt.insert("end", " COEFICIENTES DE LA ECUACION\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            
            for paso in conica.pasos_coeficientes:
                txt.insert("end", f" {paso}\n", "math")
            
            txt.insert("end", "\n", "normal")
            txt.insert("end", " CONSTRUCCION CANONICA\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            
            elementos = conica.calcular_elementos()
            for paso in elementos["pasos_canonicos"]:
                txt.insert("end", f" {paso}\n", "math")
            
            txt.insert("end", "\n", "normal")
            txt.insert("end", " PROCEDIMIENTO INVERSO\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            
            for paso in conica.procedimiento_inverso(elementos):
                txt.insert("end", f" {paso}\n", "math")
            
            # Dibujar grafica de la conica
            self.grafico_conicas.dibujar(conica, elementos)
            
            # === FUNCIONES POR TRAMOS ===
            analizador_tramos = AnalizadorFuncionTramos(conica.digitos)
            res_tramos = analizador_tramos.analizar()
            
            txt = self.txt_pasos_tramos
            
            txt.insert("end", " FUNCION POR TRAMOS\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            
            txt.insert("end", f" Caso: {res_tramos['nombre_caso']}\n", "resultado")
            txt.insert("end", f" Regla: d8 mod 3 = {res_tramos['residuo_d8_mod_3']}\n\n", "info")
            
            txt.insert("end", " Funcion generada:\n", "subtitulo")
            txt.insert("end", f" Punto critico:  x = {res_tramos['a']}\n", "normal")
            for punto in res_tramos["puntos_criticos"]:
                txt.insert("end", f" Motivo: {punto['motivo']}\n", "normal")
            txt.insert("end", f" {res_tramos['funcion']}\n\n", "math")

            txt.insert("end", " PROCEDIMIENTO MATEMATICO\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")

            for paso in res_tramos["procedimiento"]:
                txt.insert("end", f" {paso}\n", "math")

            txt.insert("end", "\n", "normal")

            valor_en_a = res_tramos["valor_en_a"]
            if valor_en_a is None:
                valor_en_a = "No definida"

            if res_tramos["limite_existe"]:
                existe_limite = "Si"
            else:
                existe_limite = "No"

            if res_tramos["es_continua"]:
                continuidad = "Si"
            else:
                continuidad = "No"

            txt.insert("end", " RESUMEN FINAL\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            txt.insert("end", f" Limite por izquierda: {res_tramos['limite_izquierda']}\n", "resultado")
            txt.insert("end", f" Limite por derecha: {res_tramos['limite_derecha']}\n", "resultado")
            txt.insert("end", f" Existe el limite: {existe_limite}\n", "resultado")
            txt.insert("end", f" Valor de f(a): {valor_en_a}\n", "resultado")
            txt.insert("end", f" Es continua en x = {res_tramos['a']}: {continuidad}\n", "resultado")
            txt.insert("end", f" Tipo: {res_tramos['tipo_discontinuidad']}\n", "resultado")
            txt.insert("end", f" Justificacion: {res_tramos['justificacion']}\n\n", "info")
            
            txt.insert("end", " EVIDENCIA COMPUTACIONAL\n", "titulo")
            txt.insert("end", " " + "\u2500" * 38 + "\n\n", "separador")
            
            txt.insert("end", f" {'x':>10}  {'Lado':>10}  {'f(x)':>12}\n", "tabla_header")
            txt.insert("end", " " + "\u2500" * 36 + "\n", "separador")
            for fila in res_tramos['tabla_valores']:
                txt.insert("end", f" {str(fila['x']):>10}  {fila['lado']:>10}  {str(fila['f(x)']):>12}\n", "tabla_fila")
            
            # Dibujar grafica de la funcion por tramos
            self.grafico_tramos.dibujar(analizador_tramos, res_tramos)

        except Exception as e:
            self.lbl_estado.configure(text=f"Error al procesar: {str(e)}", text_color="red")
            
if __name__ == "__main__":
    app = AplicacionCalculo()
    app.mainloop()
