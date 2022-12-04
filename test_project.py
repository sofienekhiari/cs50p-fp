"""Test file for the MM Assigner app"""

# pylint: disable=wildcard-import,unused-wildcard-import,
# pylint: disable=undefined-variable,no-name-in-module

from test_data import *
from project import (
    filter_mentees,
    generate_participant_notification,
    save_notification_to_file,
)


def test_filter_mentees():
    """Test the filter mentees function"""
    # Extract data to use
    people_list = [
        david_abendroth,
        maria_nacht,
        mario_moeller,
        simone_ebersbacher,
        niklas_abt,
    ]
    # Test for multiple results
    assert filter_mentees(people_list, "English") == [
        david_abendroth,
        simone_ebersbacher,
        niklas_abt,
    ]
    # Test for one result
    assert filter_mentees(people_list, "Swiss German") == [maria_nacht]
    # Test for no results
    assert len(filter_mentees(people_list, "Japanese")) == 0


def test_generate_participant_notification():
    """Test the generate participant notification function"""
    # Test generation of assigned mentor
    assert (
        generate_participant_notification(
            participant_name=david_abendroth["name"],
            participant_email=david_abendroth["email"],
            participant_assigned=True,
            other_participant_name=mario_moeller["name"],
            other_participant_email=mario_moeller["email"],
            other_participant_role="Mentee",
        )
        == DAVID_ABENDROTH_TRUE_MARIO_MOELLER
    )
    # Test generation of non-assigned participant
    assert (
        generate_participant_notification(
            participant_name=jan_fuchs["name"],
            participant_email=jan_fuchs["email"],
            participant_assigned=False,
            other_participant_name="",
            other_participant_email="",
            other_participant_role="Mentee",
        )
        == JAN_FUCHS_FALSE
    )
    # Test generation of assigned mentee
    assert (
        generate_participant_notification(
            participant_name=mathias_zimmermann["name"],
            participant_email=mathias_zimmermann["email"],
            participant_assigned=True,
            other_participant_name=maria_nacht["name"],
            other_participant_email=maria_nacht["email"],
            other_participant_role="Mentor",
        )
        == MATHIAS_ZIMMERMANN_TRUE_MARIA_NACHT
    )


def test_save_notification_to_file():
    """Test the save notification to file function"""
    save_notification_to_file("test", "Test content")
    with open("Exported notifications/test.txt", "r", encoding="utf-8") as test_file:
        assert test_file.read() == "Test content"
