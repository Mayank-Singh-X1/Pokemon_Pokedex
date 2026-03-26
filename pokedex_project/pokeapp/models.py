from django.db import models

class CaughtPokemon(models.Model):
    name=models.CharField(max_length=100, unique=True)
    sprite_url = models.URLField()
    type=models.CharField(max_length=50)

    def __str__(self):
        return self.name
