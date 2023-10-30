from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . models import Transtions ,UserCollection ,MazorCollection
from authentication.helpers import verification_required 
from .models import Notification,CountdownSeconds



# main dashboard
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class Profile(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)        

        if  UserCollection.objects.filter(user__email = self.request.user).exists():
            context['data']  = UserCollection.get_user_gem_detail(self.request.user.reffer_code)   
        if MazorCollection.objects.all().exists():
            context['history_data'] = MazorCollection.objects.latest('created')  
        return context
            



@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class ThreeMinutesCount(TemplateView):
    template_name = 'core/tmcount.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
   
      
        if  UserCollection.objects.filter(user__email = self.request.user).exists():
            context['data']  = UserCollection.get_user_gem_detail(self.request.user.reffer_code)   
        if MazorCollection.objects.all().exists():
            context['history_data'] = MazorCollection.objects.latest('created')
        if CountdownSeconds.objects.all().exists():
            count = CountdownSeconds.objects.all().first()
            context['sec'] = 177 - count.sec
                    
        return context



# Settings view
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class Settings(TemplateView):
    template_name = 'core/settings.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)   
        return context
    

# view all notification
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class Notifications(TemplateView):
    template_name = 'core/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = Notification.objects.all().order_by('-created')
        return context
    



# User all transtions
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class UserTransitions(TemplateView):
    template_name ='core/transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail = Transtions.objects.filter(user__email = self.request.user).exclude(status =False).order_by('-created')
        context['history'] = detail
        return context

# Transtions details of perticular user
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class TransitionDetail(TemplateView):
    template_name = 'core/tran_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element = Transtions.objects.get(id = kwargs['pk'])
        context['detail'] = element
        return context


# Shows the Notification detail
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class NotificationDisplay(TemplateView):
    template_name = 'core/notifi_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        display_notification = Notification.objects.get(id =kwargs['pk'] )
        context["data"] = display_notification
        return context
    

# market place
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class MarketPlace(TemplateView):
    template_name = 'core/market.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    



# User Spent gems History
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class UserGems(TemplateView):
    template_name = 'core/gems_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = UserCollection.objects.filter(user__email = self.request.user).order_by('-created')
        context['data'] = data
        return context

# World wide history
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class WorldHistory(TemplateView):
    template_name = 'core/global_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = MazorCollection.objects.all().order_by('-created')[:11]
        context['data'] = data
        return context

        

@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class RefferData(TemplateView):
    template_name   = 'core/reffer_data.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        return context



