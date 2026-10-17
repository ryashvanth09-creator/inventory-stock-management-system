from django.urls import path
from . import views


urlpatterns = [

    # ==========================================
    # LOGIN / DASHBOARD
    # ==========================================

    path('', views.user_login, name='login'),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),


    # ==========================================
    # CATEGORIES
    # ==========================================

    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),

    path(
        'categories/add/',
        views.category_add,
        name='category_add'
    ),

    path(
        'categories/edit/<int:id>/',
        views.category_edit,
        name='category_edit'
    ),

    path(
        'categories/delete/<int:id>/',
        views.category_delete,
        name='category_delete'
    ),


    # ==========================================
    # PRODUCTS
    # ==========================================

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),

    path(
        'products/add/',
        views.product_add,
        name='product_add'
    ),

    path(
        'products/edit/<int:id>/',
        views.product_edit,
        name='product_edit'
    ),

    path(
        'products/delete/<int:id>/',
        views.product_delete,
        name='product_delete'
    ),


    # ==========================================
    # SUPPLIERS
    # ==========================================

    path(
        'suppliers/',
        views.supplier_list,
        name='supplier_list'
    ),

    path(
        'suppliers/add/',
        views.supplier_add,
        name='supplier_add'
    ),

    path(
        'suppliers/edit/<int:id>/',
        views.supplier_edit,
        name='supplier_edit'
    ),

    path(
        'suppliers/delete/<int:id>/',
        views.supplier_delete,
        name='supplier_delete'
    ),
# ==========================================
# CUSTOMERS
# ==========================================

path(
    'customers/',
    views.customer_list,
    name='customer_list'
),

path(
    'customers/add/',
    views.customer_add,
    name='customer_add'
),

path(
    'customers/edit/<int:id>/',
    views.customer_edit,
    name='customer_edit'
),

path(
    'customers/delete/<int:id>/',
    views.customer_delete,
    name='customer_delete'
),
# ==========================================
# STOCK IN
# ==========================================

path(
    'stock-in/',
    views.stock_in_list,
    name='stock_in_list'
),

path(
    'stock-in/add/',
    views.stock_in_add,
    name='stock_in_add'
),
# ==========================================
# STOCK OUT
# ==========================================

path(
    'stock-out/',
    views.stock_out_list,
    name='stock_out_list'
),

path(
    'stock-out/add/',
    views.stock_out_add,
    name='stock_out_add'
),
# ==========================================
# REPORTS
# ==========================================

path(
    'reports/',
    views.reports,
    name='reports'
),

]