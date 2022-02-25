from multiprocessing import context
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
import datetime as dt
from .models import Article


# Create your views here.

def welcome(request):
  return render(request,'welcome.html')

def latest(request):
  return HttpResponse('Welcome to the latest Tribune')

def news_of_day(request):
  date=dt.date.today()
  # day=convert_dates(date)
  news=Article.todays_news()
  return render(request,'all-news/today-news.html',{'date':date,"news":news})


def convert_dates(dates):
  day_number=dt.date.weekday(dates)

  days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

  day=days[day_number]
  return day


def past_days_news(request,past_date):
  
  try:
    date=dt.datetime.strptime(past_date,'%Y-%m-%d').date()

  except ValueError:
    raise Http404()
    assert False
  # day=convert_dates(date)
  
  if date==dt.date.today():
    return redirect(news_of_day)
 
  # news=dt.date.today(date)
  news=Article.days_news(date)
  context={

    'date':date,
    'news':news,
  }
  # return render(request,'all-news/past-news.html',{'date':date,"news":news})
  return render(request,'all-news/past-news.html',context)


def search_results(request):

  if 'article' in request.GET and request.GET["article"]:
    search_term=request.GET.get("article")
    searched_articles=Article.search_by_title(search_term)

    message=f"{search_term}"

    context={
      "message":message,
      "articles":searched_articles
    }
    return render(request,'all-news/search.html',context)

  else:
    message="You haven't searched for any term"
    return render(request,'all-news/search.html',{"message":message})


def article(request,article_id):
  try:
    article=Article.objects.get(id=article_id)
  
  except DoesNotExist:
    raise Http404()

  return render(request,"all-news/article.html",{"article":article})