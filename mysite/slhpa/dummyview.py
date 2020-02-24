from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hullo Wurld. Your database may not be loaded.")
