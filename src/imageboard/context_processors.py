import gensokyo.config


def config(request):
    return {'config': gensokyo.config.__dict__}
