# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
import json
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import Category, Product, Order, ComponentOption

# Кастомизация стандартного admin.site
admin.site.site_header = "Админ-панель Tech Shop"
admin.site.site_title = "Tech Shop"
admin.site.index_title = "Управление магазином"

class CustomAdminMixin:
    class Media:
        css = {'all': ('admin/css/output.css',)}
        js = ('admin/js/my_custom_admin.js',)  # Используем my_custom_admin.js, как было ранее

@admin.register(ComponentOption)
class ComponentOptionAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'volume', 'product_count', 'display_type_label')
    list_filter = ('type',)
    search_fields = ('name', 'volume')
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ('type', 'name')
    actions = ['update_price_increase', 'update_price_decrease']

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = "Используется в товарах"

    def display_type_label(self, obj):
        return dict(ComponentOption.COMPONENT_TYPES).get(obj.type, obj.type)
    display_type_label.short_description = "Тип (название)"

    def update_price_increase(self, request, queryset):
        for component in queryset:
            component.price *= 1.05
            component.save()
        self.message_user(request, f"Цены увеличены на 5 процентов для {queryset.count()} комплектующих.")
    update_price_increase.short_description = "Увеличить цену на 5 процентов"

    def update_price_decrease(self, request, queryset):
        for component in queryset:
            component.price *= 0.95
            component.save()
        self.message_user(request, f"Цены уменьшены на 5 процентов для {queryset.count()} комплектующих.")
    update_price_decrease.short_description = "Уменьшить цену на 5 процентов"

    def get_fieldsets(self, request, obj=None):
        return [
            (None, {
                'fields': ('name', 'type', 'price', 'volume')
            }),
        ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].label = "Название"
        form.base_fields['type'].label = "Тип"
        form.base_fields['price'].label = "Цена"
        form.base_fields['volume'].label = "Объём/Размер"
        return form

@admin.register(Category)
class CategoryAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'product_count', 'total_stock', 'total_value', 'category_link')
    search_fields = ('name',)
    actions = ['duplicate_categories', 'merge_categories']
    list_per_page = 20
    ordering = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            product_count=Count('product'),
            total_stock=Sum('product__stock'),
            total_value=Sum('product__base_price')
        )

    def product_count(self, obj):
        return obj.product_count
    product_count.short_description = "Количество товаров"

    def total_stock(self, obj):
        return obj.total_stock or 0
    total_stock.short_description = "Общий запас"

    def total_value(self, obj):
        return f"${obj.total_value or 0:.2f}"
    total_value.short_description = "Общая стоимость"

    def category_link(self, obj):
        url = reverse('admin:shop_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">Посмотреть товары</a>', url)
    category_link.short_description = "Ссылка"

    def duplicate_categories(self, request, queryset):
        for category in queryset:
            category.pk = None
            category.name += " (копия)"
            category.save()
        self.message_user(request, f"Созданы копии для {queryset.count()} категорий.")
    duplicate_categories.short_description = "Дублировать выбранные категории"

    def merge_categories(self, request, queryset):
        if queryset.count() < 2:
            self.message_user(request, "Выберите как минимум 2 категории для объединения.", level=messages.ERROR)
            return
        main_category = queryset.first()
        other_categories = queryset.exclude(id=main_category.id)
        products = Product.objects.filter(category__in=other_categories)
        products.update(category=main_category)
        other_categories.delete()
        self.message_user(request, f"Объединено {other_categories.count()} категорий в '{main_category.name}'.")
    merge_categories.short_description = "Объединить выбранные категории"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].label = "Название"
        return form

class ComponentOptionInline(admin.TabularInline):
    model = Product.components.through
    extra = 2
    verbose_name = "Комплектующее"
    verbose_name_plural = "Комплектующие"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "componentoption":
            if request.resolver_match.kwargs.get('object_id'):
                try:
                    product = Product.objects.get(id=request.resolver_match.kwargs['object_id'])
                    if product.component_type:
                        kwargs["queryset"] = ComponentOption.objects.filter(type=product.component_type)
                    else:
                        kwargs["queryset"] = ComponentOption.objects.all()
                except Product.DoesNotExist:
                    kwargs["queryset"] = ComponentOption.objects.all()
            else:
                kwargs["queryset"] = ComponentOption.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Product)
class ProductAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'category', 'component_type', 'base_price', 'stock', 'display_image', 'is_available', 'discount', 'view_3d_model', 'final_price')
    list_filter = ('category', 'component_type', 'stock', 'discount')
    search_fields = ('name', 'description')
    list_editable = ('base_price', 'stock', 'discount')
    actions = ['set_stock_to_zero', 'increase_price', 'decrease_price', 'apply_discount', 'remove_discount', 'export_to_csv']
    prepopulated_fields = {'description': ('name',)}
    list_per_page = 20
    inlines = [ComponentOptionInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'component_type', 'base_price', 'description', 'image', 'model_3d', 'stock', 'discount')
        }),
        ('Совместимость', {
            'fields': ('compatible_with',),
            'classes': ('collapse',),
        }),
    )
    ordering = ('name',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Нет изображения"
    display_image.short_description = "Изображение"

    def view_3d_model(self, obj):
        if obj.model_3d:
            return format_html('<a href="{}" target="_blank">Просмотреть 3D</a>', obj.model_3d.url)
        return "Нет 3D модели"
    view_3d_model.short_description = "3D модель"

    def is_available(self, obj):
        return obj.stock > 0
    is_available.boolean = True
    is_available.short_description = "В наличии"

    def final_price(self, obj):
        if obj.discount:
            return f"${(obj.base_price * (100 - obj.discount) / 100):.2f}"
        return f"${obj.base_price:.2f}"
    final_price.short_description = "Итоговая цена"

    def set_stock_to_zero(self, request, queryset):
        updated = queryset.update(stock=0)
        self.message_user(request, f"Обновлено {updated} товаров: запас установлен в 0")
    set_stock_to_zero.short_description = "Установить запас в 0"

    def increase_price(self, request, queryset):
        for product in queryset:
            product.base_price *= 1.1
            product.save()
        self.message_user(request, f"Цены увеличены на 10 процентов для {queryset.count()} товаров")
    increase_price.short_description = "Увеличить цену на 10 процентов"

    def decrease_price(self, request, queryset):
        for product in queryset:
            product.base_price *= 0.9
            product.save()
        self.message_user(request, f"Цены уменьшены на 10 процентов для {queryset.count()} товаров")
    decrease_price.short_description = "Уменьшить цену на 10 процентов"

    def apply_discount(self, request, queryset):
        updated = queryset.update(discount=10)
        self.message_user(request, f"Скидка 10 процентов применена к {updated} товарам")
    apply_discount.short_description = "Применить скидку 10 процентов"

    def remove_discount(self, request, queryset):
        updated = queryset.update(discount=0)
        self.message_user(request, f"Скидка снята с {updated} товаров")
    remove_discount.short_description = "Снять скидку"

    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Название', 'Категория', 'Тип', 'Базовая цена', 'Запас', 'Скидка', 'Итоговая цена'])
        for product in queryset:
            final_price = product.base_price * (100 - product.discount) / 100 if product.discount else product.base_price
            writer.writerow([
                product.id,
                product.name,
                product.category.name,
                product.component_type,
                product.base_price,
                product.stock,
                product.discount,
                final_price
            ])
        return response
    export_to_csv.short_description = "Экспортировать в CSV"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].label = "Название"
        form.base_fields['category'].label = "Категория"
        form.base_fields['component_type'].label = "Тип комплектующих"
        form.base_fields['base_price'].label = "Базовая цена"
        form.base_fields['description'].label = "Описание"
        form.base_fields['image'].label = "Изображение"
        form.base_fields['model_3d'].label = "3D-модель"
        form.base_fields['stock'].label = "Запас"
        form.base_fields['discount'].label = "Скидка (проценты)"
        form.base_fields['compatible_with'].label = "Совместимость"
        return form

@admin.register(Order)
class OrderAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total', 'delivery', 'status', 'created_at', 'item_count', 'view_items')
    list_filter = ('delivery', 'status', 'created_at')
    search_fields = ('customer_name', 'address', 'comment')
    readonly_fields = ('created_at',)
    actions = ['mark_as_express', 'mark_as_shipped', 'mark_as_delivered', 'cancel_orders', 'export_to_csv']
    fields = ('customer_name', 'address', 'delivery', 'comment', 'total', 'status', 'created_at', 'items')
    date_hierarchy = 'created_at'
    list_per_page = 20
    ordering = ('-created_at',)

    def item_count(self, obj):
        try:
            items = json.loads(obj.items) if obj.items else []
            return len(items)
        except (json.JSONDecodeError, TypeError):
            return len(obj.items.split(',')) if obj.items and isinstance(obj.items, str) and obj.items.strip() else 0
    item_count.short_description = "Товаров в заказе"

    def view_items(self, obj):
        try:
            items = json.loads(obj.items) if obj.items else []
            if not items:
                return "Нет товаров"
            item_list = "<ul>"
            for item in items:
                if isinstance(item, dict) and 'name' in item:
                    item_list += f"<li>{item['name']} (x{item.get('quantity', 1)})</li>"
                else:
                    item_list += f"<li>{item}</li>"
            item_list += "</ul>"
            return mark_safe(item_list)
        except (json.JSONDecodeError, TypeError):
            return obj.items or "Нет товаров"
    view_items.short_description = "Товары"

    def mark_as_express(self, request, queryset):
        updated = queryset.update(delivery='express')
        self.message_user(request, f"Обновлено {updated} заказов: доставка изменена на Экспресс")
    mark_as_express.short_description = "Пометить как Экспресс"

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='Shipped')
        self.message_user(request, f"Обновлено {updated} заказов: статус изменён на 'Отправлен'")
    mark_as_shipped.short_description = "Пометить как отправленные"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='Delivered')
        self.message_user(request, f"Обновлено {updated} заказов: статус изменён на 'Доставлен'")
    mark_as_delivered.short_description = "Пометить как доставленные"

    def cancel_orders(self, request, queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f"Обновлено {updated} заказов: статус изменён на 'Отменён'")
    cancel_orders.short_description = "Отменить заказы"

    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Клиент', 'Итого', 'Тип доставки', 'Статус', 'Дата создания', 'Товары'])
        for order in queryset:
            writer.writerow([
                order.id,
                order.customer_name,
                order.total,
                order.delivery,
                order.status,
                order.created_at,
                order.items
            ])
        return response
    export_to_csv.short_description = "Экспортировать в CSV"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['items'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 5, 'cols': 50})
        form.base_fields['items'].help_text = "Перечислите товары в формате JSON или через запятую, например: Product1, Product2, Product3"
        form.base_fields['customer_name'].label = "Имя клиента"
        form.base_fields['address'].label = "Адрес"
        form.base_fields['delivery'].label = "Тип доставки"
        form.base_fields['comment'].label = "Комментарий"
        form.base_fields['total'].label = "Итого"
        form.base_fields['status'].label = "Статус"
        form.base_fields['created_at'].label = "Дата создания"
        form.base_fields['items'].label = "Товары"
        return form