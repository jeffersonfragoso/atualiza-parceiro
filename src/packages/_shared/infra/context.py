from contextvars import ContextVar
from typing import Optional

# _tracer_id_ctx_var: ContextVar[str] = ContextVar("tracer_id", default=None)


# def set_tracer_id():
#     tracer_id = get_tracer_id()
#     if not tracer_id:
#         return _tracer_id_ctx_var.set(str(uuid4()))


# def get_tracer_id() -> str:
#     return _tracer_id_ctx_var.get()


# def reset_tracer_id(tracer_id):
#     _tracer_id_ctx_var.reset(tracer_id)


# # Middleware
# tracer_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)
