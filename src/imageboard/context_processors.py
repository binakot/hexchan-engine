import hexchan.config


def config(request):
    return {'config': hexchan.config.__dict__}
