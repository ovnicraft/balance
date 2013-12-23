from django.db import models

# Create your models here.

class Perspectiva(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion= models.CharField(max_length=200)
    color= models.CharField(max_length=20)
    icono=models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def getNombre(self):
        return self.nombre

    def getDescripcion(self):
        return self.descripcion

    def getColor(self):
        return self.color    

    def getIcono(self):
        return self.icono

    def setNombre(self, aux):
        self.nombre=aux

    def setDescripcion(self,aux):
        self.descripcion=aux

    def setColor(self,aux):
        self.color=aux    

    def getIcono(self,aux):
        self.icono=aux

class  Mision(models.Model):
    empresa=models.CharField(max_length=50)
    descripcion= models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.descripcion

    def __str__(self):
        return self.descripcion

    def getEmpresa(self):
        return self.empresa

    def getDescripcion(self):
        return self.descripcion

class CategoriaIndicador(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=200)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50)
    abreviatura=models.CharField(max_length=10)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre
        
class Indicador(models.Model):
    nombre=models.CharField(max_length=50)
    numerador=models.CharField(max_length=50)
    denominador=models.CharField(max_length=50)
    unidad=models.ForeignKey(UnidadMedida)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class Estrategia(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=200)
    perspectivas=models.ForeignKey(Perspectiva)
    indicadores=models.ForeignKey(Indicador)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class CategoriaXIndicador(models.Model):
    categoria=models.ForeignKey(CategoriaIndicador)
    indicador=models.ForeignKey(Indicador)

    class Meta:
        unique_together = ("categoria", "indicador")