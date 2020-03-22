import pytest

from lib.foo import Foo

class TestFoo:

    @pytest.fixture
    def foo(self):
        return Foo() 

    def test_foo_bar(self, foo):
        assert foo.bar() == True
