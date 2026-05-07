from django.shortcuts import render, redirect
from urllib.parse import quote
import json  # ✅ IMPORTANTE

from products.models import Product
from orders.models import Order, OrderItem


def home(request):
    products = Product.objects.filter(active=True)

    return render(request, 'home.html', {
        'products': products
    })


def pedido(request):
    products = Product.objects.filter(active=True)

    if request.method == 'POST':

        # 🟢 1. Obtener carrito desde frontend
        cart = json.loads(request.POST.get('cart_data', '[]'))

        if not cart:
            return redirect('/pedido/')  # protección básica

        # 🟢 2. Crear orden
        order = Order.objects.create(
            customer_name=request.POST.get('customer_name', ''),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
        )

        subtotal = 0
        message_items = ""

        # 🟢 3. Recorrer carrito
        for item in cart:

            product = Product.objects.get(id=item['id'])
            quantity = float(item['quantity'])
            unit_price = float(product.price)

            line_total = quantity * unit_price
            subtotal += line_total

            # 🟢 guardar item
            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )

            # 🟢 mensaje WhatsApp
            message_items += f"""
- {product.name}
  Cantidad: {quantity}
  Total: ${round(line_total)}
"""

        iva = subtotal * 0.19
        total = subtotal + iva

        # 🟢 4. Guardar totales
        order.subtotal = subtotal
        order.iva = iva
        order.total = total
        order.save()

        # 🟢 5. Mensaje final
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