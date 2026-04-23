import pytest
import pytest_asyncio


# @pytest.mark.asyncio
# def test_simple():
#     assert 1 == 1




@pytest.mark.asyncio
@pytest.mark.parametrize(
    "in_data, out_data",
    [
        (
            1,
            1
        ),
        (
            2,
            2
        ),
        (
            3,
            3
        ),

    ]
)
async def test_simple_param(in_data, out_data):
    assert in_data == out_data