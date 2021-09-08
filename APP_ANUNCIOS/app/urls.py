from django.db import router
from django.urls import include, path
from .views import agregar_producto, galeria, home, listar_productos,\
     modificar_producto, eliminar_producto, registro, ProductoViewset, MarcaViewset, error_facebook
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewset)
router.register('marca', MarcaViewset)

urlpatterns = [
    path('', home, name='home'),
    path('galeria/', galeria, name='galeria'),
    path('agregar-producto/', agregar_producto, name='agregar_producto'),
    path('listar-producto/', listar_productos, name='listar_productos'),
    path('modificar-producto/<id>/', modificar_producto, name='modificar_producto'),
    path('eliminar-producto/<id>/', eliminar_producto, name='eliminar_producto'),
    path('registro/', registro, name='registro'),
    path('api/', include(router.urls)),
    path('error-facebook/', error_facebook, name="error_facebook"),
]

