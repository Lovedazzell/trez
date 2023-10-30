from django.urls import path
from . import views
urlpatterns = [
     path('live_data/',views.live_data,name = 'live_data'),
     path('money_analysis/',views.MoneyAnalysis.as_view(),name = 'money_analysis'),
     path('custom_day_anl/',views.CustomDayDetail.as_view(),name = 'custom_day_anl'),
     path('admin_support/',views.AdminSupport.as_view(),name = 'admin_support'),
     path('support_detail/<int:pk>',views.SupportDetail.as_view(),name = 'support_detail'),
     path('download_feedback/',views.download_feedback,name = 'download_feedback'),
     
     path('admin_refund/',views.AdminRefund.as_view(),name = 'admin_refund'),

     path('withdraw_mn/',views.ManualUserWithdraw.as_view(),name = 'withdraw_mn'),
     path('confirm_status/<int:pk>',views.ConfirmWithdrawStatus.as_view(),name = 'confirm_status'),

     path('refund_detail/<int:pk>',views.RefundDetail.as_view(),name = 'refund_detail'),

     path('process_refund/<order_id>',views.process_refund,name = 'process_refund'),

]
