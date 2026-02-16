import inspect
import time
from functools import wraps

try:
    import logfire

    logfire.configure(service_name="ai-communication-lab")
    _LOGGING_ENABLED = True
except ImportError:
    _LOGGING_ENABLED = False


class ObservationContext:
    def __init__(self):
        self.metadata = {}

    def add(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                self.metadata[k] = v


def observe_execution():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not _LOGGING_ENABLED:
                return func(*args, **kwargs)

            span_name = func.__name__
            start = time.perf_counter()
            arg_meta = _safe_argument_metadata(func, args, kwargs)

            try:
                with logfire.span(span_name, **arg_meta) as span:
                    result = func(*args, **kwargs)

                latency_ms = (time.perf_counter() - start) * 1000
                span.set_attribute("latency_ms", latency_ms)
                return result

            except Exception as e:
                latency_ms = (time.perf_counter() - start) * 1000
                logfire.error(
                    f"{span_name}_failure",
                    latency_ms=latency_ms,
                    error=str(e),
                )
                raise

        return wrapper

    return decorator


def _safe_argument_metadata(func, args, kwargs):
    """
    Extract safe metadata from arguments.
    Avoid logging full text inputs.
    """
    metadata = {}

    sig = inspect.signature(func)
    bound = sig.bind_partial(*args, **kwargs)

    for name, value in bound.arguments.items():
        if isinstance(value, str):
            metadata[f"{name}_length"] = len(value)
        else:
            metadata[f"{name}_type"] = type(value).__name__

    return metadata
