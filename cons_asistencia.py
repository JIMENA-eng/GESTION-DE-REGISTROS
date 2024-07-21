class Cons_asistencia:
    def __init__(self, nombres, apellido_paterno, apellido_materno, dni, genero, estado_civil,fecha_hora):
        self.__nombres=nombres
        self.__apellido_paterno=apellido_paterno
        self.__apellido_materno=apellido_materno
        self.__dni=dni
        self.__estado_civil=estado_civil
        self.__genero=genero
        self.__fecha_hora=fecha_hora
    
    def info(self):
        return self.__nombres,self.__apellido_paterno,self.__apellido_materno, self.__dni,self.__genero,self.__estado_civil,self.__fecha_hora
        