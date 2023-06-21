from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Category, ProductSearch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Count


# Create your views here.

class ProductList(ListView):
    model = Product
    ordering = '-pk'

    # template_name = 'product/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data()
        categories = Category.objects.order_by('name')
        context['categories'] = categories
        context['no_category_product_count'] = Product.objects.filter(category=None).count()

        return context


class ProductBestList(ListView):
    model = Product
    template_name = 'product/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(total_likes=Count('likes')).order_by('-views', '-total_likes')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductBestList, self).get_context_data()
        context['categories'] = Category.objects.order_by('name')
        context['no_category_product_count'] = Product.objects.filter(category=None).count()

        return context


class ProductDetail(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.increase_views()  # 조회 횟수 증가
        if self.request.user.is_authenticated:
            self.request.user.recently_viewed_products.add(self.object)  # 최근 본 제품 저장
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['best_products'] = Product.objects.exclude(pk=self.object.pk).order_by('-likes')[:6]
        return context


def categories_page(request, slug):
    if slug == 'no-category':
        category = '미분류'
        product_list = Product.objects.filter(category=None).order_by('-pk')
    else:
        category = Category.objects.get(slug=slug)
        product_list = Product.objects.filter(category=category).order_by('-pk')

    context = {
        'categories': Category.objects.order_by('name'),
        'category_less_post_count': Product.objects.filter(category=None).count(),
        'category': category,
        'product_list': product_list,
    }
    return render(request, 'product/product_list.html', context)


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'price', 'image', 'document', 'address', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            messages.success(self.request, '게시글이 올라갔습니다.', extra_tags='danger')
            form.instance.author = current_user
            return super(ProductCreate, self).form_valid(form)
        else:
            messages.error(self.request, '로그인을 먼저 해주세요.', extra_tags='danger')
            return redirect("/product/")


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'price', 'image', 'document', 'address', 'category']

    template_name = "product/product_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.likes.all():
        # 이미 좋아요를 누른 경우, 좋아요를 취소합니다.
        product.likes.remove(request.user)
    else:
        # 좋아요를 누르지 않은 경우, 좋아요를 추가합니다.
        product.likes.add(request.user)
    return redirect('product_detail', pk=product_id)


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated and request.user == product.author:
        product.delete()

    return redirect("/product/")


def product_search(request):
    query = request.GET.get('query')
    product_list = Product.objects.filter(Q(title__icontains=query) | Q(document__icontains=query))
    # 검색어 기록 저장
    if query:
        product_search, created = ProductSearch.objects.get_or_create(query=query)
        if not created:
            product_search.count += 1
            product_search.save()

    # 인기 검색어 추출
    popular_searches = ProductSearch.objects.all()[:5]  # 상위 5개 인기 검색어 추출
    context = {
        'product_list': product_list,
        'query': query,
        'categories': Category.objects.all(),
        'popular_searches': popular_searches,
    }
    return render(request, 'product/product_list.html', context)
