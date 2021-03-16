import functools


def log_error(logger):
    """ Wraps a function in a try-except clause, if there was an
    exception it will log it and re-raise it
    :param logger: a logger object from the logging module"""
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.exception(e)
                raise
        return wrapped
    return decorated
