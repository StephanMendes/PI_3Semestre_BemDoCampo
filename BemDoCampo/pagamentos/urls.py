from django.urls import path
from . import views

urlpatterns = [
    path('carrinho/', views.CarrinhoView.as_view(), name='carrinho'),
    path('finalizar-compra/', views.FinalizarCompraView.as_view(), name='finalizar_compra')
]
