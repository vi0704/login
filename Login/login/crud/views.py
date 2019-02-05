from django.shortcuts import render,render_to_response,resolve_url
from .forms import userform
from django.http import HttpResponse,JsonResponse
from django.template.response import TemplateResponse
from .models import Name
from django.utils.crypto import get_random_string
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
import warnings
from .models import Name
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate,get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .forms import SignUpForm,LoginForm,PasswordChangeForm,FeedbackForm,GenerateRandomUserForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm,SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from .models import user_token
from django.utils.deprecation import RemovedInDjango21Warning
from django.contrib.auth.views import password_reset
from django.views.generic.base import TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from .task import create_random_user_accounts
UserModel = get_user_model()
import re
from django.http import HttpRequest

# def signup(request):
#     if request.method == 'POST':
#         form = userform(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('Thanks')
#
#     else:
#         form = userform()
#
#     return render(request, 'crud/signup.html', {'form': form})

# class user_list(ListView):
#     model='Name'
#     template_name = 'crud/list.html'


def list(request):
    name = Name.objects.all()
    context = {'name': name}
    return render(request, 'crud/list.html', context)

class DetailCreate(LoginRequiredMixin,CreateView):
    model = Name
    fields = "__all__"
    login_url = '/login/'
    redirect_field_name = 'login'



class DetailUpdate(LoginRequiredMixin,UpdateView):
    model=Name
    fields = "__all__"
    login_url = '/login/'
    redirect_field_name = 'login'

class DetailDelete(LoginRequiredMixin,DeleteView):
    model=Name
    fields='all'
    login_url = '/login/'
    redirect_field_name = 'login'

class NameDetailView(LoginRequiredMixin,DetailView):
    model=Name
    login_url = '/login/'
    redirect_field_name = 'login'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('http://127.0.0.1:8000/userlist/')

    else:
        form = SignUpForm()
    return render(request, 'crud/signup.html', {'form': form})

class user_list(ListView):
    model=User
    fields='all'
    template_name = 'crud/user_list.html'


from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request,'username or password not correct')
            return redirect('http://127.0.0.1:8000/login/')

    else:
        form = LoginForm()
    return render(request, 'crud/login.html', {'form': form})

@login_required(login_url='http://127.0.0.1:8000/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated! Login again to continue.')
            return redirect('http://127.0.0.1:8000/login/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'crud/newp.html', {
        'form': form
    })





# def forget_password(sender, instance, User, *args, **kwargs):
#     if not instance.is_verified:
#         # Send verification email
#         send_verification_email.delay(instance.pk)
#
#
#     User.post_save.connect(User_post_save, sender=User)


class GenerateRandomUserView(FormView):
    template_name = 'crud/generate_random_users.html'
    form_class = GenerateRandomUserForm
    # def get_users(self, email):
    #     """Given an email, return matching user(s) who should receive a reset.
    #
    #     This allows subclasses to more easily customize the default policies
    #     that prevent inactive users and users with unusable passwords from
    #     resetting their password.
    #     """
    #     active_users = UserModel._default_manager.filter(**{
    #         '%s__iexact' % UserModel.get_email_field_name(): email,
    #         'is_active': True,
    #     })
    #     return (u for u in active_users if u.has_usable_password())
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        forgot_password.delay(self.request)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return HttpResponse('check Your mail')


class UsersListView(ListView):
    template_name = 'crud/user_list1.html'
    model = User


def sendEmail(request, subject, message, sender, to):
    send_mail(
        subject,
        message,
        sender,
        [to],
        fail_silently=True
)


def forgot_password(request):
    if request.method == 'POST':
        subject = 'Change Password'
        key = get_random_string(length=30)
        email = request.POST.get('email')
        sender = 'smartboyvicky05@gmail.com'
        user = User.objects.get(email=email)

        print(user)
        try:
            User.objects.get(email=email)
            user = User.objects.get(email=email)
            user_id = user.id
            try:
                user_token.objects.get(user_id=user_id).delete()
            except:
                pass
            username = user.username
            key = 'http://127.0.0.1:8000/' + 'reset-link/' + username + '!!!' + key + '/'
            sendEmail(request, subject, key, sender,email)
            token = user_token.objects.create(token=key, user=user)
            token.save()
            return JsonResponse(data={'success': 'true'})
            # return render(request, 'users/registration/password_reset_done.html')

        except User.DoesNotExist:
            return JsonResponse(data={'success': 'false'})
            # return  render(request, 'users/registration/wrong_reset_email.html')

    else:
        form = PasswordResetForm
    return render(request, 'registration/password_reset_form.html', {'form':form,})


# def stripe(request):
#     return render(request,'crud/stripe')










