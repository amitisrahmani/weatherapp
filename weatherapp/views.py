from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import City
import requests

API_KEY = "879ec736e83ca660f3e2392e1c299dbe"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

def get_weather_data(city_name):
    """Fetch weather data for a given city."""
    response = requests.get(BASE_URL.format(city_name, API_KEY))
    if response.status_code == 200:
        return response.json()
    return None

def home(request):
    # Fetching weather data for cities in the database
    cities = City.objects.all()
    user_weather = []

    for city in cities:
        data = get_weather_data(city.name)
        if data:
            user_weather.append({
                "city": city.name,
                "temperature": data.get("main", {}).get("temp", "N/A"),
                "description": data.get("weather", [{}])[0].get("description", "No data"),
                "icon": data.get("weather", [{}])[0].get("icon", "")
            })

    # Fetching Guildford weather
    guildford_weather_data = get_weather_data("Guildford")
    if guildford_weather_data:
        guildford_weather = {
            "temperature": guildford_weather_data.get("main", {}).get("temp", "N/A"),
            "description": guildford_weather_data.get("weather", [{}])[0].get("description", "No data"),
        }
    else:
        guildford_weather = {"temperature": "N/A", "description": "No data"}

    context = {
        "guildford_weather": guildford_weather,
        "user_weather": user_weather,
    }

    return render(request, "weather/home.html", context)

def add_city(request):
    if request.method == "POST":
        city_name = request.POST.get("city_name").strip()
        
        if City.objects.filter(name__iexact=city_name).exists():
            messages.warning(request, f"{city_name} is already in the list!")
        else:
            response = requests.get(BASE_URL.format(city_name, API_KEY))
            if response.status_code == 200:
                City.objects.create(name=city_name)
                messages.success(request, f"{city_name} added successfully!")
            else:
                messages.error(request, "Invalid city name. Please try again.")
    
    return redirect("home")

def delete_city(request, city_name):
    if request.method == "DELETE":
        city = get_object_or_404(City, name=city_name)
        city.delete()
        return JsonResponse({"success": True, "message": f"{city_name} has been removed."})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)