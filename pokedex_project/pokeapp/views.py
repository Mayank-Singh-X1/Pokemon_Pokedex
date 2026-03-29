from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
import requests
from .models import CaughtPokemon

def search_pokemon(request):
    """
    Search page - shows search form and result
    """
    return render(request, 'pokeapp/search.html')

def gallery(request):
    return render(request, 'pokeapp/gallery.html')
def party(request):
    return render(request, 'pokeapp/party.html')

def fetch_pokemon(request, pokemon_name):
    """
    Fetches Pokémon from API and displays it (doesn't save yet)
    """
    pokemon_name = pokemon_name.lower()
    
    # Call API
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    
    # Check if Pokémon exists
    if response.status_code == 404:
        return render(request, 'pokeapp/search.html', {
            'error': f'Pokémon "{pokemon_name}" not found!',
            'searched': True
        })
    
    # Parse data
    data = response.json()
    
    pokemon_data = {
        'id': data['id'],
        'name': data['name'].capitalize(),
        'sprite_url': data['sprites']['front_default'],
        'type': data['types'][0]['type']['name'].capitalize(),
        'height': data['height'],
        'weight': data['weight'],
        'hp': data['stats'][0]['base_stat'],
        'attack': data['stats'][1]['base_stat'],
        'defense': data['stats'][2]['base_stat'],
    }
    
    # Check if already caught
    already_caught = CaughtPokemon.objects.filter(name=pokemon_data['name']).exists()
    
    return render(request, 'pokeapp/search.html', {
        'pokemon': pokemon_data,
        'already_caught': already_caught,
        'searched': True
    })


def catch_pokemon(request, pokemon_name):
    """
    Actually saves the Pokémon to database
    """
    pokemon_name = pokemon_name.lower()
    
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    
    if response.status_code == 404:
        return redirect('search_pokemon')
    
    data = response.json()
    
    name = data['name'].capitalize()
    sprite_url = data['sprites']['front_default']
    type_name = data['types'][0]['type']['name'].capitalize()
    
    # Save to database
    try:
        CaughtPokemon.objects.create(
            name=name,
            sprite_url=sprite_url,
            type=type_name
        )
        message = f'✅ Successfully caught {name}!'
        message_type = 'success'
    except IntegrityError:
        message = f'⚠️ You already caught {name}!'
        message_type = 'warning'
    
    # Redirect back to search with the Pokémon displayed
    return redirect(f'/pokemon/search/{pokemon_name}/')