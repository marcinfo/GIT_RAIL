
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile,TbCalendarioVacina,TbUbsDadosSp
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
import folium
import webbrowser
def index(request):

    return render(request, 'vacina/index.html')

def vacinas_prazos(request):

    nascimento = "21/01/2023"
    ##transfoma a dataa para o formato intenacional
    nova_data = parse(nascimento)
    vac=TbCalendarioVacina.objects.all().values()
    dados_sql=pd.DataFrame(vac)
    dados_sql.index_col = False
    # Contador para o for
    conta_mes = 0
    # lista vazia que vai receber os valores de (data + meses)
    listadata = []
    diasfalta = []
    # percorre todas as linhas da tabela
    for (row, rs) in dados_sql.iterrows():
        # recebe a quntidade de mes e coloca na quantidade_mes
        quantidade_mes = int(dados_sql['meses'].values[conta_mes])
        # adiciona a quaantidade de mêses na data
        #data_prevista = nova_data + relativedelta(months = quantidade_mes)
        data_prevista = pd.to_datetime(nova_data) + pd.DateOffset(months=quantidade_mes)
        # incrementa o contador
        conta_mes = conta_mes + 1
        listadata += [data_prevista]
        # diasfalta += [dias]
    # adiciona a lista ao dataframe
    dados_sql['dataprevista'] = listadata
    selecao = (dados_sql['dataprevista'] >= datetime.today())

    dados_sql.to_string(index=False)
    # transforma data para o formato brasileiro
    dados_sql['dataprevista'] = pd.to_datetime(dados_sql['dataprevista'])
    dados_sql['dataprevista'] = pd.to_datetime(dados_sql['dataprevista'])
    dados_sql['dataprevista'] = dados_sql['dataprevista'].dt.strftime('%d/%m/%Y')
    dados_sql2 = dados_sql.sort_values(by=['meses'], ascending=True)
    dados_sql3 = pd.DataFrame(dados_sql2)
    dados_sql3 = dados_sql3[['descricao_vacina','observacao','meses', 'dataprevista']]
    dados_sql3.rename(
        columns={'descricao_vacina': 'Vacina', 'observacao': 'Observções', 'meses': 'Meses',
                 'dataprevista': 'Data prevista'},
        inplace=True
    )
    dados_sql3.to_string(index=False)
    context = {
        'vacin':'Vacinas disponibilizadas pelo SUS',

        'dados_sql3':dados_sql3.to_html(classes='table table-stripped', border=1, justify='center',index=False)
    }
    return render(request, 'vacina/vacinas_prazos.html', context)

def encontra_ubs(request):
    ubs = TbUbsDadosSp.objects.all().values()
    geoloc_ubs = pd.DataFrame(ubs)
    #filtra o dataset com a variavel bairroubs
    geoloc=geoloc_ubs
    #seleciona a primeiralinha da pesquisa e utiliza a coordenada para centralizar o mapa
    #par ulilizar vinda do navegador  substitua geoloc.iloc[0]
    geo_centraliza = geoloc.iloc[978]
    print(geo_centraliza)
    #variaveis ppara a plotagem
    l1=geo_centraliza['latitude']
    l2=geo_centraliza['longitude']
    #mplotagem do mapa
    m = folium.Map(location=[l1,l2],zoom_start=14, popup='teste')
    folium.Marker(location=[float(l1), float(l2)]).add_to(m)
    m = m._repr_html_()
    context = {
        'vacin':'Encontre a UBS mais proxima de você.',

        'm':m
    }

    return render(request, 'vacina/encontra_ubs.html',context)

def minhas_vacinas(request):
    nascimento = request.user.profile.date_of_birth
    print(f'user: {request.user.profile.date_of_birth}')
    ##transfoma a dataa para o formato intenacional

    vac=TbCalendarioVacina.objects.all().values()
    dados_sql=pd.DataFrame(vac)
    dados_sql.index_col = False
    # Contador para o for
    conta_mes = 0
    # lista vazia que vai receber os valores de (data + meses)
    listadata = []
    diasfalta = []
    # percorre todas as linhas da tabela
    for (row, rs) in dados_sql.iterrows():
        # recebe a quntidade de mes e coloca na quantidade_mes
        quantidade_mes = int(dados_sql['meses'].values[conta_mes])
        # adiciona a quaantidade de mêses na data
        #data_prevista = nova_data + relativedelta(months = quantidade_mes)
        data_prevista = pd.to_datetime(nascimento) + pd.DateOffset(months=quantidade_mes)
        # incrementa o contador
        conta_mes = conta_mes + 1
        listadata += [data_prevista]
        # diasfalta += [dias]
    # adiciona a lista ao dataframe
    dados_sql['dataprevista'] = listadata
    dados_sql.to_string(index=False)
    # transforma data para o formato brasileiro
    dados_sql['dataprevista'] = pd.to_datetime(dados_sql['dataprevista'])
    dados_sql['dataprevista'] = dados_sql['dataprevista'].dt.strftime('%d/%m/%Y')
    dados_sql2 = dados_sql.sort_values(by=['meses'], ascending=True)
    dados_sql3 = pd.DataFrame(dados_sql2)
    dados_sql3 = dados_sql3[['descricao_vacina','observacao','meses', 'dataprevista','status_vacina']]
    dados_sql3.rename(
        columns={'descricao_vacina': 'Vacina', 'observacao': 'Observções', 'meses': 'Meses',
                 'dataprevista': 'Data Prevista','status_vacina':'Status Vacina'},
        inplace=True
    )
    dados_sql3.to_string(index=False)
    context = {
        'vacin':'Minhas Vacinas',
        'dados_sql3':dados_sql3.to_html(classes='table table-stripped', border=1, justify='center',index=False)
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
