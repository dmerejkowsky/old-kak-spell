from typing import Any
import pytest
from pathlib import Path
import xdg.BaseDirectory


@pytest.fixture
def mocked_xdg(mocker: Any, tmp_path: Path) -> None:
    data_path_mock = mocker.patch("xdg.BaseDirectory.save_data_path")
    data_path_mock.side_effect = lambda name: tmp_path / "share" / name
