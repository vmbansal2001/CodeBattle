from django.shortcuts import render

# Create your views here.
def index(request): 
    return render(request, 'index.html')

def sign_in(request): 
    return render(request, 'register.html')