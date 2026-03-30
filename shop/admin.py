from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem


# --- ВНУТРІШНЯ ТАБЛИЦЯ ТОВАРІВ (INLINE) ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']  # Дозволяє шукати товар через лупу (зручно, якщо їх 1000+)
    extra = 0  # Не показувати пусті рядки для нових товарів

    # Поля, які ми хочемо бачити в рядку
    fields = ['product_image', 'product', 'size', 'color', 'quantity', 'price', 'get_row_total']
    readonly_fields = ['product_image', 'get_row_total']  # Ці поля тільки для читання

    # Відображення міні-фото товару прямо в замовленні
    def product_image(self, obj):
        if obj.product.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain;" />',
                               obj.product.image.url)
        return "-"

    product_image.short_description = "Фото"

    # Безпечний підрахунок суми рядка (щоб адмінка не падала)
    def get_row_total(self, obj):
        # Якщо ціни немає або кількості немає — повертаємо 0
        if not obj.price or not obj.quantity:
            return "0.00 грн"
        return f"{obj.price * obj.quantity} грн"

    get_row_total.short_description = 'Сума'


# --- ОСНОВНА АДМІНКА ЗАМОВЛЕНЬ ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Головний список замовлень
    list_display = [
        'id',
        'customer_name',
        'customer_phone',
        'display_total',  # Гарне відображення ціни
        'display_discount',  # Гарне відображення знижки
        'status_colored',  # Статус з кольором
        'created_at',
        'delivery_method'
    ]

    # Фільтри справа
    list_filter = ['status', 'created_at', 'delivery_method']

    # Пошук (можна шукати по ID, імені, телефону)
    search_fields = ['id', 'customer_name', 'customer_phone', 'delivery_address']

    # Підключаємо товари всередину замовлення
    inlines = [OrderItemInline]

    # Групуємо поля для зручності (коли відкриваєш замовлення)
    fieldsets = [
        ('Клієнт', {
            'fields': ['user', 'customer_name', 'customer_phone']
        }),
        ('Доставка', {
            'fields': ['delivery_method', 'delivery_address', 'comment']
        }),
        ('Фінанси', {
            'fields': ['total_price', 'discount_amount', 'status', 'created_at']
        }),
    ]

    readonly_fields = ['created_at']  # Дату створення не можна міняти

    # --- Гарні методи для відображення --- #

    def display_total(self, obj):
        return f"{obj.total_price} грн"

    display_total.short_description = "До сплати"
    display_total.admin_order_field = 'total_price'

    def display_discount(self, obj):
        if obj.discount_amount > 0:
            return format_html('<span style="color: green; font-weight: bold;">-{} грн</span>', obj.discount_amount)
        return "-"

    display_discount.short_description = "Знижка"

    def status_colored(self, obj):
        # Розфарбовуємо статуси
        colors = {
            'new': 'blue',
            'processing': 'orange',
            'shipped': 'purple',
            'completed': 'green',
            'canceled': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )

    status_colored.short_description = "Статус"


# --- АДМІНКА ТОВАРІВ ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'price', 'old_price', 'has_sizes', 'has_colors',
                    'is_available']

    # Що можна редагувати прямо зі списку (дуже зручно!)
    list_editable = ['price', 'old_price', 'is_available', 'has_sizes', 'has_colors']

    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url)
        return "Без фото"

    image_preview.short_description = "Фото"