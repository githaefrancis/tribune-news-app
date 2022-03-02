from multiprocessing import context
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
import datetime as dt

from news.email import send_welcome_email
from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def welcome(request):
  return render(request,'welcome.html')

def latest(request):
  return HttpResponse('Welcome to the latest Tribune')

def news_of_day(request):
  date=dt.date.today()
  # day=convert_dates(date)
  news=Article.todays_news()
  
  if request.method=='POST':
    form=NewsLetterForm(request.POST)
    if form.is_valid():
      name=form.cleaned_data['your_name']
      email=form.cleaned_data['email']
      recipient=NewsLetterRecipients(name=name,email=email)
      recipient.save()

      send_welcome_email(name,email)

      HttpResponseRedirect('news_today')

  else:
    form=NewsLetterForm()
  
  return render(request,'all-news/today-news.html',{'date':date,"news":news,"letterForm":form})


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


@login_required(login_url='/accounts/login/')
def article(request,article_id):
  try:
    article=Article.objects.get(id=article_id)
  
  except ObjectDoesNotExist:
    raise Http404()

  return render(request,"all-news/article.html",{"article":article})