from django.http import HttpResponse


def error_page(request):
    return HttpResponse('error_page')
