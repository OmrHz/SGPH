
from django.db import models

class Medicament(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    max_duree = models.IntegerField(default=0)  # Default 0 for indefinite
    max_dose = models.FloatField()
    in_stock = models.BooleanField(default=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom
