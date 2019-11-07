from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from .models import BlogPost
from .forms import BlogPostForm
from .forms import BlogPostModelForm

def blog_post_detail_page(request, slug):
    # Esta es una manera de manejar el error
    #
    # Get devuelve un objeto
    # filter devuelve un array de objetos
    #try:
    #    obj = BlogPost.objects.get(id=id)
    #except BlogPost.DoesNotExist:
    #    raise Http404
    # Esta es otra
    #
    #obj = get_object_or_404(BlogPost, slug=slug)
    #
    queryset = BlogPost.objects.filter(slug=slug)
    if queryset.count() == 0:
        raise Http404
    obj= queryset.first()
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)

##   CRUD
#
def blog_post_list_view(request):
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    print(qs)
    template_name = 'blog/list.html'
    context = {"object": qs}
    return render(request, template_name, context)

@staff_member_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    #evitar que etnre un usuario no autenitcado y que le devuelva otra pagina
    if not request.user.is_authenticated:
         return render(request, template_name, context)

    if form.is_valid():
#        print(form.cleaned_data)
        #obj = BlogPost.objects.create(**form.cleaned_data)
        obj = form.save(commit=False)
        #conseguimos el usuario que esta escribiendo el post
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()

    template_name = 'form.html'
    context = {"form": form, "title": "crear nuevo post"}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    queryset = BlogPost.objects.filter(slug=slug)
    if queryset.count() == 0:
        raise Http404
    obj= queryset.first()
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"form": form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method== "POST":
        obj.delete()
        return redirect('/blog')
    context = {"object": obj}
    return render(request, template_name, context)


