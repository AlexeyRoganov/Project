from django.views.generic import ListView,DetailView, UpdateView, CreateView, DeleteView
from .models import Product, Category
from datetime import datetime
from django.shortcuts import render
from .filters import ProductFilter
from .forms import ProductForm
from django.core.paginator import Paginator


class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
    paginate_by = 1


    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = 'Скоро распродажа'
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        # context['categories'] = Category.objects.all()
        # context['form'] = ProductForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     # берём значения для нового товара из POST-запроса, отправленного на сервер
    #     form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
    #
    #     if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
    #         form.save()
    #     return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.

# class ProductDetail(DetailView):
#     # Модель всё та же, но мы хотим получать информацию по отдельному товару
#     model = Product
#     # Используем другой шаблон — product.html
#     template_name = 'product.html'
#     # Название объекта, в котором будет выбранный пользователем продукт
#     context_object_name = 'product'

class ProductDetailView(DetailView):
    template_name = 'simple_app/product_detail.html'
    queryset = Product.objects.all()

class ProductCreateView(CreateView):
    template_name = 'simple_app/product_create.html'
    form_class = ProductForm


class ProductUpdateView(UpdateView):
    template_name = 'simple_app/product_create.html'
    form_class = ProductForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


# дженерик для удаления товара
class ProductDeleteView(DeleteView):
    template_name = 'simple_app/product_delete.html'
    queryset = Product.objects.all()
    success_url = '/products/'
