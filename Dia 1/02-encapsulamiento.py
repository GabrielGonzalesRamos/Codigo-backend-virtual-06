class Vehiculo:
    def __init__(self, largo, ancho, motor, enMarcha = False):
        self.largo = largo
        self.ancho = ancho
        self.motor = motor
        self.enMarcha = enMarcha
        # Si deseamos que el atributo sea privado( solamente pueda ser accedido dentro de la propia
        # clase tendremos que colocar doble sub guion antes de definir su nombre, y si por el contrario
        # queremos que sea publico, no se colocará el doble sub guion)
        self.__ruedas = 4
    def encender(self, estado=True):
        self.enMarcha = estado
        if(self.enMarcha):
            chequeo = self.__chequeo_interno()
            if chequeo == True:
                return "El coche esta listo"
            else:
                return "El coche tiene problemas"
        else:
            return "El coche esta parado"        

            

    def __chequeo_interno(self):
        self.gasolina= 10
        self.aceite = "OK"
        self.temperatura = 20
        self.kilometraje = 192956
        if(self.gasolina > 20 and self.aceite == "OK" and self.temperatura < 80 and self.kilometraje < 1000000):
            return True
        else:
            return False


    def __str__(self):
        return "El largo es: {} y su ancho es: {}" .format(self.largo, self.ancho)

objVehiculo = Vehiculo(4.50, 1.80, 3000)
print(objVehiculo.largo)
print(objVehiculo.encender())
print(objVehiculo.enMarcha)

print(objVehiculo)


        
        
        
            