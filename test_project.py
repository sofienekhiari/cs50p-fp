"""Test file for the MM Assigner app"""
# pylint: disable=wildcard-import,unused-wildcard-import,undefined-variable,no-name-in-module

from test_data import *
from project import filter_mentees


def test_filter_mentees():
    """Test the filter mentees function"""
    people_list = [
        david_abendroth,
        maria_nacht,
        mario_moeller,
        simone_ebersbacher,
        niklas_abt,
    ]
    assert filter_mentees(people_list, "English") == [
        david_abendroth,
        simone_ebersbacher,
        niklas_abt,
    ]
    assert filter_mentees(people_list, "Swiss German") == [maria_nacht]
    assert len(filter_mentees(people_list, "Japanese")) == 0
