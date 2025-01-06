from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Clase, Material, Tarea, EntregaTarea, Retroalimentacion

# Create your views here.
def crear_administrador(request):
    username = "admin"
    email = "admin@gmail.com"
    password = "admin"
    
    if not User.objects.filter(email=email).exists():
        try:
            # Crear el superusuario (administrador)
            User.objects.create_superuser(username=username, email=email, password=password)
            return HttpResponse("Administrador creado exitosamente.")
        except Exception as e:
            return HttpResponse(f"Error al crear el administrador: {e}")
    else:
        return HttpResponse("El administrador ya existe.")

# Vista para inicio de sesión
def login_views(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Buscar al usuario por correo electrónico
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado. Intenta nuevamente.")
            return redirect('login_views')

        # Autenticar al usuario
        if user.check_password(password):
            login(request, user)

            # Verificar si el usuario es un superusuario (administrador)
            if user.is_superuser:
                messages.success(request, "Bienvenido, Administrador.")
                return redirect('inicio_admin')  # Redirige a la interfaz del administrador
            else:
                messages.success(request, "Bienvenido.")
                return redirect('inicio_usuario')  # Redirige a la interfaz del usuario regular
        else:
            messages.error(request, "Contraseña incorrecta. Intenta nuevamente.")
            return redirect('login_views')

    return render(request, 'login.html')  # Renderiza el formulario de inicio de sesión

# Vista para la página de inicio
def inicio(request):
    return render(request, 'inicio.html')

# Vista para la interfaz de administrador
@login_required
def inicio_admin(request):
    return render(request, 'inicioAdmin.html')

# Vista para la interfaz de usuario regular
@login_required 
def inicio_usuario(request):
    return render(request, 'inicioUser.html')

#CLASES

def nuevaClase(request):
    return render(request,'nuevaClase.html')

def listadoClase(request):
    clasesBdd=Clase.objects.all()
    return render(request,'listadoClase.html',{'clases':clasesBdd})

def guardarClase(request):
    titulo = request.POST['txt_titulo']
    descripcion = request.POST['txt_descripcion']
    video_url = request.POST['txt_url']
    fecha_publicacion = request.POST['fecha_publicacion']
    nuevaClase = Clase.objects.create(titulo=titulo, descripcion=descripcion, video_url=video_url,
                                      fecha_publicacion=fecha_publicacion)
    messages.success(request,"Registro Completado")
    return redirect('/listadoClase')

def eliminarClase(request,id_clase):
    claseEliminar=Clase.objects.get(id_clase=id_clase)
    claseEliminar.delete()
    messages.success(request,"Clase Eliminad")
    return redirect('/listadoClase')

def editarClase(request,id_clase):
    claseEditar=Clase.objects.get(id_clase=id_clase)
    return render(request,'editarClase.html',
                  {'clase':claseEditar})

def procesarEdicionClase(request):
    clase=Clase.objects.get(id_clase=request.POST['id_clase'])
    clase.titulo = request.POST['txt_titulo']
    clase.descripcion = request.POST['txt_descripcion']
    clase.video_url = request.POST['txt_url']
    clase.fecha_publicacion = request.POST['fecha_publicacion']
    clase.save()
    messages.success(request, "Clase actualizada con éxito")
    return redirect('/listadoClase')

#MATERIAL
def nuevoMaterial(request):
    clases = Clase.objects.all()
    return render(request, 'nuevoMaterial.html', {'clases': clases})

def listadoMaterial(request):
    materialBdd=Material.objects.all()
    return render(request,'listadoMaterial.html',{'materiales':materialBdd})

def guardarMaterial(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.POST['txt_titulo']
        archivo = request.FILES['txt_archivo']
        clase_id= request.POST['id_clase']
        
        # Obtener la clase asociada
        clase = get_object_or_404(Clase, id_clase=clase_id)

        # Crear el material con la relación de clave foránea
        nuevoMaterial = Material.objects.create(
            titulo=titulo,
            archivo=archivo,
            clase_material=clase  # Relación de clave foránea con la clase
        )

        messages.success(request, "Material registrado con éxito")
        return redirect('/listadoMaterial')
    else:
        messages.error(request, "Error al insertar el material")
        return redirect('/nuevoMaterial')



def eliminarMaterial(request, id_material):
    materEliminar=Material.objects.get(id_material=id_material)
    materEliminar.delete()
    messages.success(request, "Material Eliminado")
    return redirect('/listadoMaterial')

def editarMaterial(request,id_material):
    materEditar= get_object_or_404(Material, id_material=id_material)
    clase = Clase.objects.all()
    return render(request,'editarMaterial.html',
                  {'material':materEditar,  
                    'clase': clase})


def procesarEdicionMaterial(request):
    if request.method == 'POST':
        material = Material.objects.get(id_material=request.POST['id_material']) 
        material.titulo = request.POST['txt_titulo']
        material.archivo = request.FILES.get('txt_archivo') 
        
        # Verifica que el campo 'txt_clase' esté presente en el formulario
        id_clase = request.POST.get('txt_clase')  # Usando .get() es más seguro
        if id_clase:
            clase_material = get_object_or_404(Clase, id_clase=id_clase)
            material.clase_material = clase_material

        material.save()
        messages.success(request, "Material actualizado con éxito")
        return redirect('/listadoMaterial')
    else:
        messages.error(request, "Error al procesar la actualización del material")
        return redirect('/listadoMaterial')

#TAREA
def nuevaTarea(request):
    clases = Clase.objects.all()
    return render(request, 'nuevaTarea.html', {'clases': clases})

def listadoTarea(request):
    tareaBdd=Tarea.objects.all()
    return render(request,'listadoTarea.html',{'tareas':tareaBdd})


def guardarTarea(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        descripcion = request.POST['descripcion']
        fecha_entrega = request.POST['fecha_entrega']
        clase_id= request.POST['clase_tarea']
        
        # Obtener la clase asociada
        clase = get_object_or_404(Clase, id_clase=clase_id)

        # Crear el material con la relación de clave foránea
        nuevaTarea = Tarea.objects.create(
           descripcion=descripcion,
           fecha_entrega=fecha_entrega,
           clase_tarea=clase  # Relación de clave foránea con la clase
        )

        messages.success(request, "Tarea registrado con éxito")
        return redirect('/listadoTarea')
    else:
        messages.error(request, "Error al insertar la tarea")
        return redirect('/nuevaTarea')

def eliminarTarea(request, id_tarea):
    tareaEliminar=Tarea.objects.get(id_tarea=id_tarea)
    tareaEliminar.delete()
    messages.success(request, "Tarea Eliminado")
    return redirect('/listadoTarea')

def editarTarea(request,id_tarea):
    tareaEditar= get_object_or_404(Tarea, id_tarea=id_tarea)
    clase = Clase.objects.all()
    return render(request,'editarTarea.html',
                  {'tarea':tareaEditar,  
                    'clase': clase})


def procesarEdicionTarea(request):
    # Obtener la mascota por su ID
    tarea = Tarea.objects.get(id_tarea=request.POST['id_tarea'])
    tarea.descripcion= request.POST['descripcion']
    tarea.fecha_entrega = request.POST['fecha_entrega']
    
    id_clase=request.POST['clase']
    clase_tarea = get_object_or_404(Clase,id_clase=id_clase)
    tarea.clase_tarea=clase_tarea

    tarea.save()
    messages.success(request,"Tarea actualizada con exito")
    return redirect('/listadoTarea')


#subirtarea
def subirTarea(request):
    tareas= Tarea.objects.all()
    return render(request, 'subirTarea.html', {'tareas': tareas})



def listadoSubida(request):
    subidaBdd=EntregaTarea.objects.all()
    return render(request,'listadoSubida.html',{'subidas':subidaBdd})


def guardarEntrega(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        archivo_entrega = request.FILES.get('archivo_entrega')
        comentario_estud = request.POST.get('comentario_estud')
        tarea_en= request.POST['id_tarea']
        
        # Obtener la clase asociada
        tarea = Tarea.objects.get(id_tarea=tarea_en)

        # Crear el material con la relación de clave foránea
        nuevoEntrega = EntregaTarea.objects.create(
            archivo_entrega=archivo_entrega,
            comentario_estud=comentario_estud,
            tarea_en=tarea  # Relación de clave foránea con la clase
        )

        messages.success(request, "Tarea subida  con éxito")
        return redirect('/listadoSubida')

#RETROALIMENTACION
def nuevoComentario(request):
    entregas = EntregaTarea.objects.all()
    for entrega in entregas:
        print(entrega.archivo_entrega.url)  # Verifica la URL del archivo
    return render(request, 'nuevoComentario.html', {'entregas': entregas})



def listadoComentario(request):
    comentarioBdd=Retroalimentacion.objects.all()
    return render(request,'listadoComentario.html',{'comentarios':comentarioBdd})


def guardarComentario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        comentario = request.POST.get('comentario')
        entrega_tarea_r = request.POST['txt_entrega']
        
        # Obtener la clase asociada
        entrega = EntregaTarea.objects.get(id_entrega=entrega_tarea_r)

        # Si se está subiendo un archivo de nuevo (si es necesario en este caso)
        if request.FILES.get('archivo_entrega'):
            archivo = request.FILES['archivo_entrega']
            # Puedes usar el archivo en el modelo si es necesario
            entrega.archivo_entrega = archivo
            entrega.save()

        # Crear el comentario con la relación de clave foránea
        nuevoComentario = Retroalimentacion.objects.create(
            comentario=comentario,
            entrega_tarea_r=entrega  # Relación de clave foránea con la clase
        )

        messages.success(request, "Comentario subido con éxito")
        return redirect('/listadoComentario')

def eliminarComentario(request, id_retro):
    coEliminar=Retroalimentacion.objects.get(id_retro=id_retro)
    coEliminar.delete()
    messages.success(request, "Comentario Eliminado")
    return redirect('/listadoComentario')       
        
def editarComentario(request,id_retro):
    retroEditar= get_object_or_404(Retroalimentacion, id_retro=id_retro)
    entrega = EntregaTarea.objects.all()
    return render(request,'editarComentario.html',
                  {'retro':retroEditar,  
                    'entrega': entrega})
def procesarEdicionComentario(request):
    # Obtener la mascota por su ID
    retro = Retroalimentacion.objects.get(id_retro=request.POST['id_retro'])
    retro.comentario= request.POST['descripcion']
    retro.fecha = request.POST['fecha']
    
    id_entrega=request.POST['archivo']
    entrega_tarea_r  = get_object_or_404(EntregaTarea,id_entrega=id_entrega)
    retro.entrega_tarea_r=entrega_tarea_r

    retro.save()
    messages.success(request,"Comentario actualizado con exito")
    return redirect('/listadoComentario')

