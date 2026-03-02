from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Recette, Categorie, Commentaire, Vote


def liste_recettes(request):
    categories = Categorie.objects.all()
    categorie_id = request.GET.get('categorie')
    tri = request.GET.get('tri', '-created_at')
    
    if categorie_id:
        recettes = Recette.objects.filter(categorie_id=categorie_id)
    else:
        recettes = Recette.objects.all()
    
    if tri == 'note':
        recettes = sorted(recettes, key=lambda r: r.moyenne_votes(), reverse=True)
    elif tri == 'temps':
        recettes = recettes.order_by('temps_preparation')
    elif tri == '-temps':
        recettes = recettes.order_by('-temps_preparation')
    else:
        recettes = recettes.order_by('-created_at')
    
    return render(request, 'recipes/liste_recettes.html', {
        'recettes': recettes,
        'categories': categories,
        'categorie_selected': categorie_id,
        'tri': tri
    })


def detail_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    commentaires = recette.commentaires.all()
    
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(recette=recette, utilisateur=request.user)
        except Vote.DoesNotExist:
            pass
    
    return render(request, 'recipes/detail_recette.html', {
        'recette': recette,
        'commentaires': commentaires,
        'user_vote': user_vote
    })


def recherche(request):
    query = request.GET.get('q')
    categories = Categorie.objects.all()
    categorie_id = request.GET.get('categorie')
    tri = request.GET.get('tri', '-created_at')
    
    recettes = Recette.objects.all()
    
    if query:
        recettes = recettes.filter(Q(titre__icontains=query) | Q(ingredients__icontains=query))
    
    if categorie_id:
        recettes = recettes.filter(categorie_id=categorie_id)
    
    if tri == 'note':
        recettes = sorted(recettes, key=lambda r: r.moyenne_votes(), reverse=True)
    elif tri == 'temps':
        recettes = recettes.order_by('temps_preparation')
    elif tri == '-temps':
        recettes = recettes.order_by('-temps_preparation')
    else:
        recettes = recettes.order_by('-created_at')
    
    return render(request, 'recipes/recherche.html', {
        'recettes': recettes,
        'query': query,
        'categories': categories,
        'categorie_selected': categorie_id,
        'tri': tri
    })


@login_required
def ajouter_recette(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        categorie_id = request.POST.get('categorie')
        temps_preparation = request.POST.get('temps_preparation')
        ingredients = request.POST.get('ingredients')
        etapes = request.POST.get('etapes')
        portions = request.POST.get('portions')
        difficulte = request.POST.get('difficulte')
        ustensiles = request.POST.get('ustensiles')
        
        recette = Recette(
            titre=titre,
            categorie_id=categorie_id,
            temps_preparation=temps_preparation,
            ingredients=ingredients,
            etapes=etapes,
            portions=portions,
            difficulte=difficulte,
            ustensiles=ustensiles,
            auteur=request.user
        )
        
        if request.FILES.get('image'):
            recette.image = request.FILES.get('image')
        
        recette.save()
        messages.success(request, 'Recette ajoutée avec succès!')
        return redirect('detail_recette', pk=recette.pk)
    
    categories = Categorie.objects.all()
    return render(request, 'recipes/ajouter_recette.html', {'categories': categories})


@login_required
def modifier_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk, auteur=request.user)
    
    if request.method == 'POST':
        recette.titre = request.POST.get('titre')
        recette.categorie_id = request.POST.get('categorie')
        recette.temps_preparation = request.POST.get('temps_preparation')
        recette.ingredients = request.POST.get('ingredients')
        recette.etapes = request.POST.get('etapes')
        recette.portions = request.POST.get('portions')
        recette.difficulte = request.POST.get('difficulte')
        recette.ustensiles = request.POST.get('ustensiles')
        
        if request.FILES.get('image'):
            recette.image = request.FILES.get('image')
        
        recette.save()
        messages.success(request, 'Recette modifiée avec succès!')
        return redirect('detail_recette', pk=recette.pk)
    
    categories = Categorie.objects.all()
    return render(request, 'recipes/modifier_recette.html', {
        'recette': recette,
        'categories': categories
    })


@login_required
def supprimer_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk, auteur=request.user)
    
    if request.method == 'POST':
        recette.delete()
        messages.success(request, 'Recette supprimée!')
        return redirect('liste_recettes')
    
    return render(request, 'recipes/supprimer_recette.html', {'recette': recette})


@login_required
def ajouter_commentaire(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        Commentaire.objects.create(
            recette=recette,
            auteur=request.user,
            contenu=contenu
        )
        messages.success(request, 'Commentaire ajouté!')
    
    return redirect('detail_recette', pk=pk)


@login_required
def voter(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    
    if request.method == 'POST':
        valeur = int(request.POST.get('valeur'))
        vote, created = Vote.objects.update_or_create(
            recette=recette,
            utilisateur=request.user,
            defaults={'valeur': valeur}
        )
        messages.success(request, 'Vote enregistré!')
    
    return redirect('detail_recette', pk=pk)


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('liste_recettes')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie!')
                return redirect('liste_recettes')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/connexion.html', {'form': form})


def deconnexion(request):
    logout(request)
    messages.info(request, 'Déconnexion réussie!')
    return redirect('liste_recettes')
