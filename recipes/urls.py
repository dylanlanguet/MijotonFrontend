from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_recettes, name='liste_recettes'),
    path('recette/<int:pk>/', views.detail_recette, name='detail_recette'),
    path('recherche/', views.recherche, name='recherche'),
    path('ajouter/', views.ajouter_recette, name='ajouter_recette'),
    path('modifier/<int:pk>/', views.modifier_recette, name='modifier_recette'),
    path('supprimer/<int:pk>/', views.supprimer_recette, name='supprimer_recette'),
    path('recette/<int:pk>/commentaire/', views.ajouter_commentaire, name='ajouter_commentaire'),
    path('recette/<int:pk>/vote/', views.voter, name='voter'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
