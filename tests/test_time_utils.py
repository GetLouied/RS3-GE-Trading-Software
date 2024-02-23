import pytest
from rs3_trading.utils.utilities import pop_unix_time_from_dict

## Name Format: Test_<function>_when_<condition>_return_<result>


def test_pop_unix_time_from_dict_when_valid_dict_return_unix_time():
    ## Arrange - Put all the testing data together
    MOCK_UNIX_TIME = 1234567
    input_dict = {
        '%LAST_UPDATE%': MOCK_UNIX_TIME,
        '%LAST_UPDATE_F%': 'foobar'
    }
    ## Act - Call the function under test
    result = pop_unix_time_from_dict(input_dict)

    ## Assert - Make an assertion about the output
    assert MOCK_UNIX_TIME == result
    assert isinstance(result, int)


def test_pop_unix_time_from_dict_when_valid_pop_from_dict():

    MOCK_UNIX_TIME = 1234567
    input_dict = {
        '%LAST_UPDATE%': MOCK_UNIX_TIME,
        '%LAST_UPDATE_F%': 'foobar'
    }

    _ = pop_unix_time_from_dict(input_dict)

    assert {} == input_dict


def test_pop_unix_time_from_dict_when_empty_dict():

    input_dict = {}

    result = pop_unix_time_from_dict(input_dict)

    assert result is None

if __name__ == "__main__":
    pytest.main()