from django.shortcuts import render, redirect
from .models import Movie


def movie_list(request):
    query = request.GET.get('search')
    genre = request.GET.get('genre')
    sort = request.GET.get('sort')
    status = request.GET.get('status')

    movies = Movie.objects.all()

    if query:
        movies = movies.filter(title__icontains=query)

    if genre:
        movies = movies.filter(genre=genre)

    if status == 'watched':
        movies = movies.filter(watched=True)

    elif status == 'unwatched':
        movies = movies.filter(watched=False)    

    if sort == 'rating':
        movies = movies.order_by('-rating')

    elif sort == 'newest':
        movies = movies.order_by('-year')

    elif sort == 'oldest':
        movies = movies.order_by('year')

    elif sort == 'title':
        movies = movies.order_by('title')    

    genres = Movie.objects.values_list('genre', flat=True).distinct()

    return render(
        request,
        'movies/movie_list.html',
        {
            'movies': movies,
            'query': query,
            'genre': genre,
            'genres': genres,
            'sort': sort,

        }
    )

def movie_detail(request, id):
    movie = Movie.objects.get(id=id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def add_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        genre = request.POST['genre']
        year = request.POST['year']
        rating = request.POST['rating']
        description = request.POST['description']

        watched = 'watched' in request.POST

        Movie.objects.create(
            title=title,
            genre=genre,
            year=year,
            rating=rating,
            description=description,
            watched=watched
        )

        return redirect('movie_list')

    return render(request, 'movies/add_movie.html')

def edit_movie(request, id):
    movie = Movie.objects.get(id=id)

    if request.method == 'POST':
        movie.title = request.POST['title']
        movie.genre = request.POST['genre']
        movie.year = request.POST['year']
        movie.rating = request.POST['rating']
        movie.description = request.POST['description']
        movie.watched = 'watched' in request.POST

        movie.save()

        return redirect('movie_detail', id=movie.id)

    return render(request, 'movies/edit_movie.html', {'movie': movie})

def delete_movie(request, id):
    movie = Movie.objects.get(id=id)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movies/delete_movie.html', {'movie': movie})