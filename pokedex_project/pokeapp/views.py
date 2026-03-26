from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import CaughtPokemon

def fetch_pokemon(request, pokemon_name):
    pokemon_name=pokemon_name.lower()

    url=f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)

    # Typing "pikacho" (typo) will show error message instead of crashing
    if response.status_code == 404:
        return HttpResponse(f"Pokemon {pokemon_name} no found")

    data = response.json()

    name=data['name'].capitalize()
    sprite_url=data['sprites']['front_default']
    type_name= data['types'][0]['type']['name'].capitalize()

    if CaughtPokemon.objects.filter(name=name).exists():
        return HttpResponse(f"u have already searched {pokemon_name} !!")
    
    pokemon= CaughtPokemon(
        name=name,
        sprite_url=sprite_url,
        type=type_name
    )
    pokemon.save()

    return HttpResponse(f" {sprite_url} Caught")