from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Movie

@login_required
def movie_list(request):
    query = request.GET.get('search')
    genre = request.GET.get('genre')
    sort = request.GET.get('sort')
    status = request.GET.get('status')
    min_rating = request.GET.get('min_rating')
    min_year = request.GET.get('min_year')
    

    movies = Movie.objects.filter(user=request.user)

    total_movies = movies.count()
    favorite_movies = movies.filter(favorite=True).count()
    watched_movies = movies.filter(watched=True).count()
    unwatched_movies = movies.filter(watched=False).count()
    average_rating = movies.aggregate(Avg('rating'))['rating__avg']

    if query:
        movies = movies.filter(title__icontains=query)

    if genre:
        movies = movies.filter(genre=genre)

    if status == 'watched':
        movies = movies.filter(watched=True)

    elif status == 'unwatched':
        movies = movies.filter(watched=False)

    elif status == 'favorite':
        movies = movies.filter(favorite=True)

    if min_rating:
        movies = movies.filter(rating__gte=min_rating)    

    if min_year:
        movies = movies.filter(year__gte=min_year)    

    if sort == 'rating':
        movies = movies.order_by('-rating')

    elif sort == 'newest':
        movies = movies.order_by('-year')

    elif sort == 'oldest':
        movies = movies.order_by('year')

    elif sort == 'title':
        movies = movies.order_by('title')    

    genres = movies.values_list('genre', flat=True).distinct()

# Pagination
    paginator = Paginator(movies, 5)   # 5 movies per page
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    return render(
        request,
        'movies/movie_list.html',
        {
            'movies': movies,
            'query': query,
            'genre': genre,
            'genres': genres,
            'sort': sort,
            'status': status,
            'total_movies': total_movies,
            'favorite_movies': favorite_movies,
            'watched_movies': watched_movies,
            'unwatched_movies': unwatched_movies,
            'average_rating': average_rating,
            'min_rating': min_rating,
            'min_year': min_year,
        }
    )

@login_required
def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id, user=request.user)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


@login_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        genre = request.POST['genre']
        year = request.POST['year']
        rating = request.POST['rating']
        description = request.POST['description']

        watched = 'watched' in request.POST

        favorite = 'favorite' in request.POST

        poster = request.FILES.get('poster')

        Movie.objects.create(
            user=request.user,
            title=title,
            genre=genre,
            year=year,
            rating=rating,
            description=description,
            watched=watched,
            favorite=favorite,
            poster=poster
        )

        return redirect('movie_list')

    return render(request, 'movies/add_movie.html')

@login_required
def edit_movie(request, id):
    movie = Movie.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        movie.title = request.POST['title']
        movie.genre = request.POST['genre']
        movie.year = request.POST['year']
        movie.rating = request.POST['rating']
        movie.description = request.POST['description']
        movie.watched = 'watched' in request.POST
        movie.favorite = 'favorite' in request.POST

        poster = request.FILES.get('poster')

        if poster:
            movie.poster = poster

        movie.save()

        return redirect('movie_detail', id=movie.id)

    return render(request, 'movies/edit_movie.html', {'movie': movie})

@login_required
def delete_movie(request, id):
    movie = Movie.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movies/delete_movie.html', {'movie': movie})

def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('movie_list')

    return render(request, 'movies/register.html')


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('movie_list')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'movies/login.html')


def user_logout(request):
    logout(request)
    return redirect('/movies/login/')


