from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def about(request):
    return render(request,'about.html')


def contact(request): 
    return render(request,'contact.html')


def faq(request): 
    return render(request,'faq.html')
