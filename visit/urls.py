from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'visit'

urlpatterns = [
    path('', views.home, name='home'),
    path('newvisitor', views.newvisitor, name='newvisitor'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visitor/', views.visitors, name='visitor'),


    path('Applicantsearch/',views.Applicantsearch,name='Applicantsearch'),
    path('visitorsearch/',views.searchVisitor,name='searchvisitor'),
    path('reject/<int:id>', views.RejectVisitorRequest, name="rejection"),
    path('changepass/', views.ChangePasswordView, name="changepass"),
    path('EditVisitortime/<int:id>',views.EditVisitorTime, name="Accept"),
    path('applicantSignup/', views.ApplicantSignUp, name='applicantSignup'),
    path('RemaningTimeToMeet/<int:pk>', views.RemaningTimeToMeet, name='RemaningTimeToMeet'),
    path('security_page/',views.security_page,name='security_page'),
    path('EntryTime/',views.EntryTime,name='EntryTime'),
    path('AcceptApplicents/<int:id>',views.AcceptApplicents,name='AcceptApplicents'),
    path('NewApplicants/',views.NewApplicants,name='NewApplicants'),
    path('RejactApplicants/<int:id>',views.RejactApplicants,name='RejactApplicants'),
    path('sineup/',views.sineup,name='sineup'),
    path('register/',views.register,name='register'),
    path('ApplicantInfo/<int:id>',views.ApplicantInfo,name='ApplicantInfo'),

    # path('jet_api/', include('jet_django.urls')),
    # url(r'^jet/', include('jet.urls', 'jet')), #django jet urls
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS


]
