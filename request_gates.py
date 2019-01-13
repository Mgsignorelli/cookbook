from werkzeug.exceptions import MethodNotAllowed, NotFound
from werkzeug.routing import RequestRedirect

from permissions import can


def get_route_from_request(app, host, url, method):
    adapter = app.url_map.bind(host)

    try:
        match = adapter.match(url, method=method)
    except RequestRedirect as e:
        # recursively match redirects
        return get_route_from_request(app=app, host=host, url=e.new_url, method=method)
    except(MethodNotAllowed, NotFound):
        # no match
        return None

    try:
        # return the view function and arguments
        return app.view_functions[match[0]], match[1]
    except KeyError:
        # no view is associated with the endpoint
        return None


def controller_exists_gate(app, request):
    return get_route_from_request(app=app, host=request.host, url=request.path, method=request.method)


def permission_gate(app, request):
    view = get_route_from_request(app=app, host=request.host, url=request.path, method=request.method)
    controller = view[0].__name__
    properties = view[1]

    return can(permission=controller)
