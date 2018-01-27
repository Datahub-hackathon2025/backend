from django.shortcuts import render, redirect

def index(request):
    return redirect('/static/frontend/index.html', permanent=True)