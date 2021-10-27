from django.shortcuts import render, redirect
from .models import Post
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name='index.html'
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        return posts

index = IndexView.as_view()

class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    success_url = reverse_lazy('timeline:index')
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました。')
        return super(CreateView, self).form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, '投稿を失敗しました。')
        return redirect('timeline:index')



create = CreateView.as_view()