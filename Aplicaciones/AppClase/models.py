from django.db import models

# Create your models here.
# Modelo de Clase
class Clase(models.Model):
    id_clase=models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    video_url = models.URLField()
    fecha_publicacion = models.DateField(auto_now_add=True)
   
# Modelo de Material
class Material(models.Model):
    id_material=models.AutoField(primary_key=True)
    clase_material = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='materiales')
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='materiales/')
    
# Modelo de Tarea
class Tarea(models.Model):
    id_tarea=models.AutoField(primary_key=True)
    clase_tarea= models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.TextField()
    fecha_entrega = models.DateField()

class EntregaTarea(models.Model):
    id_entrega=models.AutoField(primary_key=True)
    tarea_en = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="entregas")
    archivo_entrega = models.FileField(upload_to="entregas/")
    comentario_estud = models.TextField(blank=True, null=True)
    fecha_entregaT = models.DateTimeField(auto_now_add=True)

    

# Modelo de Retroalimentación
class Retroalimentacion(models.Model):
    id_retro=models.AutoField(primary_key=True)
    entrega_tarea_r = models.ForeignKey(EntregaTarea, on_delete=models.CASCADE, related_name='retroalimentaciones')
    comentario = models.TextField()
    fecha = models.DateField(auto_now_add=True)

