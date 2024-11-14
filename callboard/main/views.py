from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from .filters import *


class BoardAll(ListView):
    model = Advertisement
    template_name = 'main/board.html'
    context_object_name = 'posts'
    ordering = '-id'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BoardFilter(self.request.GET, queryset)
        return self.filterset.qs


class AdvertisementDetails(DetailView):
    model = Advertisement
    template_name = 'main/details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(post=self.get_object().id)
        return context


class AdvertisementCreate(LoginRequiredMixin, CreateView):
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'main/create.html'

    raise_exception = True
    permission_required = ('main.add_post',)
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ResponseCreate(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'main/respond.html'
    raise_exception = True

    def form_valid(self, form):
        form.instance.user = self.request.user
        post = self.kwargs.get('pk')
        form.instance.post = Advertisement.objects.get(id=post)
        return super().form_valid(form)

    def test_func(self):
        post_id = self.kwargs.get('pk')
        post = Advertisement.objects.get(pk=post_id)
        return self.request.user != post.author

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'pk': self.kwargs['pk']})


class AdvertisementUpdate(UserPassesTestMixin, UpdateView):
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'main/create.html'

    raise_exception = True
    permission_required = ('main.change_post',)
    # success_url = reverse_lazy('board')

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'pk': self.kwargs['pk']})


class AdvertisementDelete(UserPassesTestMixin, DeleteView):
    model = Advertisement
    template_name = 'main/delete.html'
    success_url = reverse_lazy('board')
    raise_exception = True

    def test_func(self):
        return self.request.user == self.get_object().author


class ResponseDelete(UserPassesTestMixin, DeleteView):
    model = Response
    template_name = 'main/delete.html'

    raise_exception = True

    def test_func(self):
        return self.request.user == self.get_object().post.author

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'pk': self.kwargs['post_id']})


@csrf_protect
def my_advertisements(request):
    # posts
    queryset = Advertisement.objects.filter(author=request.user)

    # responses
    responses = {}
    for post in queryset:
        responses[post] = Response.objects.filter(post=post).order_by('-id')[:3]

    # subs
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscription.objects.filter(user=request.user).update(is_subscribed=True)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user).update(is_subscribed=False)

    subscribed = Subscription.objects.get(user=request.user)

    # filtration
    queryset = MyBoardFilter(request.GET, queryset).qs

    # pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'main/me.html', {
        'posts': page_obj,
        'subscribed': subscribed,
        'responses': responses,
    })


def response_answer(request, pk, post_id):
    response = Response.objects.get(pk=pk)
    post = Advertisement.objects.get(pk=post_id)

    if response.user == post.author:
        responder_email = response.user.email
    else:
        raise PermissionDenied

    url = reverse_lazy('details', kwargs={'pk': post_id})

    if responder_email:
        send_mail(
            subject='На Ваш отклик ответили',
            message=f'Автор "{post}" ответил на ваш отклик',
            from_email=None,
            recipient_list=[responder_email]
        )
    return redirect(url)


def index(request):
    return render(request, 'main/index.html')
