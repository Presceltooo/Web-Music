from django.db.models import Q 
from music.models import Music

def Search(request):
    '''Search function view'''
    search_query = ''

    if request.GET.get('query'):
        search_query = request.GET.get('query')
    
    only_published_music = Music.objects.filter(published=True)

    music = only_published_music.distinct().filter(
        Q(title__icontains=search_query)
    )

    return music