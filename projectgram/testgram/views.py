from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Profile, Comment
from .forms import PostForm, Post_Update_Form, Comment_Add_Form
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User


class HomeView(ListView):
    model = Post
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            follows_users = user.profile.follows.all()
            follows_posts = Post.objects.filter(author_id__in=follows_users)

            context = {
                'posts': follows_posts,
            }

            return context
        else:
            posts = Post.objects.all()

            context = {
                'posts': posts,
            }

            return context


class Post_Details_View(DetailView):
    model = Post
    template_name = 'post_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Post_Details_View, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])

        form = Comment_Add_Form
        comments = post.comments.all()

        likes_count = post.likes_count

        liked = False
        if post.like.filter(id=self.request.user.id).exists():
            liked = True

        context['likes_count'] = likes_count
        context['liked'] = liked
        context['comment_form'] = form
        context['comments'] = comments

        return context


    def post(self, request, *args, **kwargs):
        new_comment = Comment(text=request.POST.get('text'),
                                  author=self.request.user,
                                  post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class Post_List_View(ListView):
    template_name = 'post_view.html'
    model = Post
    context_object_name = 'posts'


class Post_Add_View(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_add.html'
    success_url = reverse_lazy('home')

    # ordering = ['publication_date']
    # fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Post_Update_View(UpdateView):
    model = Post
    form_class = Post_Update_Form
    template_name = 'post_update.html'
    # fields = '__all__'


class Post_Delete_View(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


class Profile_List_View(ListView):
    template_name = 'users_list.html'
    model = Profile
    context_object_name = 'profiles'


class Profile_Search_View(ListView):
    template_name = 'users_list.html'
    model = Profile
    context_object_name = 'profiles'

    def get_queryset(self):
        result = super(Profile_Search_View, self).get_queryset()
        query = self.request.GET.get('query')
        if query:
          postresult = Profile.objects.filter(user__username__contains=query)
          result = postresult
        else:
           result = None
        return result

class Profile_View(DetailView):
    model = Profile
    template_name = 'profile_user.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(Profile_View, self).get_context_data(*args, **kwargs)
        user_page = get_object_or_404(Profile, id=self.kwargs['pk'])
        followers_count = user_page.followers_count
        follows_count = user_page.follows_count

        user = self.get_object().user_id

        followed = False
        if user_page.followers.filter(id=self.request.user.id).exists():
            followed = True

        context['user_page'] = user_page
        context['posts'] = Post.objects.filter(author_id=user)
        context['followers_count'] = followers_count
        context['follows_count'] = follows_count
        context['followed'] = followed

        return context


class Profile_Edit_View(UpdateView):
    model = Profile
    template_name = 'profile_edit.html'
    fields = ['avatar', 'biography']


class Comment_Add_View(CreateView):
    model = Comment
    form_class = Comment_Add_Form
    template_name = 'comment_add.html'
    # fields = '__all__'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)


class Comment_Delete_View(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('home')


def Likes_View(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))


def Follows_View(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    user = request.user
    user_profile = User.objects.get(pk=profile.user.id)

    followed = False
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
        user.profile.follows.remove(user_profile)
        followed = False
    else:
        profile.followers.add(request.user)
        user.profile.follows.add(user_profile)
        followed = True

    return HttpResponseRedirect(reverse('profile_details', args=[str(pk)]))


# def Follows_View(request, pk):
#     current_user = request.user
#     other_user = User.objects.get(pk=request.POST.get('profile_id'))
#
#     if other_user not in current_user.profile.follows.all():
#         current_user.profile.follows.add(other_user)
#         other_user.profile.followers.add(current_user)
#
#     else:
#         current_user.profile.follows.remove(other_user)
#         other_user.profile.followers.remove(current_user)
#     return HttpResponseRedirect(reverse('profile_details', args=[str(pk)]))
