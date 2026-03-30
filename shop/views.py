from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Order, OrderItem
from decimal import Decimal
import requests

# ==========================================
# 👇 НАЛАШТУВАННЯ TELEGRAM
# ==========================================
TELEGRAM_BOT_TOKEN = '8466683634:AAF-qAYO-rAKzlfSxBWFHSz5jqum4qjtPqU'
TELEGRAM_CHAT_ID = '1031408038'


def send_telegram_order(order, order_items):
    """Функція для відправки повідомлення в Telegram"""
    try:
        message = f"🔥 <b>НОВЕ ЗАМОВЛЕННЯ #{order.id}</b>\n"
        message += f"➖➖➖➖➖➖➖➖➖➖\n"
        message += f"👤 <b>Клієнт:</b> {order.customer_name}\n"
        message += f"📞 <b>Телефон:</b> {order.customer_phone}\n"
        message += f"🚚 <b>Доставка:</b> {order.get_delivery_method_display()}\n"

        if order.delivery_method == 'nova_poshta':
            message += f"📍 <b>Місто:</b> {order.city}\n"
            message += f"🏠 <b>Відділення:</b> {order.warehouse}\n"
        else:
            message += f"📍 <b>Адреса:</b> {order.delivery_address}\n"

        message += f"💰 <b>Оплата:</b> {order.get_payment_method_display()}\n"

        if order.comment:
            message += f"💬 <b>Коментар:</b> {order.comment}\n"

        message += f"➖➖➖➖➖➖➖➖➖➖\n"
        message += f"🛒 <b>ТОВАРИ:</b>\n"

        for item in order_items:
            item_line = f"▫️ {item.product.name}"
            details = []
            if item.size: details.append(f"Розмір: {item.size}")
            if item.color: details.append(f"Колір: {item.color}")
            if details:
                item_line += f" ({', '.join(details)})"
            item_line += f" — {item.quantity} шт."
            message += f"{item_line}\n"

        message += f"➖➖➖➖➖➖➖➖➖➖\n"
        message += f"💵 <b>СУМА: {order.total_price} грн</b>"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=data)
    except Exception as e:
        print(f"⚠️ Помилка відправки в Telegram: {e}")


def shop_list(request, category_slug=None):
    category_map = {
        't-shirts': 'TSHIRT',
        'hoodies': 'HOODIE',
        'shorts': 'SHORTS',
        'scarfs': 'SCARF',
        'souvenirs': 'SOUVENIR',
        'other': 'OTHER',
    }

    menu_categories = []
    for code, name in Product.CATEGORY_CHOICES:
        slug = next((k for k, v in category_map.items() if v == code), None)
        if slug:
            menu_categories.append({'name': name, 'slug': slug, 'code': code})

    products = Product.objects.filter(is_available=True).order_by('-created_at')

    active_category_code = None
    active_category_name = "Всі новинки"

    if category_slug:
        db_category = category_map.get(category_slug)
        if db_category:
            products = products.filter(category=db_category)
            active_category_code = db_category
            for code, name in Product.CATEGORY_CHOICES:
                if code == db_category:
                    active_category_name = name
                    break

    cart = request.session.get('cart', {})
    mini_cart_items = []
    mini_cart_total = 0

    for key, item_data in cart.items():
        try:
            product = Product.objects.get(id=item_data['product_id'])
            total_item_price = product.price * item_data['quantity']
            mini_cart_total += total_item_price
            mini_cart_items.append({
                'key': key,
                'product': product,
                'quantity': item_data['quantity'],
                'size': item_data['size'],
                'color': item_data['color'],
                'total_price': total_item_price
            })
        except Product.DoesNotExist:
            continue

    context = {
        'products': products,
        'menu_categories': menu_categories,
        'active_category_code': active_category_code,
        'active_category_name': active_category_name,
        'mini_cart_items': mini_cart_items,
        'mini_cart_total': mini_cart_total,
    }
    return render(request, 'shop.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    mini_cart_items = []
    mini_cart_total = 0
    for key, item_data in cart.items():
        try:
            p = Product.objects.get(id=item_data['product_id'])
            total = p.price * item_data['quantity']
            mini_cart_total += total
            mini_cart_items.append({'product': p, 'quantity': item_data['quantity'], 'key': key, 'total_price': total})
        except Product.DoesNotExist:
            continue

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'mini_cart_items': mini_cart_items,
        'mini_cart_total': mini_cart_total
    })


def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', '')
    color = request.POST.get('color', '')
    cart_key = f"{product_id}_{size}_{color}"

    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {'product_id': product_id, 'quantity': quantity, 'size': size, 'color': color}

    request.session['cart'] = cart
    messages.success(request, f"Додано: {product.name}")
    return redirect(request.META.get('HTTP_REFERER', 'shop_list'))


def cart_remove(request, cart_key):
    cart = request.session.get('cart', {})
    if cart_key in cart:
        del cart[cart_key]
        request.session['cart'] = cart
        messages.warning(request, "Товар видалено")
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal(0)

    for key, item_data in cart.items():
        try:
            product = Product.objects.get(id=item_data['product_id'])
            total_item_price = product.price * item_data['quantity']
            subtotal += total_item_price
            cart_items.append({
                'key': key,
                'product': product,
                'quantity': item_data['quantity'],
                'size': item_data['size'],
                'color': item_data['color'],
                'total_price': total_item_price
            })
        except Product.DoesNotExist:
            continue

    discount = Decimal(0)
    if request.user.is_authenticated:
        discount = subtotal * Decimal('0.05')

    total_price = subtotal - discount

    if request.method == 'POST' and 'checkout' in request.POST:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        delivery = request.POST.get('delivery')
        comment = request.POST.get('comment')
        payment_method = request.POST.get('payment_method', 'cod')

        # Отримуємо дані Нової пошти або звичайну адресу
        city = request.POST.get('city_name')
        warehouse = request.POST.get('warehouse_name')
        address = request.POST.get('address')  # Для укрпошти

        if name and phone and cart_items:
            current_user = request.user if request.user.is_authenticated else None

            order = Order.objects.create(
                user=current_user,
                customer_name=name,
                customer_phone=phone,
                delivery_method=delivery,
                city=city if delivery == 'nova_poshta' else None,
                warehouse=warehouse if delivery == 'nova_poshta' else None,
                delivery_address=address if delivery != 'nova_poshta' else None,
                payment_method=payment_method,
                comment=comment,
                total_price=total_price,
                discount_amount=discount
            )

            saved_items = []
            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity'],
                    size=item['size'],
                    color=item['color']
                )
                saved_items.append(order_item)

            send_telegram_order(order, saved_items)
            request.session['cart'] = {}
            messages.success(request, "Замовлення прийнято! Дякуємо.")
            return redirect('shop_list')
        else:
            messages.error(request, "Заповніть обов'язкові поля")

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)