import sys
import warnings
from pathlib import Path
from typing import Any

import pandas as pd
from loguru import logger


FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}'


def setup(path: Path = None, format: str = FORMAT):
    """Sets up the logger to log in the format we want.
    
    This is done because technically every log entry is made from this file - and
    the default format records only that.

    We use our custom format here that removes that (and we add the actual 
    function to the message itself).
    """
    logger.remove()  # remove the default one

    if path is not None:
        logger.add(path, format=format)

    logger.add(sys.stderr, format=format)


def log_function_call(
    include_params: bool | list[str] = False,
    include_output: bool = False,
    include_output_size: bool = False,  # DEPRECATED v1.3.1, REMOVE v1.4
    level: str = 'DEBUG'
):
    """Logs a function call.

    Args:
        include_params (bool, default is False)
            Should the values of the parameters passed to the function be logged?

            (bool -> False)
                The default - the parameter values won't be included in the log.
                
            (bool -> True)
                All parameter values will be included in the log.

                The actual values will be logged in the following cases:
                - None, int, float: All the time
                - list, set, tuple, dict, str: If the __repr__ of the value has
                  length less than 50 characters

                Otherwise, the values will be coerced to be more readable:
                - str: Value will be truncated to 50 characters (47 plus an ellipsis)
                - list, set, tuple, dict, pd.Series: The type with the length
                - pd.DataFrame: The type with the shape

            *DEPRECATED v1.3.1, REMOVE in v1.4* 
            (list[str])
                To combat cumbersome __repr__ for some parameter values, a list
                of strings can be passed - indicating which parameters should
                have their values added to the log.

        include_output (bool, default is False)
            Should the output be logged?

            If True, then the output of the function will be included in the log. If
            False, then the output will not be logged.

            NOTE: If this is True, then *two* log entries will be made for this
                  function call: one when it's called, one when it returns.

            NOTE II: Values will be subject to the same truncation as described
                     in `include_params`.

        *DEPRECATED v1.3.1, REMOVE in v1.4*
        include_output_size (bool, default is False)
            Should the size of the outputted value(s) be logged?

            If True, then the size (__len__) of the output of the function
            be included in the log. If False, then the output will not be logged.

            NOTE: If this is True, then *two* log entries will be made for this
                  function call: one when it's called, one when it returns.
    
    """
    if not isinstance(include_params, bool):
        msg = 'Passing a list of param names to `include_params` is now deprecated. '
        warnings.warn(msg, category=UserWarning)

        # Set to True - which would be the new (probably...) desired behaviour on
        # the grounds they'd now likely be happy to have the coerced version 
        # displayed.
        include_params = True

    if include_output_size:
        msg = '`include_output_size` is deprecated - use `include_output` instead'
        warnings.warn(msg, category=UserWarning)

        # Enforce the use of include_output instead.
        include_output_size = False
        include_output = True

    def decorator(function: callable):

        def wrapper(*args, **kwargs):
            function_call_str = _get_function_call_str(
                function, 
                args, 
                kwargs, 
                include_params
            )
            logger.log(level, function_call_str)

            try:
                output = function(*args, **kwargs)
            except Exception as error:
                error_str = _get_error_str(error, function_call_str)
                logger.log('ERROR', error_str)
                raise error

            if include_output:
                output_str = _get_output_str(output, function_call_str)
                logger.log(level, output_str)

            return output

        return wrapper

    return decorator    


def _get_function_call_str(
    function: callable, 
    args: tuple, 
    kwargs: dict, 
    include_params: bool
) -> str:
    if include_params: 
        function_call_params_str = _get_function_call_params_str(args, kwargs)
    else:
        function_call_params_str = ''

    return f'{function.__module__}:{function.__name__}({function_call_params_str})'


def _get_function_call_params_str(args: str, kwargs: dict) -> str:
    return ', '.join(
        [
            _coerce_value(arg)
            for arg 
            in args
        ]
        + [
            f'{k}={_coerce_value(v)}' 
            for k, v 
            in kwargs.items()
        ]
    )


def _get_output_str(output: Any, function_call_str: str) -> str:
    # We know that only a maximum of one of include_output and include_output_size is True.
    return function_call_str + f' -> {_coerce_value(output)}'


def _get_error_str(error: Exception, function_call_str: str) -> str:
    return function_call_str + f' -> {error.__repr__()}'


def _coerce_value(value: Any) -> Any:
    if value is None:
        return 'None'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return _coerce_str(value)
    elif isinstance(value, (list, set, tuple, dict)):
        return _coerce_basic_iterable(value)
    elif isinstance(value, pd.DataFrame):
        return _coerce_dataframe(value)
    elif isinstance(value, pd.Series):
        return _coerce_series(value)
    else:
        return _coerce_other(value)


def _coerce_str(value: str) -> str:
    # Limit the string the 50 characters.
    if len(value) <= 50:
        return value.__repr__()
    else:
        truncated = value[:47] + '...'
        return truncated.__repr__()


def _coerce_basic_iterable(value: list | set | tuple | dict) -> str:
    if len(value.__repr__()) <= 50:
        return value.__repr__()
    else:
        return f'{value.__class__.__name__}<len={len(value)}>'


def _coerce_dataframe(value: pd.DataFrame) -> str:
    return f'DataFrame<shape={value.shape}>'


def _coerce_series(value: pd.Series) -> str:
    return f'Series<len={len(value)}>'


def _coerce_other(value: Any) -> str:
    return value.__class__.__name__
