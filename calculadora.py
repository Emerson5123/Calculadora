import os

def calcular_precio_final(precio_original, descuento):
    # R1: Descuento entre 0 y 100 (si no, levantar error)
    if not (0 <= descuento <= 100):
        raise ValueError("El descuento debe estar entre 0 y 100.")
    
    # R2: Precio original debe ser positivo (mayor que 0)
    if precio_original <= 0:
        raise ValueError("El precio original debe ser un valor positivo.")
    
    # R3: Calcular precio final base
    precio_final = precio_original * (1 - descuento / 100)
    
    # R5: Si el descuento es >= 80%, aplicar descuento adicional del 5% sobre lo ya descontado
    if descuento >= 80:
        precio_final = precio_final * (1 - 5 / 100)
        
    # R4: Redondear a 2 decimales
    return round(precio_final, 2)


def registrar_en_auditoria(precio, descuento, resultado_o_error, es_exitoso):
    archivo_auditoria = "auditoria.txt"
    
    # Si el archivo no existe, lo creamos con un encabezado bonito
    if not os.path.exists(archivo_auditoria):
        with open(archivo_auditoria, "w", encoding="utf-8") as archivo:
            archivo.write("=== HISTORIAL DE AUDITORÍA DE LA CALCULADORA ===\n\n")
    
    # Abrimos en modo "a" (append) para añadir líneas al final sin borrar lo anterior
    with open(archivo_auditoria, "a", encoding="utf-8") as archivo:
        if es_exitoso:
            linea = f"ENTRADA -> Precio: {precio}, Descuento: {descuento}% | RESULTADO: ${resultado_o_error}\n"
        else:
            linea = f"ENTRADA -> Precio: {precio}, Descuento: {descuento}% | ERROR: {resultado_o_error}\n"
        archivo.write(linea)


def iniciar_calculadora_interactiva():
    print("=========================================")
    print("  CALCULADORA DE DESCUENTOS INTERACTIVA  ")
    print("=========================================\n")
    
    while True:
        try:
            # Entrada de datos por el usuario
            entrada_precio = input("Ingrese el precio original (o escriba 'salir' para terminar): ")
            if entrada_precio.lower() == 'salir':
                print("\n¡Gracias por usar la calculadora! Programa terminado.")
                break
                
            entrada_descuento = input("Ingrese el porcentaje de descuento (0 a 100): ")
            if entrada_descuento.lower() == 'salir':
                print("\n¡Gracias por usar la calculadora! Programa terminado.")
                break
            
            # Convertimos las entradas a números
            precio = float(entrada_precio)
            descuento = float(entrada_descuento)
            
            # Intentamos calcular el precio final según los requisitos
            resultado = calcular_precio_final(precio, descuento)
            
            # Si todo sale bien, mostramos en pantalla y guardamos en la auditoría
            print(f"-> ¡Éxito! El precio final es: ${resultado}\n")
            registrar_en_auditoria(precio, descuento, resultado, es_exitoso=True)
            
        except ValueError as e:
            # Capturamos errores de validación (R1, R2) o si el usuario no ingresó un número válido
            mensaje_error = str(e)
            
            # Si el error es porque el usuario escribió letras en vez de números
            if "could not convert string to float" in mensaje_error:
                mensaje_error = "Debe ingresar valores numéricos válidos."
            
            print(f"-> Error: {mensaje_error}\n")
            
            # Intentamos registrar el fallo en la auditoría si al menos eran números
            try:
                registrar_en_auditoria(float(entrada_precio), float(entrada_descuento), mensaje_error, es_exitoso=False)
            except:
                # Si ni siquiera eran números, registramos el texto crudo que puso el usuario
                registrar_en_auditoria(entrada_precio, entrada_descuento, mensaje_error, es_exitoso=False)

# Ejecutar la aplicación
if __name__ == "__main__":
    iniciar_calculadora_interactiva()