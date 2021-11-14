import pytest

from labgrid.driver.fake import FakeCommandDriver
from labgrid import Target


@pytest.fixture
def command():
    t = Target("dummy")
    d = FakeCommandDriver(t, "command")
    t.activate(d)
    return d
