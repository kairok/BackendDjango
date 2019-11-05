from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import *



urlpatterns = [


    path('reqall/', ReqView.as_view()),
    path('specall/', GetSpecView.as_view()),
    path('findreq/', FindreqView.as_view()),
    path('allmaster/', GetAllMasterView.as_view()),
    path('addreq/', AddReqView.as_view()),
    path('editreq/', EditreqView.as_view()),

    path('allemplyee/', GetAllEmplyeesView.as_view()),
    path('findemplyee/', FindmployeeView.as_view()),
    path('editemplyee/', EditmployeeView.as_view()),
path('addemplyee/', AddmployeeView.as_view()),
path('delemplyee/', DelemployeeView.as_view()),

    path('allfirm/', GetAllFirmView.as_view()),
    path('findfirm/', FindFirmView.as_view()),
    path('editfirm/', EditFirmView.as_view()),
path('addfirm/', AddFirmView.as_view()),
path('delfirm/', DelFirmView.as_view()),

path('analitic/', RequestchartView.as_view()),
path('chartspec/', SpecchartView.as_view()),
path('chartallstat/', AllStatchartView.as_view()),

path('editspec/', EditSpecView.as_view()),


]