import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
    file = csv.DictReader(csvfile)
    STATIONS = [station for station in file]


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(STATIONS, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
