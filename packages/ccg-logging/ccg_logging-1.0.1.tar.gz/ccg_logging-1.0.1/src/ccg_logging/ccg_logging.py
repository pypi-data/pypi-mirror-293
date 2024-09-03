import sys
from pathlib import Path

from loguru import logger


FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}'


def setup(path: Path, format: str = FORMAT):
    """Sets up the logger to log in the format we want.
    
    This is done because technically every log entry is made from this file - and
    the default format records only that.

    We use our custom format here that removes that (and we add the actual 
    function to the message itself).
    """
    logger.remove()  # remove the default one

    logger.add(path, format=format)
    logger.add(sys.stderr, format=format)


def log_function_call(
    include_params: bool = False,
    include_output: bool = False,
    include_output_size: bool = False,
    severity: str = 'DEBUG'
):
    if include_output and include_output_size:
        raise ValueError('Only one of `include_output` and `include_output_size can be True!')

    def decorator(function: callable):

        def wrapper(*args, **kwargs):
            msg = f'{_get_function_call(function)}'

            if include_params:
                msg += _get_function_call_params(args, kwargs)

            logger.log(msg, severity=severity)

            output = function(*args, **kwargs)

            if include_output or include_output_size:
                if include_output:
                    msg += f' -> {output}'

                if include_output_size:
                    msg += f' -> {output.__class__.__name__} size {len(output)}'

                logger.log(f'\t{msg}', severity=severity)

            return output

        return wrapper

    return decorator    


def _get_function_call(function):
    return f'{function.__module__}:{function.__name__}'


def _get_function_call_params(args, kwargs):
    return f'({_get_args_kwargs_string(args, kwargs)})' 


def _get_args_kwargs_string(args, kwargs):
    return ', '.join(
        [arg.__repr__() for arg in args] 
        + [f'{k}={v.__repr__()}' for k, v in kwargs.items()]
    )
