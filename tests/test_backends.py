from besserberg.backends import base as backends_base


def test_basic_register():
    backends_base.backends_registry = backends_base.BackendsRegistry()
    assert not backends_base.backends_registry

    class TestBackend(backends_base.BesserbergBackend):
        BACKEND_CODE = 'test-backend'

    br = backends_base.backends_registry
    assert isinstance(br['test-backend'], TestBackend)
