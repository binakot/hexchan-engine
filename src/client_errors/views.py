# Standard library imports
import logging

# Django imports
from django.http import JsonResponse

# App imports
from .forms import ClientErrorForm


# Get logger
logger = logging.getLogger('client_errors')


def client_error_handler(request):
    # Check request type
    if not request.POST:
        return JsonResponse({'status': 'error'}, status=500)

    # Get form data
    form = ClientErrorForm(request.POST)
    if not form.is_valid():
        print(request.POST)
        print(form.errors)
        return JsonResponse({'status': 'error'}, status=500)

    # Write log
    logger.error('URL: "{url}" -- Line: "{line}" -- Message: "{msg}"'.format(
        url=form.cleaned_data['url'],
        line=form.cleaned_data['line'],
        msg=form.cleaned_data['msg'],
    ))

    # Send ok response
    return JsonResponse({'status': 'ok'})
