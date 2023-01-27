
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


# def login_user(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse_lazy('users:profile_user'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context=context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login_user')
    success_message = 'Вы успешно зарегистрировались!'
    title = 'Store - Регистрация'


# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse_lazy('users:login_user'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context=context)

# @login_required
# def logout_user(request):
#     logout(request)
#     return redirect('index')


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile_user', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.request.user)
    #     return context

# @login_required
# def profile_user(request):
#     if request.method == "POST":
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно обновили данные!')
#             return HttpResponseRedirect(reverse('users:profile_user'))
#     else:
#         form = UserProfileForm(instance=request.user)
#         baskets = Basket.objects.filter(user=request.user)
#
#         # total_quantity = sum([basket.quantity for basket in baskets])
#         # total_sum = sum([basket.sum() for basket in baskets])
#
#
#     context = {'title': 'Store - Профиль',
#                'form': form,
#                'baskets': baskets,
#                # 'total_quantity': total_quantity,
#                # 'total_sum': total_sum,
#                }
#     return render(request, 'users/profile.html', context=context)


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение email'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
