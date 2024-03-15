from django.urls import path,include
from.views import *

app_name = 'shop'
urlpatterns = [
    path('',index,name='index'),
    path('product/<int:id>',detail,name='detail'),
    path('wishlist/',wishlist,name='wishlist'),
    path('login/wishlist/',wishlist_login,name='wishlist_login'),
    path('login/wishlist/<int:id>', remove_wishlist, name='remove_wishlist'),
    path('cart/', cart, name='cart'),
    path('cart/remove/<int:id>',remove_cart, name='remove_cart'),
    path('add-product/<int:id>',add_product_cart, name='add_product_cart'),
    path('remove-product/<int:id>',remove_product_cart, name='remove_product_cart'),
    path('checkout/',checkout,name='checkout'),
    path('address/',user_address,name='user_address'),
    path('add/product/',add_product,name='add_product'),
    path('view/product/',view_product,name='view_product'),
    path('update/product/<int:id>',update_product,name='update_product'),
    path('delete/product/<int:id>',delete_product,name='delete_product'),
    

]