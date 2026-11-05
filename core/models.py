from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre


class LugarPatrimonial(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=160)
    anio_construccion = models.PositiveIntegerField('año de construcción', null=True, blank=True)
    imagen = models.URLField('URL de imagen', max_length=500, blank=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='lugares'
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'lugar patrimonial'
        verbose_name_plural = 'lugares patrimoniales'

    def __str__(self):
        return self.nombre
