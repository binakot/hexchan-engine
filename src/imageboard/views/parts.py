from typing import Callable, Union, List, Tuple


def get_session_list(request, session_key: str, limit=16) -> List[int]:
    return request.session.get(session_key, [])[-limit:]


def push_to_session_list(request, session_key: str, value: int, limit=16) -> None:
    session_list = request.session.get(session_key, [])[-(limit-1):]
    session_list.append(value)
    request.session[session_key] = session_list


def set_session_data_as_cookie(request, response, session_key: str):
    session_list = get_session_list(request, session_key)
    data_string = '#'.join([str(x) for x in session_list])
    response.set_cookie(session_key, data_string)
