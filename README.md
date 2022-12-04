# MM Assigner

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sofienekhiari/cs50p-fp?label=version)
[![MM Assigner Tests](https://github.com/sofienekhiari/cs50p-fp/actions/workflows/tests.yaml/badge.svg)](https://github.com/sofienekhiari/cs50p-fp/actions/workflows/tests.yaml)
![GitHub top language](https://img.shields.io/github/languages/top/sofienekhiari/cs50p-fp)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/sofienekhiari/cs50p-fp)
![GitHub](https://img.shields.io/github/license/sofienekhiari/cs50p-fp)

## Video Demo

The app video demo can be found following [this link](https://youtu.be/OIb_oKSPKy0).

## Description

### General project description

This project is an app that gives the possibility for representatives of groups (for example at university) to collect data about mentors and mentees and randomly assign one to another, generating automatically email data that can be sent manually (see _design choices_ later).
It takes into account if there are any preferences for the mentors when it comes to the language of the interaction.

The app's source code and versions history can be found following [this link](https://github.com/sofienekhiari/cs50p-fp).

### Usage

The app is run locally just as the data that is saved.
To do so, you can clone this repository and run the following code.

```bash
set -e

# Install pipenv
pip3 install pipenv

# Install dependencies
pipenv install
pipenv shell

# Run app
streamlit run project.py
```

_N.B._ You are welcome to fork this repository and publish your version of the app online.
Please remember to change the database to an online non-prototype one.

### Project files structure

The project mainly contains the following files:

- `project.py` (contains the app's main code)
- `test_project.py` (contains the app's tests)
- `test_data.py` (contains sample data to be used for the tests) 

### Code and design explanation

#### The MMDatabase class

This class encapsulates the needed code to interact with the database.
Its sole purpose is to simplify the code and reduce redundancy.
There are only functions to save mentors and mentees to the database (in their respective table structure), no other data and no function(s) to retreive data from the database.
This is because the data retrieval process and code are pretty straightforward and don't need encapsulation.

#### The main function

The main function is a simple one that sets up the page configuration and the general layout of the app.
The choice of such a main function was made for the purpose of seperation of concerns.
This way, the code is easier to write, read and test.

#### The col_*_content functions

The functions with the format `col_*_content` contain the UI code and functions calls for each related section and functionality.
They also contain the code for the event loop hooks and triggers.
The `*` in this case corresponds to the number of the column in question.

#### The add_person function

This function adds a person entry to the database.
It generates the needed UI elements to collect the data about the person.
Then, it formats said data and adds it to the database depending on the role of the person.

In the case of this app, roles consist of simple strings instead of possible enums.
This design choice is explained by the later usage of the GUI interface by the users and not the functions themselves directly and the relatively small size of the project.
The introduction of the enums and associated safety didn't therefore seem necessary.

No verification of the data (number of characters, email format) has been implemented in this version but it could be implemented in the future.

#### The filter_mentees function

This function takes the list of mentees as an input and the specified language.
It then creates a filtered list of mentees that have the same language value and returns it.

#### The assign_mentors_mentees function

This function gets the list of mentors and list of mentees and assigns mentors to mentees in a random way, possibly taking the language into account.
It updates the list of assigned couples and possibly the list of people that were not assigned to other ones.

Since the lists are generally very small in this use case, no detailed thought has been put into optimising the efficiency of the assigning algorithm.

#### The generate_participant_notification function

This function generates the right notification text for each participant in the right format.
This depends on whether the participant was assigned another one and the roles of each.

#### The save_notification_to_file function

This function takes a file name and content as input and creates a file in the proper directory with that content inside.

#### The notify_participants function

This function gets the result of the assign_mentors_mentees function and creates a file for every participant in the right sub-folder (using the `save_notification_to_file` function) containing the proper data and content to be sent to that person depending on whether they were selected for the program or not and depending on their role (content generated by the `generate_participant_notification` function).
