import datetime
from today import daily_readme, follower_getter, simple_request
import pytest

def test_daily_readme():
    """
    Tests the daily_readme function to ensure it calculates age correctly.
    """
    birthday = datetime.datetime(2000, 1, 1)
    # Freeze time for a predictable result
    known_date = datetime.datetime(2023, 1, 16)
    
    # We need to monkeypatch datetime.datetime.today() to return a fixed date
    class MockDateTime(datetime.datetime):
        @classmethod
        def today(cls):
            return known_date

    # Temporarily replace the real datetime with our mocked one
    original_datetime = datetime.datetime
    datetime.datetime = MockDateTime

    age_string = daily_readme(birthday)
    
    # Restore the original datetime
    datetime.datetime = original_datetime

    assert age_string == "23 years, 0 months, 15 days"


def test_follower_getter_mocked(mocker):
    """
    Tests the follower_getter function with a mocked API response.
    This test does not make a real network request.
    """
    # 1. Create a mock response object that mimics requests.Response
    mock_response = mocker.Mock()
    
    # 2. Set the desired status code and .json() return value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "user": {
                "followers": {
                    "totalCount": 12345
                }
            }
        }
    }

    # 3. Use mocker to patch 'today.simple_request'.
    # Whenever simple_request is called in the code being tested,
    # it will return our mock_response instead of making a real API call.
    mocker.patch('today.simple_request', return_value=mock_response)

    # 4. Call the function we are testing
    follower_count = follower_getter("any_username")

    # 5. Assert that the function correctly parsed the mocked JSON
    assert follower_count == 12345 