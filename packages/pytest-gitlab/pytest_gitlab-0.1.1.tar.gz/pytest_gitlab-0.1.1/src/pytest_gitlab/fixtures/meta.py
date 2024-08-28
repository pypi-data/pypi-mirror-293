from pathlib import Path

import gitlab
import pytest


@pytest.fixture(scope='session')
def pt_gitlab_dir() -> Path:
    import pytest_gitlab

    return Path(pytest_gitlab.__file__).parent


@pytest.fixture(autouse=True)
def mock_clean_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensures user-defined environment variables do not interfere with tests."""
    monkeypatch.delenv('PYTHON_GITLAB_CFG', raising=False)
    monkeypatch.delenv('GITLAB_PRIVATE_TOKEN', raising=False)
    monkeypatch.delenv('GITLAB_URL', raising=False)
    monkeypatch.delenv('CI_JOB_TOKEN', raising=False)
    monkeypatch.delenv('CI_SERVER_URL', raising=False)


@pytest.fixture(autouse=True)
def default_files(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensures user configuration files do not interfere with tests."""
    monkeypatch.setattr(gitlab.config, '_DEFAULT_FILES', [])


@pytest.fixture
def valid_gitlab_ci_yml() -> str:
    return """---
:test_job:
  :script: echo 1
"""


@pytest.fixture
def invalid_gitlab_ci_yml() -> str:
    return 'invalid'
