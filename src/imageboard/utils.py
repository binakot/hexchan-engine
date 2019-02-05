import math


def get_client_ip(request) -> str:
    """Get real client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_pretty_file_size(size_in_bytes: int) -> str:
    exponent = math.floor(math.log(size_in_bytes, 1024))
    unit = {
        0: 'B',
        1: 'KB',
        2: 'MB',
        3: 'GB',
    }[exponent]
    size = size_in_bytes / (1024 ** exponent)
    return '{size} {unit}'.format(size=size, unit=unit)
