import pytest
from embdata.language.describe_geometry import describe_geometry as format_robot_response


def test_trajectory_planning_all_components():
    responses = set()
    for _ in range(100):
        response = format_robot_response(1.5, -2, 3, 10, -15, 20, "meters", "degrees", True)
        responses.add(response)
        print(f"Response: {response}")
        assert "Move" in response or "Translate" in response or "Shift" in response or "Reposition" in response
        assert "1.50 meters" in response and "2.00 meters" in response and "3.00 meters" in response
        assert "10.00 degrees" in response and "15.00 degrees" in response and "20.00 degrees" in response
        assert "forward" in response.lower() or "ahead" in response.lower() or "positive x" in response.lower() or "front" in response.lower()
        assert "right" in response.lower() or "port" in response.lower() or "negative y" in response.lower()
        assert "up" in response.lower() or "skyward" in response.lower() or "positive z" in response.lower()
        assert "counterclockwise roll" in response.lower() or "positive roll" in response.lower() or "roll to the left" in response.lower()
        assert "clockwise pitch" in response.lower() or "upward pitch" in response.lower() or "negative pitch" in response.lower() or "nose-up pitch" in response.lower()
        assert "counterclockwise yaw" in response.lower() or "positive yaw" in response.lower() or "yaw to the left" in response.lower()
    assert len(responses) > 1, "No variation in responses"


def test_object_positioning_all_components():
    responses = set()
    for _ in range(100):
        response = format_robot_response(1.5, -2, 3, 10, -15, 20, "meters", "degrees", False)
        responses.add(response)
        assert "object" in response and "base frame" in response
        assert "1.50 meters" in response and "2.00 meters" in response and "3.00 meters" in response
        assert "10.00 degrees" in response and "15.00 degrees" in response and "20.00 degrees" in response
        assert "front" in response.lower() or "ahead" in response.lower() or "forward" in response.lower()
        assert "right" in response.lower() or "right side" in response.lower() or "starboard" in response.lower()
        assert "above" in response.lower() or "over" in response.lower() or "higher than" in response.lower()
    assert len(responses) > 1, "No variation in responses"



def test_no_movement():
    response = format_robot_response(0, 0, 0, 0, 0, 0, "meters", "degrees", True)
    assert (
        "Maintain" in response or "Keep" in response or "Do not change" in response or "remain stationary" in response
    )


def test_only_translation():
    response = format_robot_response(1, 2, 3, 0, 0, 0, "meters", "degrees", True)
    assert "Move" in response or "Translate" in response or "Shift" in response or "Reposition" in response
    assert "orientation" not in response.lower()


def test_only_rotation():
    response = format_robot_response(0, 0, 0, 10, 20, 30, "meters", "degrees", True)
    assert "Adjust" in response or "Modify" in response or "Change" in response or "Alter" in response
    assert (
        "Move" not in response
        and "Translate" not in response
        and "Shift" not in response
        and "Reposition" not in response
    )


def test_invalid_input():
    with pytest.raises(AssertionError):
        format_robot_response("invalid", 0, 0, 0, 0, 0, "meters", "degrees", True)


def test_missing_units():
    with pytest.raises(AssertionError):
        format_robot_response(1, 2, 3, 0, 0, 0, "", "", True)


def test_invalid_trajectory_planning():
    with pytest.raises(AssertionError):
        format_robot_response(1, 2, 3, 0, 0, 0, "meters", "degrees", "invalid")