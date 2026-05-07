from django.shortcuts import render, redirect
from urllib.parse import quote
import json

from products.models import Product
from orders.models import Order, OrderItem


def pedido(request):
    products = Product.objects.filter(active=True)

    if request.method == 'POST':

        cart = json.loads(request.POST.get('cart_data', '[]'))

        if not cart:
            return redirect('/pedido/')

        order = Order.objects.create(
            customer_name=request.POST.get('customer_name', ''),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
        )

        subtotal = 0
        message_items = ""

        for item in cart:
            product = Product.objects.get(id=item['id'])
            quantity = float(item['quantity'])

            unit_price = float(product.price)
            line_total = unit_price * quantity

            subtotal += line_total

            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )

            message_items += f"""
- {product.name}
  Cantidad: {quantity}
  Total: ${round(line_total)}
"""

        iva = subtotal * 0.19
        total = subtotal + iva

        order.subtotal = subtotal
        order.iva = iva
        order.total = total
        order.save()

        message = f"""
🧾 Pedido #{order.id}

👤 Cliente: {order.customer_name}
📍 Dirección: {order.address}

📦 Productos:
{message_items}

💰 Subtotal: ${round(subtotal)}
🧾 IVA: ${round(iva)}
💵 Total: ${round(total)}
"""

        url = f"https://wa.me/56937589348?text={quote(message)}"

        return redirect(url)

    return render(request, 'pedido.html', {
        'products': products
    })

def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'dashboard.html', {
        'orders': orders
    })  