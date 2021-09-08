from django.db import router
from django.urls import include, path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewset)
router.register('marca', MarcaViewset)

urlpatterns = [
    path('', home, name='home'),
    path('cat/<id>/', cat, name='cat'),
    path('agregar-producto/', agregar_producto, name='agregar_producto'),
    path('listar-producto/', listar_productos, name='listar_productos'),
    path('modificar-producto/<id>/', modificar_producto, name='modificar_producto'),
    path('eliminar-producto/<id>/', eliminar_producto, name='eliminar_producto'),
    path('registro/', registro, name='registro'),
    path('api/', include(router.urls)),
    path('error-facebook/', error_facebook, name="error_facebook"),
]

