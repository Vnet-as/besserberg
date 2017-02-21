

class BackendsRegistry(dict):

    def register(self, backend_class):
        code = backend_class.get_code()
        if code:
            self[backend_class.get_code()] = backend_class()
        return bool(code)


backends_registry = BackendsRegistry()


class BesserbergBackendMeta(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(BesserbergBackendMeta, cls).__new__(
            cls, name, bases, attrs)
        backends_registry.register(new_class)
        return new_class


class BesserbergBackend(metaclass=BesserbergBackendMeta):
    '''
    Base class for all besserberg's PDF backends.
    '''

    BACKEND_CODE = None

    @classmethod
    def get_code(cls):
        return cls.BACKEND_CODE

    def render(self, template, options=None):
        raise NotImplementedError('Subclass must implement this method.')
