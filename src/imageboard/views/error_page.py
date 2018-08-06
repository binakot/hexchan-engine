from django.shortcuts import render


def error_page(request):
    return render(request, 'imageboard/error_page.html', {})
