import psycopg2
from django.shortcuts import render
from .forms import NumberForm
import logging
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Number
from .serializers import NumberChangeSerializer
from .serializers import NumberListSerializer

logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse


def index(request):
    error = ''
    number = "Здесь будет обработанное число"
    if request.method == 'POST':
        form = NumberForm(request.POST)  # Форма, полученная только что от пользователя
        form_base = Number.objects.all()  # Данные, доступные в БД
        if form.is_valid():
            if not form_base:
                form.save()
                number = form.cleaned_data.get("number")
                form = NumberForm()
                context = {
                    'form': form,
                    'number': number + 1
                }

                return render(request, 'main/index.html', context)
            form_base = Number.objects.all()[0]
            number = form_base.number
            if number == form.cleaned_data.get("number"):
                error = 'ОШИБКА! Такое число уже вводилось'
                number = "Ошибка"
                logger.error('ОШИБКА! Такое число уже вводилось')
            elif (form.cleaned_data.get("number") - number) == -1:
                error = 'ОШИБКА! Поступившее число на единицу меньше обработанного числа'
                number = "Ошибка"
                logger.error('ОШИБКА! Поступившее число на единицу меньше обработанного числа')
            else:
                form_base.number = form.cleaned_data.get("number")
                form_base.save()
                number = form.cleaned_data.get("number") + 1

    form = NumberForm()
    context = {
        'form': form,
        'error': error,
        'number': number
    }
    return render(request, 'main/index.html', context)

class NumberView(APIView):
    '''Вывод числа'''

    def get(self, request):
        numbers = Number.objects.all()
        serializer = NumberListSerializer(numbers, many=True)
        return Response(serializer.data)


class NumberChange(APIView):
    '''Изменение числа'''

    def post(self, request):
        number_api = NumberChangeSerializer(data=request.data)
        print(number_api)
        if number_api.is_valid():
            if type(request.data["number"]) != int or request.data["number"] < 0:
                return Response({"error": "Ожадилось неотрицательное целое число"})
            form_base = Number.objects.all()  # Данные, доступные в БД
            if not form_base:
                number_api.save()
                return Response({"number": request.data["number"] + 1})
            form_base = Number.objects.all()[0]
            number = form_base.number
            if number == request.data["number"]:
                logger.error('ОШИБКА! Такое число уже вводилось')
                return Response({"error": 'ОШИБКА! Такое число уже вводилось'})
            elif (request.data["number"] - number) == -1:
                error = 'ОШИБКА! Поступившее число на единицу меньше обработанного числа'
                number = "Ошибка"
                logger.error('ОШИБКА! Поступившее число на единицу меньше обработанного числа')
                return Response({"error": 'ОШИБКА! Поступившее число на единицу меньше обработанного числа'})
            else:
                form_base.number = request.data["number"]
                form_base.save()
                return Response({"number": request.data["number"] + 1})
        else:
            return Response({'error': "Нет числа"})
