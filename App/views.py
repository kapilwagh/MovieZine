from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import http.client, json, requests
from .forms import AccountAuthenticationForm, RegistrationForm
from .models import Account, Movie
import time
import pickle
import pandas as pd


# Create your views here.

my_api_key = '9e8c5a314d6ac88caafdf94f375f64c3'
base_url = 'https://api.themoviedb.org/3/'

def home(request):
    if request.method == "POST":
        if 'trailer' in request.POST:
            movie_id = request.POST.get("name")
            trailer_url = f'{base_url}movie/{movie_id}/videos?api_key={my_api_key}&language=en-US'
            trailer_response = requests.get(trailer_url)
            trailer = trailer_response.json()['results'][0]['key']
            return JsonResponse({"trailer": trailer})
    trend = f'{base_url}trending/all/day?api_key={my_api_key}'
    response = requests.get(trend)
    l = response.json()['results']
    for i in l:
        id = i['id']
        movie_cast_url = f'{base_url}/movie/{id}/credits?api_key={my_api_key}&language=en-US'
        response = requests.get(movie_cast_url)
        if response.status_code==200 and i['media_type']=='movie':
            movie_cast = response.json()['cast']
            count = 0
            actors = []
            for j in movie_cast:
                if count==4:
                    break
                actors.append(j['name'])
                count = count+1
            i['cast']=actors
        movie_cast_url = f'{base_url}tv/{id}/season/1/credits?api_key={my_api_key}&language=en-US'
        response = requests.get(movie_cast_url)
        if response.status_code==200 and i['media_type']=='tv':
            movie_cast = response.json()['cast']
            count = 0
            actors = []
            for j in movie_cast:
                if count==4:
                    break
                actors.append(j['original_name'])
                count = count+1
            i['cast']=actors
    return render(request, 'home.html', {'trending_movies': l})


def search_results(request):
    def recommend(movie):
        index = movies[movies['title'] == movie]
        if len(index) is 0:
            return "None","None","None"
        index = index.index[0]
        print(index)
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        recommended_movies_poster = []
        recommended_movies_trailer = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            movie_poster = fetch_poster(movie_id)
            movie_trailer = fetch_trailer(movie_id)
            recommended_movies_poster.append(movie_poster)
            recommended_movies_trailer.append(movie_trailer)
        return recommended_movies, recommended_movies_poster, recommended_movies_trailer
    def fetch_poster(movie_id):
        print(movie_id)
        url = "https://api.themoviedb.org/3/movie/{}?api_key=9e8c5a314d6ac88caafdf94f375f64c3&language=en-US".format(
            movie_id)

        data = requests.get(url)
        data = data.json()

        full_path = "https://image.tmdb.org/t/p/w500/" + (data["poster_path"])
        return full_path
    def fetch_trailer(movie_id):
        video_url = "http://api.themoviedb.org/3/movie/{}?api_key=9e8c5a314d6ac88caafdf94f375f64c3&append_to_response=videos&language=en-US".format(
            movie_id)

        data = requests.get(video_url)
        data = data.json()
        temp = data["videos"]
        tempp = temp["results"]
        temppp = tempp[0]
        video_key = temppp["key"]

        video_path = "https://www.youtube.com/watch?v=" + (video_key)
        return video_path

    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    start = time.time()
    user = request.user
    if request.method == "POST": # AJAX POST Request to Add Fav Movie to DB
        if 'ajax' in request.POST:
            movie_id = request.POST.get("name")
            m = Movie.objects.filter(movie_id=movie_id)
            # checks if movie already present in the DB
            if m:
                m[0].user.add(user)
            # adds it to the DB if movie not present in DB
            else:
                movie = Movie(movie_id=movie_id)
                movie.save()
                movie.user.add(user)
            return JsonResponse({"msg":movie_id, })
        if 'remove' in request.POST:
            movie_id = request.POST.get("name")
            m = Movie.objects.filter(movie_id=movie_id)
            m[0].user.remove(user)
            return JsonResponse({"msg":movie_id, })
        if 'cast' in request.POST:
            movie_id = request.POST.get("name")
            movie_cast_url = f'{base_url}/movie/{movie_id}/credits?api_key={my_api_key}&page=1'
            trailer_url = f'{base_url}movie/{movie_id}/videos?api_key={my_api_key}&language=en-US'
            response = requests.get(movie_cast_url)
            trailer_response = requests.get(trailer_url)
            movie_cast_api = response.json()['cast']
            trailer = trailer_response.json()['results'][0]['key']
            movie_cast = []
            count = 0
            while count<len(movie_cast_api)-1:
                d = {}
                d['name'] = movie_cast_api[count]['name']
                d['pic'] = movie_cast_api[count]['profile_path']
                movie_cast.append(d)
                count = count + 1
                if count>15:
                    return JsonResponse({"cast":movie_cast, "trailer": trailer})
            return JsonResponse({"cast":movie_cast, "trailer": trailer})
    fav_mov_list = Movie.objects.all()
    search = request.GET.get('search')
    url = f'{base_url}search/movie/?api_key={my_api_key}&language=en-US&query={search}&page=1'
    response = requests.get(url)
    l = response.json()['results']
    first_movie = None
    movie_name = ""
    names = "None"
    posters = ""
    trailer = ""
    while names is "None":
        for i in range(20):
            first_movie = l[i]
            movie_name = first_movie["title"]
            names,posters,trailer = recommend(movie_name)
            if names != "None":
                break
        if names != None:
            break
    for i in posters:
        print(i)
    for i in names:
        print(i)
    for i in trailer:
        print(i)
    movies = []
    for i in l:
        if (i['poster_path']):
            movies.append(i)
    datafronend = []
    for i in range(4):
        datafronend.append((names[i], posters[i],trailer[i]))
    return render(request, 'movies.html', {'results': movies, 'fav_mov_list': fav_mov_list, 'names':names, 'posters': posters, 'data':datafronend})

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()
        context['login_form'] = form

    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect('/')

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("home")
        else:
            context['registration_form'] = form
            return render(request, 'register.html', context)

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

def my_movies(request):
    m = Movie.objects.filter(user=request.user)
    fav_mov_list = []
    if request.method == "POST":
        if 'remove' in request.POST:
            movie_id = request.POST.get("name")
            m = Movie.objects.filter(movie_id=movie_id)
            m[0].user.remove(request.user)
            return JsonResponse({"msg":movie_id, })
    for i in m:
        url = f'{base_url}movie/{i.movie_id}?api_key={my_api_key}&language=en-US'
        response = requests.get(url)
        l = response.json()
        movie_cast_url = f'{base_url}/movie/{i.movie_id}/credits?api_key={my_api_key}&language=en-US'
        response = requests.get(movie_cast_url)
        movie_cast = response.json()['cast']
        count = 0
        actors = []
        for j in movie_cast:
            if count==10:
                break
            actors.append(j['profile_path'])
            actors.append(j['name'])
            count = count+1
        l['cast']=actors
        fav_mov_list.append(l)
    return render(request, 'fav_mov_list.html', {'fav_mov_list': fav_mov_list})
