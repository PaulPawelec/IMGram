from .forms import Register_Form, User_Edit_Form, Password_Change_Form
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse
from testgram.models import Profile

class UserRegisterView(generic.CreateView):
    form_class = Register_Form
    # profile_form = ProfileForm(instance=request.user.profile)
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = User_Edit_Form
    # form_class = UserChangeForm
    template_name = 'registration/user_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class ChangePasswordView(PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = Password_Change_Form
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'registration/password_success.html', {})