
# Funcion para personalizar el mensaje de error de mi libreria de JWT
def manejo_error_JWT(error):
    print(error)
    print(error.status_code) # Devolverá el codigo de estado del error
    print(error.description) # Mensaje del error
    print(error.headers) # La cabecera del error (Solo aparece cuando no hay token)
    respuesta = {
        "success" : False,
        "content" : None,
        "message" : None
    }

    if error.error == 'Authorization Required':
        respuesta["message"] = "Se necesita una token para esta peticion"
    elif error.error == 'Bad Request':
        respuesta["message"] = "Credenciales invalidas"

    return respuesta, error.status_code   