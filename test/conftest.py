import pytest
from path import Path


@pytest.fixture
def tmp_path(tmpdir):
    return Path(str(tmpdir))
