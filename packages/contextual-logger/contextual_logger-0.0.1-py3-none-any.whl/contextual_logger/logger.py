"""A logger that lets you drop context markers that are included in extras."""

import functools
import logging
import operator as op


class ContextualLogger(logging.Logger):
    def __init__(self, *args, **kwargs):
        """Allow functions earlier in the call stack to set context information in later logs messages.

        This allows us to avoid things like: Passing kwargs to inner functions
          for the sole purpose of logging, logging at multiple levels with some
          sort of association key.

        Note: This doesn't support opening a logging context A, then a context B
              and then closing context A without closing B first. This is inline
              with how python context managers work (i.e. ExitStack).

        Note: This is not threadsafe, it could be possible to have ._context
              changed in one thread before another emits it's log message.
        """
        super().__init__(*args, **kwargs)
        self._context = []
        self._cached_context = None

    @property
    def context(self):
        if not self._cached_context:
            # TODO: Detect and warn/error about overwrites in the context.
            self._cached_context = functools.reduce(op.or_, self._context, {})
        return self._cached_context

    def __call__(self, **kwargs):
        """Save the current context.

        This is what is called first when you do `with logger(...):`. It allows
        us to call the `with` with different arguments to save different contexts
        in different places.
        """
        # TODO: Make it possible to set the context for specific log levels?
        self._context.append(kwargs)
        self._cached_context = None
        return self

    # We enumerate the arguments, instead of using *args, **kwargs as several
    # logger methods call things positionally and setting `extra` in kwargs can
    # cause double values for it.
    def makeRecord(self, name, level, fn, lno, msg, args,exc_info, func=None, extra=None, sinfo=None):
        """Make sure the context is in the extra field."""
        # Save context to a local variable to avoid running the reduction
        # multiple times.
        ctx = self.context
        # Combine extra and context, while preserving extra=None if neither are
        # defined. If only ctx is defined, that is passed as extra. Extra and no
        # ctx passes extra through. If they are both defined, they are combined.
        if extra is not None:
            # An empty context is {} so we can always pass it to the or
            extra |= ctx
        # This branch only happens when extra is None and ctx is not empty
        elif ctx:
            extra = ctx
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func=func, extra=extra, sinfo=sinfo)

    def __enter__(self):
        """Turn it into a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tab):
        """"When the `with` statement is closed, remove the most recent context."""
        if self._context:
            # TODO: Add error messaging/failure. However, if you closing the
            # context manager and there isn't a context to pop you are in what
            # should be an unreachable state.
            self._context.pop()
            self._cached_context = None


logging.setLoggerClass(ContextualLogger)
