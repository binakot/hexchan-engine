from django.shortcuts import render


def start_page(request):
    return render(request, 'imageboard/start_page.html', {})
