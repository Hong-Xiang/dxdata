from .dataclass import DataClass
from contextlib import contextmanager

__all__ = ['CommonContext', 'CurrentContext', 'replace_context']

class CommonContext(DataClass):
    __slots__ = ['is_lazy']


class CurrentContext:
    ctxs = {CommonContext: CommonContext(is_lazy=False)}

    @classmethod
    def get(cls, ctx_cls=None):
        if ctx_cls is None:
            ctx_cls = CommonContext
        return ctxs.get(ctx_cls)

    @classmethod
    def replace(cls, ctx_cls, ctx_ins):
        cls.ctxs[ctx_cls] = ctx_ins


@contextmanager
def replace_context(ctx):
    pre = CurrentContext.get(type(ctx))
    try:
        CurrentContext.replace(type(ctx), ctx)
        yield
    except:
        pass
    CurrentContext.replace(type(ctx), pre)