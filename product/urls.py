from django.urls import path
from . import views

urlpatterns = [
    path('best_product/',views.ProductBestList.as_view(),name='best_product'),
    path('search/', views.product_search, name='product_search'),
    path('<int:product_id>/like/', views.like_product, name='like_product'),
    path('update_product/<int:pk>',views.ProductUpdate.as_view(), name='product_update'),
    path('create_product/',views.ProductCreate.as_view(),name = "product-create"),
    path('delete_product/<int:product_id>/',views.product_delete,name='product_delete'),
    path('<int:pk>/',views.ProductDetail.as_view(), name='product_detail'),
    path('category/<str:slug>/',views.categories_page),
    path('',views.ProductList.as_view()),
]
