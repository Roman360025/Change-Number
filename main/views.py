from django.shortcuts import render
from .forms import NumberForm
from .models import Number
import logging

logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse


def index(request):
    error = ''
    number = "Здесь будет обработанное число"
    if request.method == 'POST':
        form = NumberForm(request.POST) # Форма, полученная только что от пользователя
        form_base = Number.objects.get(id=1) # Данные, доступные в БД
        if form.is_valid() :
            if not form_base:
                form.save()
                context = {
                    'form': form,
                }

                return render(request, 'main/index.html', context)
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
