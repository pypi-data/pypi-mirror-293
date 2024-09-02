import pytest
import uuid
from datetime import datetime

from dialogicai.utils import current_time, generate_uuid

def test_current_time():
    assert current_time() == datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_str = current_time()
    assert len(time_str) == 19
    assert time_str[4] == "-"
    assert isinstance(time_str, str)

    try:
        datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail("The time string is not in the correct format.")


def test_generate_uuid():
    """
    Test the generate_uuid function.
    """
    uuid_str = generate_uuid()
    assert isinstance(uuid_str, str)
    assert len(uuid_str) == 36
    assert uuid_str[8] == "-"
    assert uuid_str[13] == "-"
    assert uuid_str[18] == "-"
    assert uuid_str[23] == "-"

    try:
        val = uuid.UUID(uuid_str, version=4)
        assert val.version == 4
        assert val.hex == uuid_str.replace("-", "")
    except ValueError:
        pytest.fail("The UUID string is not in the correct format.")