import flask
import functools

class Blueprint(flask.Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def route(self, rule, **kwargs):
        original = super().route(rule, **kwargs)
        def route_wrapper(route):
            @functools.wraps(route)
            def wrapped_route(*args, **kwargs):
                try:
                    result = route(*args, **kwargs)
                    if isinstance(result, tuple):
                        return flask.jsonify(result[0]), result[1]
                    else:
                        return flask.jsonify(result)
                except RequestException as e:
                    return flask.jsonify({"message": e.message}), e.status
            original(wrapped_route)
            return route
        return route_wrapper

class RequestException(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status
