from django.shortcuts import render, redirect
from django.http import Http404
from hypernews import settings
from itertools import groupby
import json
import random
import datetime


# Create your views here.
def get_news(request, id):
    with open(settings.NEWS_JSON_PATH) as json_file:
        all_news = json.load(json_file)
        news = list(filter(lambda news: news["link"] == id, all_news))
        if len(news) > 0:
            return render(request, 'news/news.html', context={'news': news[0]})
        else:
            raise Http404("link doesn't exist")


def index(request, *args, **kwargs):
    with open(settings.NEWS_JSON_PATH) as json_file:
        all_news = json.load(json_file)
        q = request.GET.get('q')
        if q:
            all_news = filter(lambda item: q in item['title'], all_news)
        news_grouped = {k: list(v) for k, v in groupby(sorted(all_news, key= lambda item: item["created"], reverse=True), key=lambda item: item["created"][:10])}
        return render(request, 'news/index.html', context={'all_news': news_grouped})


def create_news(request):
    if request.method == 'GET':
        return render(request, 'news/new.html')
    elif request.method == 'POST':
        news = dict()
        news['title'] = request.POST.get('title')
        news['text'] = request.POST.get('text')
        news['link'] = random.randint(4, 100000)
        news['created'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(settings.NEWS_JSON_PATH) as json_file:
            all_news = json.load(json_file)
            with open(settings.NEWS_JSON_PATH, 'w') as json_file_w:
                json.dump(all_news + [news], json_file_w)
            return redirect("/news")
