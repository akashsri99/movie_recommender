from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import urllib.parse
import asyncio
from pyppeteer import launch

HOST="http://192.168.1.10:8080/"
def result_parser(results, total_pages, movie_id, request):
    movies= list()
    for result in results:
        if result["original_language"] == "en" or result["original_language"] == "in" or result["original_language"] == "hi":
            print(result)
            result["action"] = HOST+'movies/play/'+ urllib.parse.quote(result["title"])
            result["trailer"] = HOST+"movies/watch/"+str(result["id"])
            movies = movies + [result]
            

    for i in range(2, total_pages+1):
        URL = "https://api.themoviedb.org/3/movie/"+movie_id+"/similar?api_key=dd0ea450d1f8d5009ca368e376ddec80&language=en-US&page=" + str(i)
        r = requests.get(url=URL)
        data = r.json()
        print("----------------\n\n\n")
        print(data)
        results = data["results"]
        for result in results:
            if result["original_language"] == "en" or result["original_language"] == "in" or result["original_language"] == "hi":
                result["action"] = HOST+"?name="+ urllib.parse.quote(result["title"])
                result["trailer"] = HOST+"movies/watch/"+str(result["id"])
                movies = movies + [result]

    print(movies)
    template = loader.get_template('index.html')
    context = {
        'data': movies,
    }
    return HttpResponse(template.render(context, request))

def search(request, query):
    print(query)
    URL = "https://api.themoviedb.org/3/search/movie?api_key=dd0ea450d1f8d5009ca368e376ddec80&language=en-US&query=" + query + "&page=1&include_adult=false"
    print(URL)
    r = requests.get(url=URL)
    data = r.json()
    results = data["results"]
    return result_parser(results,0, 0, request)


def similar(request, movie_id):
    
    URL = "https://api.themoviedb.org/3/movie/"+movie_id+"/similar?api_key=dd0ea450d1f8d5009ca368e376ddec80&language=en-US&page=1"
    r = requests.get(url=URL)
    data = r.json()
    results = data["results"]
    total_pages = data["total_pages"]
    if total_pages > 10:
        total_pages = 10;
    return result_parser(results, total_pages,movie_id, request)

def watch(request, movie_id):
    print(movie_id)
    URL = "https://api.themoviedb.org/3/movie/"+movie_id+"/videos?api_key=dd0ea450d1f8d5009ca368e376ddec80&language=en-US"
    r = requests.get(url=URL)
    data = r.json()
    results = data["results"]
    print(results)
    for result in results:
        if result["site"] == "YouTube"  and result["type"] == "Trailer":
            key = result["key"]
            URL = "http://localhost:3001/trailer?video_id=" + key
            r = requests.get(url=URL)
            return HttpResponse(results)
    return HttpResponse(results)

def search_movie(request):
    print(request.POST)
    query = request.POST["movie"]
    print(query)
    return search(request, query)
    

def play(request, query):
    movie = query
    URL = "http://localhost:3001/?name=" + movie
    print(movie)
    r = requests.get(url=URL)
    return HttpResponse("Success")


    

    
