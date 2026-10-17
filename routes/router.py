import re
from flask import Blueprint


class Router(Blueprint):
    """
    Blueprint dengan gaya route Hono:

        admin.get('/user/:id', auth_middleware, admin_only, user_controller.get_detail)

    Handler terakhir adalah controller, sisanya middleware `def middleware(next)`.
    Parameter `:id` otomatis diubah ke format Flask `<id>` dan diteruskan ke controller.
    """

    def get(self, rule, *handlers, **options):
        return self._add('GET', rule, handlers, options)

    def post(self, rule, *handlers, **options):
        return self._add('POST', rule, handlers, options)

    def put(self, rule, *handlers, **options):
        return self._add('PUT', rule, handlers, options)

    def patch(self, rule, *handlers, **options):
        return self._add('PATCH', rule, handlers, options)

    def delete(self, rule, *handlers, **options):
        return self._add('DELETE', rule, handlers, options)

    def _add(self, method, rule, handlers, options):
        if not handlers:
            return self.route(rule, methods=[method], **options)

        *middlewares, controller = handlers

        def endpoint(**params):
            def dispatch(index):
                if index == len(middlewares):
                    return controller(**params)
                return middlewares[index](lambda: dispatch(index + 1))

            return dispatch(0)

        names = self.__dict__.setdefault('_endpoint_names', set())
        name  = base = f"{method.lower()}_{controller.__qualname__}".replace('.', '_')
        count = 2
        while name in names:
            name   = f"{base}_{count}"
            count += 1
        names.add(name)

        self.add_url_rule(re.sub(r':(\w+)', r'<\1>', rule), endpoint=name, view_func=endpoint, methods=[method], **options)
        return controller
