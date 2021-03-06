from django.contrib.auth.password_validation import password_changed
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import Producto, Marca
from .forms import ProductoForm, CustomUserCreationFrom
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import serializers, viewsets
from .serializers import MarcaSerialize, ProductoSerializer
from django.contrib.auth.models import User
# Create your views here.

def error_facebook(request):
    return render(request, 'registration/error_facebook.html')

class MarcaViewset(viewsets.ModelViewSet):
    queryset= Marca.objects.all()
    serializer_class = MarcaSerialize

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        productos = Producto.objects.all()

        nombre = self.request.GET.get('nombre')
        
        if nombre:
            productos = productos.filter(nombre__contains=nombre)

        return productos

def home(request):
    productos = Producto.objects.all()
    categorias= Marca.objects.all()
    data ={
        'productos': productos,
        'categorias': categorias
    }
    return render(request, 'app/home.html', data)

def terminos(request):

    return render(request, 'app/terminos.html')

def cat(request, id):
    productos = Producto.objects.filter(marca=id)
    categorias= Marca.objects.all()
    data ={
        'productos': productos,
        'categorias': categorias
    }
    return render(request, 'app/cat.html', data)



#permiso para entrar a cualquier pesgtaña
#@login_required

def agregar_producto(request):
    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
            
        else:
            data["form"] = formulario

    return render(request, 'app/producto/agregar.html', data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 10)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity' : productos,
        'paginator': paginator
    }
    return render(request, 'app/producto/listar.html', data)


def modificar_producto(request, id):
    
    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Se modifico correctamente")
            data["mensaje"] = "modificado correctamente"
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'app/producto/modificar.html', data)


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Se elimino corectamente")
    return redirect(to="home")

def registro(request):
    data = {
        'form': CustomUserCreationFrom()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationFrom(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #refirigir al home
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)
 
