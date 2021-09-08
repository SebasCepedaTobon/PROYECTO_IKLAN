from django.contrib.auth.password_validation import password_changed
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import Producto, Marca
from .forms import ContactoForm, ProductoForm, CustomUserCreationFrom
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import serializers, viewsets
from .serializers import MarcaSerialize, ProductoSerializer
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
    data ={
        'productos': productos
    }
    return render(request, 'app/home.html', data)

def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto guardado"
        else:
            data["form"] = formulario
    return render(request, 'app/contacto.html', data)

#permiso para entrar a cualquier pesgtaña
#@login_required
def galeria(request):
    return render(request, 'app/galeria.html')

@permission_required('app.add_producto')
def agregar_producto(request):
    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
            data["mensaje"] = "Se guardo correctamente"
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

@permission_required('app.chage_producto')
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
            return redirect(to="listar_productos")
        data["form"] = formulario
    return render(request, 'app/producto/modificar.html', data)

@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Se elimino corectamente")
    return redirect(to="listar_productos")

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
 
