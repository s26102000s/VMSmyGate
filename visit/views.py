import json

from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.edit import DeleteView

from .forms import StudentVisitForm, HrUpdateTimeForm,  SineUpForm,SineUpForm1,SecurityTimeForm, PasswordChangingForm
from .models import Student,Applicant
from .decorators import unauthenticated_user
from datetime import datetime
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
# Create your views here.
    
# from .filters import StudentFilter




import math
import http

def sineup(request):
    form = SineUpForm()
    if request.method=="POST":
        role=request.POST['role']
        status = "pending"
        form = SineUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return HttpResponse("Thanks")
            form = SineUpForm()
            return render(request,"visit/sineup.html",{'error1':"User Succussfully Registered",'form': form})
        else:
            return render(request,"visit/sineup.html",{'error':"User Alredy Exist With This Details",'form': form})
    return render(request,"visit/sineup.html",{'form': form})

def register(request):
    form = SineUpForm1()
    if request.method=="POST":
        role=request.POST['role']
        status = "Accepted"
        form = SineUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            id=Applicant.objects.all().count()
            ap = Applicant.objects.get(pk=id)
            name_r = ap.username
            email_r = ap.email

            password_r = name_r.title()+'@123'
            recipent_email=(ap.email,)
            email_from=settings.EMAIL_HOST_USER
            try:
                user=User.objects.create_user(name_r, email_r, password_r,is_staff=True)
                Applicant.objects.filter(pk=id).update(status="Accepted")
                my_group  = Group.objects.get(name=ap.role) 
                # my_group.user_set.add(ap)
                user.groups.add(my_group)
                print(my_group)
                subject="Application Accepted"
                messages=(f"Your Applicatition Has Been Approved.Your Username is --> {name_r} and Password is --> {password_r}")
                send_mail(subject, messages,email_from, recipent_email)
                context={}
                form = SineUpForm1()

                context['form']=form
                context['error1']="User Created Succesfully"
                return render(request,'visit/register.html',context)
            except:
                return render(request,"visit/register.html",{'error':"User Alredy Exist With This Details",'form': form})
        else:
            return render(request,"visit/register.html",{'error':"User Alredy Exist With This Details",'form': form})
    return render(request,"visit/register.html",{'form': form})

def newvisitor(request):
    form = StudentVisitForm()
    if request.method == 'POST':
        form = StudentVisitForm(request.POST, request.FILES)
        if form.is_valid():
            
            status = request.POST['status']
            from_time=request.POST['from_time']
            to_time=request.POST['to_time']
            date=request.POST['date']
            time=datetime.now().time()
            date1=datetime.now().date()
            date_time_str = date+" "+from_time
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            from_time1=date_time_obj.time()
            date2=date_time_obj.date()
            if date2>date1:
                if  from_time>to_time:
                    return render(request,'visit/newvisitor.html', {'form': form,'error':'please enter a valid time duration'})
                else:
                    form.save()
            elif from_time1<time and from_time>to_time:
                return render(request,'visit/newvisitor.html', {'form': form,'error':'please enter a valid time duration'})
            else:
                form.save()
            id= Student.objects.all().count()
            st= Student.objects.get(pk=id)
            Student.objects.filter(pk=id).update(status="Accepted")
            print(st.email)
            recipent_email=(st.email,)
            subject="Meeting confirmed"
            messages=(f"you can check your remaning time to meeting is here--> http://127.0.0.1:8000/RemaningTimeToMeet/{st.id} and your id is {st.id}")
            email_from=settings.EMAIL_HOST_USER
            send_mail(subject, messages,email_from, recipent_email)
            form = StudentVisitForm()
            return render(request, 'visit/newvisitor.html', {'form': form,"messages":"Meeting Registered Succussfully"})
            # messages.success(request, 'A visit is requested by'+name)
    return render(request, 'visit/newvisitor.html', {'form': form})



def home(request):
    form = StudentVisitForm()
    if request.method == 'POST':
        form = StudentVisitForm(request.POST, request.FILES)
        if form.is_valid():
            
            status = request.POST['status']
            from_time=request.POST['from_time']
            to_time=request.POST['to_time']
            date=request.POST['date']
            time=datetime.now().time()
            date1=datetime.now().date()
            date_time_str = date+" "+from_time
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            from_time1=date_time_obj.time()
            date2=date_time_obj.date()
            if date2>date1:
                if  from_time>to_time:
                    return render(request,'visit/home.html', {'form': form,'error':'please enter a valid time duration'})
                else:
                    form.save()
                    return HttpResponse("Thanks")
            elif from_time1<time:
                return render(request,'visit/home.html', {'form': form,'error':'please enter a valid time duration time is not before now'})
            else:
                form.save()
                form = StudentVisitForm()
                return render(request, 'visit/home.html', {'form': form,"messages":"Request sent Succussfully"})
            # messages.success(request, 'A visit is requested by'+name)
    return render(request, 'visit/home.html', {'form': form})


@unauthenticated_user 
def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('visit:dashboard'))
        else:
            messages.info(request, 'Username or Password is incorrect!!')
    return render(request, 'visit/login.html')

@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return redirect(reverse('visit:login'))
    # return redirect('/login/')


@login_required(login_url='/login/')
def dashboard(request):
    total_visit = Student.objects.all().count()
    completed_visit = Student.objects.filter(status="Completed").count()
    panding_visit = Student.objects.filter(status="Accepted").count()
    completed_visit_today = Student.objects.filter(status="Completed",date=datetime.now().date()).count()
    panding_visit_today = Student.objects.filter(status="Accepted",date=datetime.now().date()).count()
    today_total_visit=Student.objects.filter(date=datetime.now().date()).count()
    
    
    context = {'total_visit': total_visit,'panding_visit':panding_visit,"completed_visit_today":completed_visit_today,"completed_visit":completed_visit,"today_total_visit":today_total_visit,"panding_visit_today":panding_visit_today}
    if request.user.is_superuser:
        return render(request, 'visit/dashboard.html', context)
    elif request.user.has_perm("visit.is_hr"):
        return render(request, 'visit/dashboard.html', context)
    elif request.user.has_perm("visit.is_Security"):
        visitor = Student.objects.all().order_by('id').reverse()
        data = visitor.values()
        page_number = request.GET.get('page')
        context = pagination(visitor, page_number)
        return render(request, 'visit/Security.html', context)
    else:
        return render(request, 'visit/dashboard.html', context)

def pagination(visitor, page_number):
    paginator = Paginator(visitor, 7, orphans=1)
#    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print("Page Object:", page_obj)

    context = {'page_obj': page_obj}

    return context

# @login_required(login_url='/login/')
# @permission_required('visit.is_hr')
# def visitors(request):
#     visitor = Student.objects.all().order_by('id')
#     data = visitor.values()
#     page_number = request.GET.get('page')
#     context = pagination(visitor, page_number)
#     return render(request, 'visit/visitor1.html', context)
@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def visitors(request):
    visitor = Student.objects.all().order_by('date').reverse()
    pending_visit = Student.objects.filter(date=datetime.now().date()).filter(status='pending')[0:6:-1]
    print("pending visit : ", pending_visit)
    data = visitor.values()
    page_number = request.GET.get('page')
    context = pagination(visitor, page_number)
    context['pending_visit'] = pending_visit
    return render(request, 'visit/visitor1.html', context)

@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def NewApplicants(request):
    ap = Applicant.objects.all()
    page_number = request.GET.get('page')
    context = pagination(ap, page_number)
    return render(request,'visit/newApplicants.html',context)


@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def searchVisitor(request):
    
    search_text = request.GET['searchText']
    print("search_text : ", search_text)
    visitors = None
    if len(search_text.strip()) > 0:
        visitors = Student.objects.filter(
            name__icontains=search_text) | Student.objects.filter(name__istartswith=search_text) | Student.objects.filter(
            purpose__icontains=search_text) | Student.objects.filter(
            purpose__istartswith=search_text) | Student.objects.filter(
            contact__icontains=search_text) | Student.objects.filter(
            status__istartswith=search_text) | Student.objects.filter(
            status__istartswith=search_text)
        visitor=visitors
        page_number = request.GET.get('page')
        context = pagination(visitor, page_number)
        
        context['searchText']=search_text
        return render(request, 'visit/visitor1.html', context)
        # else:
        #     return render(request, 'visit/visitor1.html', context)

        # return render(request, 'visit/visitor1.html', {"visitors": visitors})
    search_text=""
    page_number = request.GET.get('page')
    visitors = Student.objects.all()
    print("visitors : ", visitors)
    context = pagination(visitors, page_number)
    context['searchText']=search_text
    # return render(request, 'visit/visitor1.html', {"visitors": visitors})
    return render(request, 'visit/visitor1.html', context)

@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def Applicantsearch(request):
    search_text = request.GET['searchText']
    print("search_text : ", search_text)
    visitors = None
    if len(search_text.strip()) > 0:
        visitors = Applicant.objects.filter(
            username__icontains=search_text) | Applicant.objects.filter(username__istartswith=search_text) | Applicant.objects.filter(
            lastname__icontains=search_text) | Applicant.objects.filter(
            lastname__istartswith=search_text) | Applicant.objects.filter(
            role__icontains=search_text) | Applicant.objects.filter(
            role__istartswith=search_text) | Applicant.objects.filter(
            firstname__icontains=search_text) | Applicant.objects.filter(
            firstname__istartswith=search_text) | Applicant.objects.filter(
            contact__icontains=search_text) | Applicant.objects.filter(
            status__istartswith=search_text) | Applicant.objects.filter(
            status__istartswith=search_text)
        print('visitors :', visitors)
        visitor=visitors
        page_number = request.GET.get('page')
        context = pagination(visitor, page_number)
        
        context['searchText']=search_text

        return render(request, 'visit/newApplicants.html',context)
    search_text=""
    visitors = Applicant.objects.all()
    print("visitors : ", visitors)
    page_number = request.GET.get('page')
    context = pagination(visitors, page_number)
    context['searchText']=search_text
    return render(request, 'visit/newApplicants.html', context)


# def search_visitor(request):

#    search_str = json.loads(request.body).get('searchText')

#    visitors = Student.objects.filter(
#        name__istartswith=search_str) | Student.objects.filter(
#        email__icontains=search_str) | Student.objects.filter(
#        purpose__icontains=search_str) | Student.objects.filter(
#        contact__icontains=search_str)

#    data = visitors.values()

#    return JsonResponse(list(data), safe=False)



@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def RejectVisitorRequest(request, id):
    if request.method == 'POST':
        Student.objects.filter(pk=id).update(status="Rejected")
        st = Student.objects.get(pk=id)
        recipent_email=(st.email,)
        subject="Meeting confirmed"
        messages=(f"Your Applicatition Has Been Rejected")
        email_from=settings.EMAIL_HOST_USER
        send_mail(subject, messages,email_from, recipent_email)
        return HttpResponseRedirect('/visitor/')
    # st=Student.objects.filter(pk=id)
    return render(request, "visit/VisitorDetail.html", {"student": st})

# @login_required(login_url='/login/')
# @permission_required('visit.is_Security')
# def security_page(request):
#     return render(request,'visit/Security.html')

@login_required(login_url='/login/')
@permission_required('visit.is_Security')
def security_page(request):
    visitor = Student.objects.all().order_by('date').reverse()
    data = visitor.values()
    page_number = request.GET.get('page')
    context = pagination(visitor, page_number)
    return render(request, 'visit/Security.html', context)

@login_required(login_url='/login/')
@permission_required('visit.is_Security')
def EntryTime(request):
    try:
        try:
            pk=int(request.GET['searchText'])
        except:return  render(request,'visit/Security.html',{"error":"wrong id, id must be a number"})
        st = Student.objects.get(id=pk)       
        fm = SecurityTimeForm(request.POST or None, instance=st)
        if request.method == "POST" :
            if fm.is_valid():
                entrytime=request.POST.get('student_entry_time')
                exittime=request.POST.get('student_exit_time')
                print(entrytime,type(entrytime),exittime,type(exittime))
                if entrytime!="":
                    time=datetime.now().time()
                    date1=str(datetime.now().date())
                    date_time_str = date1+" "+entrytime
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                    from_time1=date_time_obj.time()
                    date2=date_time_obj.date()
                    if from_time1<time:
                        return render(request,'visit/Entry.html', {'student': st,'form': fm,'error':'please enter a valid time duration time is not before now'})
                
                    elif exittime!="" and entrytime>exittime:
                        return render(request,'visit/Entry.html', {'student': st,'form': fm,'error':'please enter a valid time duration '})
                    else:
                        fm.save()
                        Student.objects.filter(pk=st.id).update(status="Completed")
                else:
                    return render(request,'visit/Entry.html', {'student': st,'form': fm,'error':'please enter Entry time '})
                
                return render(request,'visit/Entry.html',{'student': st, 'form': fm}) 
        return render(request,'visit/Entry.html',{'student': st, 'form': fm })
    except:
        return render(request,'visit/Security.html',{'error':'this id does not Exist in the system'})
@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def EditVisitorTime(request, id):
    id=id
    if request.method == 'POST':
        st = Student.objects.get(pk=id)
        fm = HrUpdateTimeForm(request.POST, instance=st)
        form=fm
        if fm.is_valid():
            from_time=request.POST['from_time']
            to_time=request.POST['to_time']
            time=datetime.now().time()
            date1=str(datetime.now().date())
            date_time_str = date1+" "+from_time
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            from_time1=date_time_obj.time()
            date2=date_time_obj.date()
            if from_time1<time:
                return render(request,'visit/VisitorDetail.html', {'student': st,'error':'please enter a valid time duration time is not before now'})
            
            elif from_time>to_time:
                return render(request,'visit/VisitorDetail.html', {'student': st,'form': form,'error':'please enter a valid time duration '})
            else:
                form.save()
            
            Student.objects.filter(pk=id).update(status="Accepted")
            recipent_email=(st.email,)
            subject="Meeting confirmed"
            messages=(f"you can check your remaning time to meeting is here--> http://127.0.0.1:8000/RemaningTimeToMeet/{st.id} and your id is {st.id}")
            email_from=settings.EMAIL_HOST_USER
            send_mail(subject, messages,email_from, recipent_email)
        return HttpResponseRedirect('/visitor/')

    st = Student.objects.get(pk=id)
    fm = HrUpdateTimeForm(instance=st)
    return render(request, 'visit/VisitorDetail.html', {'student': st, 'form': fm})

# @unauthenticated_user
def RemaningTimeToMeet(request,pk):
    pk=pk
    ob=Student.objects.get(id=pk)
    timeleft=ob.from_time
    timeleft1=ob.to_time
    date = ob.date
    datetime1 = datetime.combine(date, timeleft)
    datetime2 = datetime.combine(date, timeleft1)
    datetime3 = datetime.now()
    context={'ob':ob}
    if datetime1>datetime3:
        context['timeleft']=datetime1
        context["option"]="We're meet with you soon"
    elif datetime1<datetime3<datetime2:
        context["option"]="Your Meeting time has been Started it will be end in"
        context['timeleft']=datetime2
    else:
        context["option"]="your meeting is end"
    
    return render(request,'visit/RemaningTimeToMeet.html',context)

@login_required(login_url='/login/')
def ChangePasswordView(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)
    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"] = data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request, user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request, "visit/ChangePassword.html", context)


@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def AcceptApplicents(request,id):
        
        # return render(request,'visit/newApplicants.html',{"visitors":ap,"error":"User Created Succesfully"})
        id=id
        ap = Applicant.objects.get(pk=id)
        name_r = ap.username
        email_r = ap.email

        password_r = name_r.title()+'@123'
        recipent_email=(ap.email,)
        email_from=settings.EMAIL_HOST_USER
        try:
            user=User.objects.create_user(name_r, email_r, password_r,is_staff=True)
            Applicant.objects.filter(pk=id).update(status="Accepted")
            my_group  = Group.objects.get(name=ap.role) 
            # my_group.user_set.add(ap)
            user.groups.add(my_group)
            print(my_group)
            subject="Application Accepted"
            messages=(f"Your Applicatition Has Been Approved.Your Username is --> {name_r} and Password is --> {password_r}")
            send_mail(subject, messages,email_from, recipent_email)
            ap = Applicant.objects.all()
            page_number = request.GET.get('page')                
            context = pagination(ap, page_number)
            context['error']="User Created Succesfully"
            return render(request,'visit/newApplicants.html',context)
        except:
            ap = Applicant.objects.all()
            page_number = request.GET.get('page')                
            context = pagination(ap, page_number)
            context['error']="User with this detailsis allready exist"
            return render(request,'visit/newApplicants.html',context)
            # return render(request,'visit/newApplicants.html',{"visitors":ap,"error":"User with this detailsis allready exist"})
            

@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def ApplicantInfo(request,id):
    ap = Applicant.objects.get(id=id)
    return render(request,"visit/ApplicantsInfo.html",{"student":ap})

@login_required(login_url='/login/')
@permission_required('visit.is_hr')
def RejactApplicants(request,id):
    id=id
    print(id)
    Applicant.objects.filter(pk=id).update(status="Rejected")
    ap=Applicant.objects.get(pk=id)
    u=User.objects.filter()
    j=[]
    for i in u:
        j=str(i.username)
        if ap.username in j:
            u=User.objects.get(username=ap.username)
            u.delete()
    recipent_email=[ap.email,]
    subject="Meeting Rejected"
    messages=(f"Your Applicatition Has Been Rejected")
    email_from=settings.EMAIL_HOST_USER
    send_mail(subject, messages,email_from, recipent_email)
    ap = Applicant.objects.all()
        # visitors = Applicant.objects.all()
    print("visitors : ", visitors)
    page_number = request.GET.get('page')
    context = pagination(ap, page_number)
    context['error']="Applicant Rejected Succesfully"
    return render(request,'visit/newApplicants.html',context)


def ApplicantSignUp(request):
    #    if request.method == "POST" and "applicant_save_btn" in request.POST:
    #        applicant.objects.create(username=request.POST['uname'],firstname=request.POST['fname'],
    #        )
    return render(request, "visit/applicantSignup.html")
