import pathlib
import textwrap
import zipfile
from unittest.mock import Mock, patch

import pytest
from packaging.requirements import Requirement
from packaging.version import Version

from fromager import sdist
from fromager.context import WorkContext


@patch("fromager.sources.resolve_dist")
def test_missing_dependency_format(
    resolve_dist: Mock,
    tmp_context: WorkContext,
):
    resolutions = {
        "flit_core": "3.9.0",
        "setuptools": "69.5.1",
    }
    resolve_dist.side_effect = lambda ctx, req, url: (
        "",
        Version(resolutions[req.name]),
    )

    req = Requirement("setuptools>=40.8.0")
    other_reqs = [
        Requirement("flit_core"),
        req,
    ]
    ex = sdist.MissingDependency(tmp_context, "test", req, other_reqs)
    s = str(ex)
    # Ensure we report the thing we're actually missing
    assert "Failed to install test dependency setuptools>=40.8.0. " in s
    # Ensure we report what version we expected of that thing
    assert "setuptools>=40.8.0 -> 69.5.1" in s
    # Ensure we report what version we expect of all of the other dependencies
    assert "flit_core -> 3.9.0" in s


def test_ignore_based_on_marker(tmp_context: WorkContext):
    version = sdist.handle_requirement(
        ctx=tmp_context,
        req=Requirement('foo; python_version<"3.9"'),
        req_type="toplevel",
        why=[],
    )
    assert version == ""


@patch("fromager.sources.download_url")
def test_invalid_wheel_file_exception(mock_download_url, tmp_path: pathlib.Path):
    mock_download_url.return_value = pathlib.Path(tmp_path / "test" / "fake_wheel.txt")
    fake_url = "https://www.thisisafakeurl.com"
    fake_dir = tmp_path / "test"
    fake_dir.mkdir()
    text_file = fake_dir / "fake_wheel.txt"
    text_file.write_text("This is a test file")
    with pytest.raises(zipfile.BadZipFile):
        sdist._download_wheel_check(fake_dir, fake_url)


def test_missing_dependency_pattern():
    msg = textwrap.dedent("""
        Looking in indexes: http://192.168.0.201:9999/simple
        Looking in links: /Users/dhellmann/.pip/wheelhouse
        Processing /Users/dhellmann/.pip/wheelhouse/pbr-6.0.0-py2.py3-none-any.whl (from -r /Users/dhellmann/Devel/fromager/fromager/e2e-output/work-dir/stevedore-5.2.0/build-3.12.0/requirements.txt (line 1))
        ERROR: Could not find a version that satisfies the requirement setuptools>=40.8.0 (from versions: 11.3.1, 14.0)
        ERROR: No matching distribution found for setuptools>=40.8.0
        """)
    match = sdist._pip_missing_dependency_pattern.search(msg)
    assert match is not None


def test_missing_dependency_pattern_resolution_impossible():
    msg = textwrap.dedent("""
    Looking in indexes: http://10.1.0.116:9999/simple
    ERROR: Cannot install setuptools>=40.8.0 because these package versions have conflicting dependencies.

    The conflict is caused by:
        The user requested setuptools>=40.8.0
        The user requested (constraint) setuptools<72.0.0

    To fix this you could try to:
    1. loosen the range of package versions you've specified
    2. remove package versions to allow pip to attempt to solve the dependency conflict

    ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts
    """)
    match = sdist._pip_missing_dependency_pattern.search(msg)
    assert match is not None
