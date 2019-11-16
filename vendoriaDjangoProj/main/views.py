from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homepage(request):
	return HttpResponse("This is some dope god damn <strong>TESTING</strong>.")
