from django.shortcuts import render
from django.http import HttpResponse
from .models import Manufacturer
from .models import Shipper

# Create your views here.
def homepage(request):
	return HttpResponse("This is some dope god damn <strong>TESTING</strong>.")


def manufacturers(request):
	return render(request,
			'main/manufacturers.html',
			context={"manus": Manufacturer.objects.all}
			)
def shippers(request):
	return render(request,
				  'main/shippers.html',
				  context= {"ships" : Shipper.objects.all}
	)