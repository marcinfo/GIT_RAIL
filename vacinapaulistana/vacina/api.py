from ninja import  NinjaAPI
from .models import  TbCalendarioVacina
import json
apis = NinjaAPI()
@apis.get('prazos/')
def listar(request):
    prazos = TbCalendarioVacina.objects.all()
    response = [{'id_vacina': i.id_vacina, 'descricao_vacina': i.descricao_vacina} for i in prazos]
    print(response)

    return response

