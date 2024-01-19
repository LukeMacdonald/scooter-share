SCOOTER_METHODS = ["LOCATION", "UNLOCK", "LOCK"]
scooter_functions = {}


def scooter_method_decorator(method, functions_dict):
    def decorator(key, param_types={}):
        def wrapper(func):
            def inner_wrapper(*args, **kwargs):
                # Check parameter types
                for param, param_type in param_types.items():
                    if param in kwargs and not isinstance(kwargs[param], param_type):
                        raise TypeError(
                            f"Invalid type for parameter '{param}'. Expected {param_type.__name__}, got {type(kwargs[param]).__name__}")

                # Execute the wrapped function
                result = func(*args, **kwargs)

                # Return the result of the wrapped function
                return result

            functions_dict[key] = inner_wrapper
            return inner_wrapper

        return wrapper

    return decorator


def location(key, param_types={}):
    return scooter_method_decorator("LOCATION", scooter_functions )(key, param_types)
