from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [

    path('',views.homepage,name="homepage"),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    path('forgotpassword/confirm/<str:passwordchangerid>',views.lemmecheck,name="lemmecheck"),

    path('notices',views.nots,name="nots"),
    path('contact',views.contact,name="contact"),
    path('studentlogin',views.studentlogin,name="studentlogin"),
    path('studentlogin/student',views.sthome,name="sthome"),
    path('studentlogin/logout',views.stlogout,name="stlogout"),
    path('stafflogin/staff',views.staffhome,name="staffhome"),
    path('stafflogin',views.stafflogin,name="stafflogin"),
    path('stafflogin/logout',views.stafflogout,name="stafflogout"),
    path('adminlogin',views.adminlogin,name="adminlogin"),
    path('adminlogin/admin',views.adlog,name="adlog"),
    path('adminlogin/logout',views.checkout,name="checkout")
    
    

]
