from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sample_app.models import Topic, AccessRecord, Webpage, WebUser
from . import forms
from django.urls import reverse #new from Django 2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

#Just by calling a method here can trigger the navigation to that page
#However, the url in the browser isn't changed. Perhaps fix that with JavaScript?
def index(request):

    webpages_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records' : webpages_list}

    return render(request, 'sample_app/index.html', context=date_dict)

@login_required
def help(request):
    my_dict = {'help_info' : 'This is some help info.'}
    return render(request, 'sample_app/help.html', context = my_dict)

@login_required
def user(request):
    user_list = WebUser.objects.order_by('last_name')
    user_dict = {'user_records' : user_list}

    return render(request, 'sample_app/users.html', context=user_dict)

@login_required
def relative_url_templates(request):
    return render(request, 'sample_app/relative_url_templates.html')

# def base_template(request):
#     return render(request, 'sample_app/base.html')

@login_required
def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("VALIDATION SUCCESS")
            print("NAME: " + form.cleaned_data['name'])
            print("EMAIL: " + form.cleaned_data['email'])
            print("TEXT: " + form.cleaned_data['text'])
        else:
            print("FORM VALIDATION FAILED")

    return render(request, "sample_app/form_page.html", {'form': form})

@login_required
def form_user_enter(request):
    form = forms.FormWebUser()

    if request.method == 'POST':
        form = forms.FormWebUser(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request) #go back to the home page
        else:
            print("FORM VALIDATION FAILED")

    return render(request, "sample_app/userform_page.html", {'form': form})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = forms.FormUser(data=request.POST)
        profile_form = forms.FormUserProfileInfo(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            #NOTE: ModelForm.save() and Model.save() BOTH update the databases
            #Having both gives the flexibility below.
            #When the ModeForm is saved, we'll get the Model object.
            #You can then update the Model object further and then save again.
            #IF the object will be in a bad state without that extra
            #update, then we'll need to save the ModelForm with commit = False.
            #Then save the Model object after all the necessary updates
            #have been done.

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #Set up the one-to-one relationship
            #Don't commit yet until it is done
            profile = profile_form.save(commit=False)
            profile.user = user

            #Note: profile_pic refers to the member of UserProfileInfo
            #, it's not referring to the media location
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True


        else:

            print(user_form.errors, profile_form.errors)
    else:
        user_form = forms.FormUser()
        profile_form = forms.FormUserProfileInfo()

    return render(request, 'sample_app/registration.html',
                            {'rego_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered
                            })

#using login_required decorator to make sure the user is logged in first.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active: #it's possible to deactive inactive users
                login(request, user)
                #'reverse look-up' the 'index', which is the name for the
                #corresponding URL and then redirect the user there
                #This is similar to {% url 'app_name:view_name'%}
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to log in and failed!")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, "sample_app/login.html", {})
