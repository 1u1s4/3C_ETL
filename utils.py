import base64

def guardar_imagen_decodificada(empleado):
    # Datos binarios de la imagen (por ejemplo, recibidos desde una API o leídos de una base de datos)
    binary_data = empleado['image_128']
    # pasar a binario 
    binary_data = base64.b64decode(binary_data)

    # Convertir binario a base64
    base64_string = base64.b64encode(binary_data).decode('utf-8')
    print("Base64:", base64_string)

    # Decodificar base64 a binario y guardar la imagen
    decoded_image_data = base64.b64decode(base64_string)

    # Guardar la imagen en un archivo
    with open('imagen_decodificada.png', 'wb') as image_file:
        image_file.write(decoded_image_data)

    print("Imagen guardada como imagen_decodificada.png")

