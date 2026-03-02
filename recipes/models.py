from django.db import models
from django.contrib.auth.models import User


class Categorie(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Recette(models.Model):
    DIFFICULTE_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]
    titre = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    temps_preparation = models.IntegerField(help_text="Temps en minutes")
    image = models.ImageField(upload_to='recettes/', blank=True, null=True)
    ingredients = models.TextField()
    etapes = models.TextField()
    portions = models.IntegerField()
    difficulte = models.CharField(max_length=20, choices=DIFFICULTE_CHOICES)
    ustensiles = models.TextField(blank=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def moyenne_votes(self):
        votes = self.votes.all()
        if votes:
            return sum(v.valeur for v in votes) / len(votes)
        return 0


class Commentaire(models.Model):
    recette = models.ForeignKey(Recette, related_name='commentaires', on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.recette.titre}"


class Vote(models.Model):
    recette = models.ForeignKey(Recette, related_name='votes', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    valeur = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('recette', 'utilisateur')

    def __str__(self):
        return f"{self.utilisateur.username} a voted {self.valeur} pour {self.recette.titre}"
