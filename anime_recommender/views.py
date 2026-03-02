from django.db.models import Q # Import Q
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Anime
from .api import MAL_Access, KNN

def anime_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Anime.objects.filter(
            Q(name__icontains=query) | Q(genre__icontains=query)
        )
    return render(request, 'index.html', {'results': results, 'query': query})

def detail(request, question_id):
    anime = get_object_or_404(Anime, pk=question_id)
    recommendations = recommend_anime(request, anime.anime_id)
    return render(request, "anime_details.html", {"anime": anime, "recommendations": recommendation})

def recommend_anime(request, anime_id):
    recommendations = KNN.recommendation_identification(anime_id)
    for x in recommendations["similar_anime_ids"]:
        print(x)