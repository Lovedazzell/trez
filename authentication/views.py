from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView,RedirectView 
from django.views.generic.edit import FormView
from . forms import LoginForm , UserCreateForm
from django.utils.decorators import method_decorator
from . models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login , logout ,update_session_auth_hash
import uuid
from .tasks import email_token_send
from authentication.forms import UserChangePassword , EditProfileForm
from .helpers import logout_required , verification_required
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.





# user login view
@csrf_exempt
@logout_required
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request,data =request.POST)
        uname = request.POST.get('username')
        upass = request.POST.get('password')

        Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # validate if user enter their number
        if Pattern.match(uname) != None:
            if User.objects.filter(mobile = int(uname)).exists():
                verified = User.objects.filter(mobile = int(uname)).first()

                # if form.is_valid():
                if verified.is_verified == True:
                    user = authenticate(username = verified.email, password = upass)
                    if user is not None:
                        login(request,user)
                        return HttpResponseRedirect('/profile/')
                    else:
                        messages.error(request,' Wrong username or password')
                        return HttpResponseRedirect('/auth/login/')
                else:
                    return HttpResponseRedirect('/auth/check_email/')
         
            else:
                messages.error(request,' Username not found')
                return HttpResponseRedirect('/auth/login/')
        
        # validate if user enter their email
        elif re.fullmatch(regex,uname ) != None:
            if User.objects.filter(email = uname).exists():
                verified = User.objects.filter(email = uname).first()

                if form.is_valid():
                    if verified.is_verified == True:
                        user = authenticate(username = uname, password = upass)
                        if user is not None:
                            login(request,user)
                            return HttpResponseRedirect('/profile/')
                        else:
                            messages.error(request,' Wrong username or password')
                            return HttpResponseRedirect('/auth/login/')
                    else:
                        return HttpResponseRedirect('/auth/check_email/')
                else:
                    messages.error(request,' User not found')
                    return HttpResponseRedirect('/auth/login/')

            else:
                messages.error(request,' Username not found')
                return HttpResponseRedirect('/auth/login/')
        else:
            messages.error(request,' Please enter register email or number')
            return HttpResponseRedirect('/auth/login/')

        
    else:
        context = {'form':LoginForm()}
        return render(request,'authentication/login.html',context)





  

# user creation view

@method_decorator(logout_required,name = 'dispatch')
class UserSingup(FormView):
    template_name= 'authentication/singup.html'
    form_class = UserCreateForm
    success_url = '/auth/check_email/'
    
    def form_valid(self, form):
        u_email =form.cleaned_data['email']
        if User.objects.filter(email = u_email).exists():
            messages.error(self.request,' Account already exists. Try to login or forget password.')
            return HttpResponseRedirect('/auth/login/')
        u_username =form.cleaned_data['username']
        password =form.cleaned_data['password1']
        obj = User(email = u_email,username = u_username, not_google_verified = True)
        obj.set_password(password)
        obj.email_token = str(uuid.uuid4())
        obj.save()
        token = obj.email_token
        email_token_send.delay(u_email,token)
       
        return super().form_valid(form)

# User Verification

class Verify(TemplateView):
    template_name= 'authentication/verify_account.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        token = kwargs['pk']
        try:
            data = User.objects.filter(email_token = token).first()
            data.is_verified = True
            data.save()
        except Exception as e:
          pass
        return context



# Check email message
class CheckEmail(TemplateView):
    template_name = 'authentication/check_email.html' 

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
      
        return context

    def post(self,request):
        email = self.request.POST['email']
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex,email ) != None:
            if User.objects.filter(email = email).exists():
                unverified_user = User.objects.filter(email = email).first()
                token = unverified_user.email_token
                email_token_send.delay(unverified_user.email,token)

                messages.success(self.request,' verification mail send succesfully.')
                return HttpResponseRedirect('/auth/check_email/')
            else:    
                messages.error(self.request,' Account not exist.')
                return HttpResponseRedirect('/auth/check_email/')
        else:
            messages.error(self.request,' Please enter a valid email.')
            return HttpResponseRedirect('/auth/check_email/')



# Trems and conditions

class TermsAndConditions(TemplateView):
    template_name = 'authentication/terms.html'


# Privacy and policies

class PrivacyPolicy(TemplateView):
    template_name = 'authentication/privacy_policy.html'


# Contact us page 
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class ContactUs(TemplateView):
    template_name = 'authentication/contact_us.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


# user logout view
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class UserLogout(RedirectView):
    
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/auth/login/')




# password change view    
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class ChangePassword(TemplateView):
    template_name = 'authentication/password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserChangePassword(self.request.user)
        return context

    def post(self,request):
        form = UserChangePassword(user = request.user , data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')





# Edit and view user profile
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class EditProfile(TemplateView):
    template_name = 'authentication/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] =EditProfileForm(instance = self.request.user) 
        return context

    def post(self,request):
        form = EditProfileForm( request.POST ,request.FILES ,instance=request.user )
        if form.is_valid():
            form.save()
            messages.success(request,' profile picture update')
            return HttpResponseRedirect('/auth/edit_profile/')
        else:
            messages.error(request,' Invalid details')
            return HttpResponseRedirect('/auth/edit_profile/')
