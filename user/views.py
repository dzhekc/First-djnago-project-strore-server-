from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth,messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from user.common import TitleMixin
from user.models import User
from user.forms import UserLoginForm,UserRegistrationForm,UserProfileForm
from products.models import Basket
from user.forms import UserResetPasswordForm

from user.models import EmailVerification


# Create your views here.


class UserLoginView(TitleMixin,LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')

    title = 'Авторизация'



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request,'users/login.html',context=context)



class UserRegestrationView(SuccessMessageMixin,TitleMixin,CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = 'Store-регистрация'
    success_message = "Вы успешно зарегистрировались "





def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request,"Вы успешно зарегистрировались")
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request,'users/register.html',context=context)


class UserProfileView(TitleMixin,UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'
    def get_success_url(self):
        return reverse_lazy('users:profile',args=(self.object.id),)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView,self).get_context_data()
        context['basket'] = Basket.objects.filter(user=self.request.user)
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(user=user,code=code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified = True
            user.save()
            return super().get(request,args,kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))




# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {'title': 'profile','form':form, 'basket':Basket.objects.all(),}
#     return render(request,'users/profile.html',context=context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class PasswordResetEmailView(PasswordResetView):
    form_class = UserResetPasswordForm
    template_name = 'users/password_res.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('index')

class PasswordResetEmailConfirm(PasswordResetConfirmView):
    template_name = 'users/password_confirm.html'
    success_url = reverse_lazy('users:password_complete')

class PasswordComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_confirm.html'


# class PasswordResetConfirmView(SuccessMessageMixin, FormView):