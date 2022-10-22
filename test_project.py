"""Test file for the MM Assigner app"""
# pylint: disable=wildcard-import,undefined-variable,no-name-in-module

from test_data import *
from project import filter_mentees


def test_filter_mentees_en():
    """Test the filter mentees function
    in case the language is english"""
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


def test_filter_mentees_sg():
    """Test the filter mentees function
    in case the language is swiss german"""
    people_list = [
        david_abendroth,
        maria_nacht,
        mario_moeller,
        simone_ebersbacher,
        niklas_abt,
    ]
    assert filter_mentees(people_list, "Swiss German") == [maria_nacht]


def test_filter_mentees_nm():
    """Test the filter mentees function
    in case the language is non existant
    in the list"""
    people_list = [
        david_abendroth,
        maria_nacht,
        mario_moeller,
        simone_ebersbacher,
        niklas_abt,
    ]
    assert len(filter_mentees(people_list, "Japanese")) == 0
