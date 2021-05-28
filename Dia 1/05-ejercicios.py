class Persona:
    def __init__(self, nombre, fecha_nacimiento, nacionalidad , dni):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad
        self.dni = dni

class Alumno(Persona):
    def __init__(self, nombre, fecha_nacimiento, dni, nacionalidad = "PERUANO"):
        super().__init__(nombre, fecha_nacimiento, nacionalidad, dni)
        self.__cursos_matriculados = cursos_matriculados

    def mostrar_cursos(self):
        print("Los cursos son {}".format(self.cursos_matriculados))    


    def __setCurso(self):
        self.__cursos_matriculados = cursos_matriculados

    def __getCurso(self):
        return self.__cursos_matriculados

    cursos_matriculados = property(__setCurso, __getCurso)    






class Docente(Persona):
    def __init__(self, nombre, fecha_nacimiento, dni, nacionalidad = "PERUANO"):
        super().__init__(nombre, fecha_nacimiento, nacionalidad, dni)
        self.__seguro_social = seguro_social
        self.cts = self.__ingresarcts(cts)

    def __ingresarcts(self, cts):
        return cts + 100    

    def mostrar_cts(self):
        print("Su cta cts es {}".format(self.cts))


objDocente  = Docente("Michael", "1985-05-01", 26565654)
objAlumno = Alumno("Sandra", "1985-04-15", 568431, "COLOMBIANA")