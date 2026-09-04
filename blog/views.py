from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from blog.models import BlogPost


class BlogListView(ListView):
    """Список блоговых записей (только опубликованные)"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Возвращаем только опубликованные записи"""
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Детальная страница блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Увеличиваем счётчик просмотров при открытии статьи"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    """Создание новой блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    """Редактирование блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        """После редактирования перенаправляем на страницу статьи"""
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')