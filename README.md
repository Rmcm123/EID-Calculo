# Calculadora Dígito Verificador (RUT)

Este proyecto es una herramienta en Python desarrollada para calcular y validar el dígito verificador de un RUT chileno (Rol Único Tributario) utilizando el algoritmo algorítmico tradicional de "Módulo 11".

## Archivos del Proyecto

- **`modulo_rut.py`**: Contiene la clase `DigitoVerificador` que encapsula la lógica matemática. Multiplica los dígitos de la serie (de derecha a izquierda) por la secuencia del 2 al 7, suma los productos, y calcula el dígito verificador. Retorna el resultado esperado junto con un desglose de las operaciones matemáticas para fácil depuración o presentación.
- **`main.py`**: Archivo principal destinado a levantar la interfaz gráfica de usuario. (Actualmente preparado con importaciones de `tkinter` y `customtkinter`).

## Cómo Funciona la Lógica Matemática (Módulo 11)

El algoritmo obtiene los dígitos del RUT e interviene al revés multiplicando cada dígito:
1. Multiplica los números secuencialmente tomando modificadores que van desde 2 hasta 7, reiniciándose una vez pasan el 7.
2. Suma todos estos productos obtenidos.
3. El resultado se divide utilizando el Módulo 11 (`suma_total % 11`). 
4. El dígito verificador se calcula como el remanente: `11 - resto`.
5. Se manejan las dos posibles excepciones del modelo:
   - Si el valor de resta es **11**, el dígito es **'0'**.
   - Si el valor de resta es **10**, el dígito es **'K'**.
   
## Uso

El archivo expone el método estático `DigitoVerificador.calcular(rut)` que recibe un string numérico y devuelve un diccionario con toda la información desglosada del cálculo, desde los productos por número hasta el resultado esperado final.