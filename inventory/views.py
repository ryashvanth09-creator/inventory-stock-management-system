from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from .models import Product, Category, Supplier, Customer, StockIn, StockOut

# ==========================================
# LOGIN
# ==========================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(request, 'login.html')


# ==========================================
# DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    total_customers = Customer.objects.count()

    total_stock = sum(
        product.quantity
        for product in Product.objects.all()
    )

    low_stock_products = Product.objects.filter(
        quantity__lte=F('reorder_level')
    )

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'total_customers': total_customers,
        'total_stock': total_stock,
        'low_stock_products': low_stock_products,
    }

    return render(
        request,
        'dashboard.html',
        context
    )

# ==========================================
# LOGOUT
# ==========================================

def user_logout(request):

    logout(request)

    return redirect('login')


# ==========================================
# CATEGORY - VIEW ALL
# ==========================================

@login_required
def category_list(request):

    categories = Category.objects.all().order_by('name')

    return render(
        request,
        'category_list.html',
        {
            'categories': categories
        }
    )


# ==========================================
# CATEGORY - ADD
# ==========================================

@login_required
def category_add(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        if not name:

            messages.error(
                request,
                'Category name is required.'
            )

            return render(
                request,
                'category_form.html'
            )

        if Category.objects.filter(
            name__iexact=name
        ).exists():

            messages.error(
                request,
                'This category already exists.'
            )

            return render(
                request,
                'category_form.html'
            )

        Category.objects.create(
            name=name,
            description=description
        )

        messages.success(
            request,
            'Category added successfully.'
        )

        return redirect('category_list')

    return render(
        request,
        'category_form.html'
    )


# ==========================================
# CATEGORY - EDIT
# ==========================================

@login_required
def category_edit(request, id):

    category = get_object_or_404(
        Category,
        id=id
    )

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        if not name:

            messages.error(
                request,
                'Category name is required.'
            )

            return render(
                request,
                'category_form.html',
                {
                    'category': category
                }
            )

        duplicate = Category.objects.filter(
            name__iexact=name
        ).exclude(
            id=category.id
        ).exists()

        if duplicate:

            messages.error(
                request,
                'Another category with this name already exists.'
            )

            return render(
                request,
                'category_form.html',
                {
                    'category': category
                }
            )

        category.name = name
        category.description = description

        category.save()

        messages.success(
            request,
            'Category updated successfully.'
        )

        return redirect('category_list')

    return render(
        request,
        'category_form.html',
        {
            'category': category
        }
    )


# ==========================================
# CATEGORY - DELETE
# ==========================================

@login_required
def category_delete(request, id):

    category = get_object_or_404(
        Category,
        id=id
    )

    if request.method == 'POST':

        category.delete()

        messages.success(
            request,
            'Category deleted successfully.'
        )

        return redirect('category_list')

    return render(
        request,
        'category_delete.html',
        {
            'category': category
        }
    )


# ==========================================
# PRODUCT - VIEW ALL
# ==========================================

@login_required
def product_list(request):

    products = Product.objects.all().order_by('name')

    return render(
        request,
        'product_list.html',
        {
            'products': products
        }
    )


# ==========================================
# PRODUCT - ADD
# ==========================================

@login_required
def product_add(request):

    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        sku = request.POST.get(
            'sku',
            ''
        ).strip()

        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        reorder_level = request.POST.get('reorder_level')

        if not name or not sku or not category_id:

            messages.error(
                request,
                'Please fill all required fields.'
            )

            return render(
                request,
                'product_form.html',
                {
                    'categories': categories
                }
            )

        if Product.objects.filter(
            sku__iexact=sku
        ).exists():

            messages.error(
                request,
                'A product with this SKU already exists.'
            )

            return render(
                request,
                'product_form.html',
                {
                    'categories': categories
                }
            )

        category = get_object_or_404(
            Category,
            id=category_id
        )

        Product.objects.create(
            name=name,
            sku=sku,
            category=category,
            quantity=int(quantity or 0),
            purchase_price=purchase_price or 0,
            selling_price=selling_price or 0,
            reorder_level=int(reorder_level or 5)
        )

        messages.success(
            request,
            'Product added successfully.'
        )

        return redirect('product_list')

    return render(
        request,
        'product_form.html',
        {
            'categories': categories
        }
    )


# ==========================================
# PRODUCT - EDIT
# ==========================================

@login_required
def product_edit(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        sku = request.POST.get(
            'sku',
            ''
        ).strip()

        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        reorder_level = request.POST.get('reorder_level')

        duplicate_sku = Product.objects.filter(
            sku__iexact=sku
        ).exclude(
            id=product.id
        ).exists()

        if duplicate_sku:

            messages.error(
                request,
                'Another product with this SKU already exists.'
            )

            return render(
                request,
                'product_form.html',
                {
                    'product': product,
                    'categories': categories
                }
            )

        category = get_object_or_404(
            Category,
            id=category_id
        )

        product.name = name
        product.sku = sku
        product.category = category
        product.quantity = int(quantity or 0)
        product.purchase_price = purchase_price or 0
        product.selling_price = selling_price or 0
        product.reorder_level = int(reorder_level or 5)

        product.save()

        messages.success(
            request,
            'Product updated successfully.'
        )

        return redirect('product_list')

    return render(
        request,
        'product_form.html',
        {
            'product': product,
            'categories': categories
        }
    )


# ==========================================
# PRODUCT - DELETE
# ==========================================

@login_required
def product_delete(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == 'POST':

        product.delete()

        messages.success(
            request,
            'Product deleted successfully.'
        )

        return redirect('product_list')

    return render(
        request,
        'product_delete.html',
        {
            'product': product
        }
    )
# ==========================================
# SUPPLIER - VIEW ALL
# ==========================================

@login_required
def supplier_list(request):

    suppliers = Supplier.objects.all().order_by('name')

    return render(
        request,
        'supplier_list.html',
        {
            'suppliers': suppliers
        }
    )


# ==========================================
# SUPPLIER - ADD
# ==========================================

@login_required
def supplier_add(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not name or not phone:

            messages.error(
                request,
                'Supplier name and phone number are required.'
            )

            return render(
                request,
                'supplier_form.html'
            )

        Supplier.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )

        messages.success(
            request,
            'Supplier added successfully.'
        )

        return redirect('supplier_list')

    return render(
        request,
        'supplier_form.html'
    )


# ==========================================
# SUPPLIER - EDIT
# ==========================================

@login_required
def supplier_edit(request, id):

    supplier = get_object_or_404(
        Supplier,
        id=id
    )

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not name or not phone:

            messages.error(
                request,
                'Supplier name and phone number are required.'
            )

            return render(
                request,
                'supplier_form.html',
                {
                    'supplier': supplier
                }
            )

        supplier.name = name
        supplier.phone = phone
        supplier.email = email
        supplier.address = address

        supplier.save()

        messages.success(
            request,
            'Supplier updated successfully.'
        )

        return redirect('supplier_list')

    return render(
        request,
        'supplier_form.html',
        {
            'supplier': supplier
        }
    )


# ==========================================
# SUPPLIER - DELETE
# ==========================================

@login_required
def supplier_delete(request, id):

    supplier = get_object_or_404(
        Supplier,
        id=id
    )

    if request.method == 'POST':

        supplier.delete()

        messages.success(
            request,
            'Supplier deleted successfully.'
        )

        return redirect('supplier_list')

    return render(
        request,
        'supplier_delete.html',
        {
            'supplier': supplier
        }
    )
# ==========================================
# CUSTOMER - VIEW ALL
# ==========================================

@login_required
def customer_list(request):

    customers = Customer.objects.all().order_by('name')

    return render(
        request,
        'customer_list.html',
        {
            'customers': customers
        }
    )


# ==========================================
# CUSTOMER - ADD
# ==========================================

@login_required
def customer_add(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not name or not phone:

            messages.error(
                request,
                'Customer name and phone number are required.'
            )

            return render(
                request,
                'customer_form.html'
            )

        Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )

        messages.success(
            request,
            'Customer added successfully.'
        )

        return redirect('customer_list')

    return render(
        request,
        'customer_form.html'
    )


# ==========================================
# CUSTOMER - EDIT
# ==========================================

@login_required
def customer_edit(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not name or not phone:

            messages.error(
                request,
                'Customer name and phone number are required.'
            )

            return render(
                request,
                'customer_form.html',
                {
                    'customer': customer
                }
            )

        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.address = address

        customer.save()

        messages.success(
            request,
            'Customer updated successfully.'
        )

        return redirect('customer_list')

    return render(
        request,
        'customer_form.html',
        {
            'customer': customer
        }
    )


# ==========================================
# CUSTOMER - DELETE
# ==========================================

@login_required
def customer_delete(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if request.method == 'POST':

        customer.delete()

        messages.success(
            request,
            'Customer deleted successfully.'
        )

        return redirect('customer_list')

    return render(
        request,
        'customer_delete.html',
        {
            'customer': customer
        }
    )
# ==========================================
# STOCK IN - HISTORY
# ==========================================

@login_required
def stock_in_list(request):

    stock_records = StockIn.objects.select_related(
        'product',
        'supplier'
    ).order_by('-date')

    return render(
        request,
        'stock_in_list.html',
        {
            'stock_records': stock_records
        }
    )


# ==========================================
# STOCK IN - ADD
# ==========================================

@login_required
def stock_in_add(request):

    products = Product.objects.all().order_by('name')
    suppliers = Supplier.objects.all().order_by('name')

    if request.method == 'POST':

        product_id = request.POST.get('product')
        supplier_id = request.POST.get('supplier')
        quantity = request.POST.get('quantity')

        # Check all fields
        if not product_id or not supplier_id or not quantity:

            messages.error(
                request,
                'Please fill all fields.'
            )

            return render(
                request,
                'stock_in_form.html',
                {
                    'products': products,
                    'suppliers': suppliers
                }
            )

        # Check quantity is a valid number
        try:
            quantity = int(quantity)

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messages.error(
                request,
                'Quantity must be greater than 0.'
            )

            return render(
                request,
                'stock_in_form.html',
                {
                    'products': products,
                    'suppliers': suppliers
                }
            )

        supplier = get_object_or_404(
            Supplier,
            id=supplier_id
        )

        # Update stock safely
        with transaction.atomic():

            product = Product.objects.select_for_update().get(
                id=product_id
            )

            # Increase product quantity
            product.quantity += quantity
            product.save(update_fields=['quantity'])

            # Save Stock In transaction
            StockIn.objects.create(
                product=product,
                supplier=supplier,
                quantity=quantity
            )

        messages.success(
            request,
            f'{quantity} units of {product.name} added successfully.'
        )

        return redirect('stock_in_list')

    return render(
        request,
        'stock_in_form.html',
        {
            'products': products,
            'suppliers': suppliers
        }
    )
# ==========================================
# STOCK OUT - HISTORY
# ==========================================

@login_required
def stock_out_list(request):

    stock_records = StockOut.objects.select_related(
        'product',
        'customer'
    ).order_by('-date')

    return render(
        request,
        'stock_out_list.html',
        {
            'stock_records': stock_records
        }
    )


# ==========================================
# STOCK OUT - ADD
# ==========================================

@login_required
def stock_out_add(request):

    products = Product.objects.all().order_by('name')
    customers = Customer.objects.all().order_by('name')

    if request.method == 'POST':

        product_id = request.POST.get('product')
        customer_id = request.POST.get('customer')
        quantity = request.POST.get('quantity')

        # Check all fields
        if not product_id or not customer_id or not quantity:

            messages.error(
                request,
                'Please fill all fields.'
            )

            return render(
                request,
                'stock_out_form.html',
                {
                    'products': products,
                    'customers': customers
                }
            )

        # Validate quantity
        try:
            quantity = int(quantity)

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messages.error(
                request,
                'Quantity must be greater than 0.'
            )

            return render(
                request,
                'stock_out_form.html',
                {
                    'products': products,
                    'customers': customers
                }
            )

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        # Safely update stock
        with transaction.atomic():

            product = get_object_or_404(
                Product.objects.select_for_update(),
                id=product_id
            )

            # Check available stock
            if quantity > product.quantity:

                messages.error(
                    request,
                    f'Insufficient stock! Only {product.quantity} units of {product.name} are available.'
                )

                return render(
                    request,
                    'stock_out_form.html',
                    {
                        'products': products,
                        'customers': customers
                    }
                )

            # Subtract quantity
            product.quantity -= quantity

            product.save(
                update_fields=['quantity']
            )

            # Save Stock Out transaction
            StockOut.objects.create(
                product=product,
                customer=customer,
                quantity=quantity
            )

        messages.success(
            request,
            f'{quantity} units of {product.name} issued successfully.'
        )

        return redirect('stock_out_list')

    return render(
        request,
        'stock_out_form.html',
        {
            'products': products,
            'customers': customers
        }
    )
# ==========================================
# REPORTS
# ==========================================

@login_required
def reports(request):

    # Total number of products
    total_products = Product.objects.count()

    # Total current stock
    total_stock = Product.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Total quantity received
    total_stock_in = StockIn.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Total quantity issued
    total_stock_out = StockOut.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Low stock products
    low_stock_products = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).order_by('quantity')

    # Calculate inventory value for every product
    value_expression = ExpressionWrapper(
        F('quantity') * F('purchase_price'),
        output_field=DecimalField(
            max_digits=15,
            decimal_places=2
        )
    )

    products = Product.objects.select_related(
        'category'
    ).annotate(
        stock_value=value_expression
    ).order_by('name')

    # Total inventory value
    total_inventory_value = products.aggregate(
        total=Sum('stock_value')
    )['total'] or 0

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'total_stock_in': total_stock_in,
        'total_stock_out': total_stock_out,
        'low_stock_products': low_stock_products,
        'products': products,
        'total_inventory_value': total_inventory_value,
    }

    return render(
        request,
        'reports.html',
        context
    )