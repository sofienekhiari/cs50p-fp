"""MM Assigner: App that matches mentors and mentees"""

# Import relevant modules
# pylint: disable=import-error
import streamlit as st
from pycountry import languages as LANGUAGES
from tinydb import TinyDB # pylint: disable=unused-import

# Set data variable for dev (will be replaced by the session state)
DATA = {"mentors": [], "mentees": []}

# Define a main function that just defines the general format
def main():  # DONE
    """Main function"""
    set_page_config()
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        col_1_content()
    with col_2:
        col_2_content()
    with col_3:
        col_3_content()


# Set the streamlit page configuration
def set_page_config():  # DONE
    """Set the main page configuration"""
    st.set_page_config(
        page_title="MM Assigner", layout="wide", initial_sidebar_state="collapsed"
    )


def col_1_content():  # DONE
    """Defines the content of the first column"""
    st.write("# MM Assigner")
    st.write("This app allows you to assigns mentors to mentees.")
    add_person()


def add_person():  # WAITING FOR DATABASE INTRODUCTION
    """Function that adds a new person"""
    languages_list = [language.name for language in list(LANGUAGES)]
    with st.form("add_person", clear_on_submit=True):
        st.write("### Add a person")
        role = st.selectbox("Role", ["Mentor", "Mentee"])
        name = st.text_input("Full name")
        email = st.text_input("Email")
        generally_preferred_language = st.selectbox(
            "Generally preferred language", languages_list
        )
        prefers_preferred_language = st.checkbox(
            label="I would rather use my preferred language"
        )
        mentor_submitted = st.form_submit_button("Add")
    if mentor_submitted:
        if role == "Mentor":
            DATA["mentors"].append(
                {
                    "name": name,
                    "email": email,
                    "generally_preferred_language": generally_preferred_language,
                    "prefers_preferred_language": prefers_preferred_language,
                }
            )
        else:
            DATA["mentees"].append(
                {
                    "name": name,
                    "email": email,
                    "generally_preferred_language": generally_preferred_language,
                    "prefers_preferred_language": prefers_preferred_language,
                }
            )


def col_2_content():  # WAITING FOR DATABASE INTRODUCTION
    """Defines the content of the second column"""
    st.write("Col 2 content")
    st.json(DATA)

class MMDatabase():  # IN PROGRESS
    """Class that takes charge of interacting with the database

    Algorithm
    -----------

    # Init function
        # Initiate the instance by assigning TinyDB('.mm_assigner_db.json') to it.
        # The database is basically comprised of a dictionary containing two key, one
        # for the mentors and one for mentees. You need to make sure when initiating
        # the database that this structure is already present in the database. For
        # that, you need to make sure that there's a dictionnary with two keys, one for
        # the mentors and one for the mentees, and that there's a list corresponding to
        # each key.

    # Add mentee function
        # Check that the person passed to this function is a mentee
        # Generate proper formatting for the entry in the database
        # Add the entry to the database

    # Add mentor function
        # Check that the person passed to this function is a mentor
        # Generate proper formatting for the entry in the database
        # Add the entry to the database$

    """


def col_3_content():  # IN PROGRESS
    """Defines the content of the third column"""
    st.write("Col 3 content")


def filter_mentees(people_list, language):  # WAITING FOR TESTING
    """Filter the mentees list depending on the chosen language"""
    return [
        person
        for person in people_list
        if person["generally_preferred_language"] == language
    ]


def assign_mentors_mentees():  # IN PROGRESS
    """Function that assigns mentors to mentees

     Algorithm
    -----------

    # Create a variable to hold the combinations
    # Create a variable to hold the non-assigned people
    # Get the list of mentors
    # Get the list of mentees
    # Repeat indefinitely:
        # If the list of mentors is empty or the list of mentees is empty:
            # Leave the loop
        # Randomly select a mentor (take it out of the mentors list)
        # Create a local (per loop) copy of the mentees list
        # If the mentor prefers a certain language:
            # Filter the mentees list depending on the language in question
            # If the result of the filter is not empty:
                # Assign the filtered list to the local copy
        # Create a combination of the mentor and a random choice
        # from the local copy of the mentees list (take the latter
        # out of the mentees list)
        # Add the combination to the combinations variable
    # Add all the remaining people to the non-assigned people list
    # Return the combinations variable and the remaining people one

    """


def notify_participants():
    """Function that generates the emails to
    send to the different participants

    Algorithm
    -----------

    # Create a variable to hold the notification messages
    # Get the list of combinations
    # Get the list of remaining people
    # For every combination in the list of combinations:
        # Get the mentor and the mentee in seperate variables
        # Store the right notification message for the mentor in the notification
        # messages variable
        # Store the right notification message for the mentee in the notification
        # messages variable
    # For every combination in the list of remaning people:
        # Get the mentor and the mentee in seperate variables
        # Store the right notification message for the mentor in the notification
        # messages variable
        # Store the right notification message for the mentee in the notification
        # messages variable
    # Create a variable to hold the human readable output format
    # Format the notification messages to be human readable and store the result in the
    # human readable output format variable
    # Store the result in a file and output a notification

    """


if __name__ == "__main__":  # DONE
    main()
