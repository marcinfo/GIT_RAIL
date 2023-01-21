import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile,TbCalendarioVacina
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse

def index(request):

    return render(request, 'vacina/index.html')

def vacinas_prazos(request):
    data_nascimento = date.today()
    ##transfoma a dataa para o formato intenacional
    nova_data = parse(data_nascimento)

    vac=TbCalendarioVacina.objects.raw(f'SELECT  *,date_add({nova_data}, interval meses month) as previsao\
                                        FROM vacina_paulistana.tb_calendario_vacina;')
    context = {
        'vacin':'Vacinas disponibilizadas pelo SUS',
        'vac':vac
    }
    return render(request, 'vacina/vacinas_prazos.html', context)

def encontra_ubs(request):

    return render(request, 'vacina/encontra_ubs.html')

def minhas_vacinas(request):
    vac = TbCalendarioVacina.objects.all().order_by('meses','id_vacina')

    context = {
        'vacin':'Minha agenda',
        'vac':vac
    }
    return render(request, 'vacina/minhas_vacinas.html',context)

def links(request):

    return render(request, 'vacina/links.html')

def api(request):

    return render(request, 'vacina/api.html')
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'vacina/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'vacina/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'vacina/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'vacina/dashboard.html', {'section': 'dashboard'})




@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Atualizado com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'vacina/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
