from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .query import *
# Create your views here.


def main(request):
    #set_authors()
    #set_titles()
    #get_title_count()
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'main.html', context)

def book_list(request, pk):
    titles = Title.objects.filter(author_id=pk)
    authors = Author.objects.filter(author_id=pk)
    form = NewBookForm()
    form.fields['author_id'].initial = pk
    if request.method == 'POST':
        print(request.POST)
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            get_title_count()

    context = {'titles': titles, 'authors': authors, 'form': form}
    return render(request, 'book_list.html', context)
