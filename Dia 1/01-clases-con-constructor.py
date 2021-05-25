class Persona:
    # Crear una instancia para los atributos que necesitemos
    def __init__(self, nombre, fecha_nacimiento):
        # Hacer referencia a la propia posicion de memoria de la clase
        self.nombre = nombre
        self.fecha_nac = fecha_nacimiento

    def saludar(self):
        print("hola {}".format(self.nombre))

    def __str__(self):
        """ Metodo que sirve para que cuando vayamos a imprimir el valor de la instancia se modifique a lo que
        el desarrollador necesite """
        return self.nombre

objPersona = Persona("Eduardo", "1991-04-22")
objPersona2 = Persona("Daniel", "1997-09-16")
print(objPersona.nombre)
print(objPersona2.nombre)
objPersona.saludar()
