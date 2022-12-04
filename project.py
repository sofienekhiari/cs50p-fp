"""MM Assigner: App that matches mentors and mentees"""


import os
import random
import streamlit as st
from pycountry import languages as LANGUAGES
from tinydb import TinyDB


class MMDatabase:
    """Class that interacts with the database"""

    def __init__(self):
        """Function that initiates the database and the two tables"""
        self.db = TinyDB(".mm_assigner_db.json")  # pylint: disable=invalid-name
        self.mentors = self.db.table("mentors")
        self.mentees = self.db.table("mentees")

    def add_mentee(
        self,
        role,
        name,
        email,
        generally_preferred_language,
        prefers_preferred_language,
    ):  # pylint: disable=too-many-arguments
        """Function that adds a mentee to the database"""
        self.mentees.insert(
            {
                "role": role,
                "name": name,
                "email": email,
                "generally_preferred_language": generally_preferred_language,
                "prefers_preferred_language": prefers_preferred_language,
            }
        )

    def add_mentor(
        self,
        role,
        name,
        email,
        generally_preferred_language,
        prefers_preferred_language,
    ):  # pylint: disable=too-many-arguments
        """Function that adds a mentor to the database"""
        self.mentors.insert(
            {
                "role": role,
                "name": name,
                "email": email,
                "generally_preferred_language": generally_preferred_language,
                "prefers_preferred_language": prefers_preferred_language,
            }
        )


# Initialise the database
mma_db = MMDatabase()
# Create a session_state variable to hold the combinations
if "combinations_assigned" not in st.session_state:
    st.session_state.combinations_assigned = []
# Create a session_state variable to hold the non-assigned people
if "combinations_non_assigned" not in st.session_state:
    st.session_state.combinations_non_assigned = []
# Create a session_state variable to hold the state of the generation button
if "generation_button_disabled" not in st.session_state:
    st.session_state.generation_button_disabled = True


def main():
    """Main function"""
    # Set the page configuration
    set_page_config()
    # Define the general layout of the app
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        col_1_content()
    with col_2:
        col_2_content()
    with col_3:
        col_3_content()


def set_page_config():
    """Sets the main page configuration"""
    st.set_page_config(
        page_title="MM Assigner", layout="wide", initial_sidebar_state="collapsed"
    )


def col_1_content():
    """Defines the content of the first column"""
    st.write("# MM Assigner")
    st.write("This app allows you to assigns mentors to mentees.")
    add_person()


def add_person():
    """Adds a new person"""
    # Format the languages list
    languages_list = [language.name for language in list(LANGUAGES)]
    # Generate the form
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
        person_submitted = st.form_submit_button("Add")
    # Generate hook for person submitted event
    if person_submitted:
        if role == "Mentor":
            mma_db.add_mentor(
                role,
                name,
                email,
                generally_preferred_language,
                prefers_preferred_language,
            )
        else:
            mma_db.add_mentee(
                role,
                name,
                email,
                generally_preferred_language,
                prefers_preferred_language,
            )


def col_2_content():
    """Defines the content of the second column"""
    # Only show the assignment button when there are at least two people,
    # one of each role
    assigner_button_disabled = True
    if len(mma_db.mentees.all()) > 0 and len(mma_db.mentors.all()) > 0:
        assigner_button_disabled = False
    assigner_button_clicked = st.button(
        "Assign mentors & mentees", disabled=assigner_button_disabled
    )
    # Generate hook for assigner button clicked event
    if assigner_button_clicked:
        assign_mentors_mentees()
        # Enable the export button in the third column
        st.session_state.generation_button_disabled = False
    # Display the list of people entered
    st.write("## Mentors")
    st.dataframe(
        [
            {
                "Name": mentor["name"],
                "E-Mail": mentor["email"],
                "Preferred Language": mentor["generally_preferred_language"],
            }
            for mentor in mma_db.mentors.all()
        ]
    )
    st.write("## Mentees")
    st.dataframe(
        [
            {
                "Name": mentee["name"],
                "E-Mail": mentee["email"],
                "Preferred Language": mentee["generally_preferred_language"],
            }
            for mentee in mma_db.mentees.all()
        ]
    )


def col_3_content():
    """Defines the content of the third column"""
    # Show the generation button
    generation_button_clicked = st.button(
        "Generate notifications", disabled=st.session_state.generation_button_disabled
    )
    # Generate hook for generation button clicked event
    if generation_button_clicked:
        notify_participants()
    # Display the result of the assignment
    st.write("## Generated combinations")
    st.dataframe(
        [
            {
                "Mentor": mentor["name"],
                "Mentee": mentee["name"],
            }
            for mentor, mentee in st.session_state.combinations_assigned
        ]
    )
    st.write("## Non-assigned participants")
    st.dataframe(
        [
            {
                "Name": participant["name"],
            }
            for participant in st.session_state.combinations_non_assigned
        ]
    )


def filter_mentees(people_list, language):
    """Filters the mentees list depending on the chosen language"""
    return [
        person
        for person in people_list
        if person["generally_preferred_language"] == language
    ]


def assign_mentors_mentees():
    """Assigns mentors to mentees"""
    # Get the list of mentors
    mentors_list = mma_db.mentors.all()
    # Get the list of mentees
    mentees_list = mma_db.mentees.all()
    # Reset the combinations variables
    st.session_state.combinations_assigned = []
    st.session_state.combinations_non_assigned = []
    # Repeat indefinitely:
    while True:
        # If the list of mentors is empty or the list of mentees is empty:
        if not mentors_list or not mentees_list:
            # Leave the loop
            break
        # Randomly select a mentor (take it out of the mentors list)
        mentor = random.choice(mentors_list)
        mentors_list.remove(mentor)
        # Create a local (per loop) copy of the mentees list
        local_mentees_list = mentees_list.copy()
        # If the mentor prefers a certain language:
        if mentor["prefers_preferred_language"]:
            # Filter the mentees list depending on the language in question
            filtered_mentees_list = [
                mentee
                for mentee in local_mentees_list
                if mentee["generally_preferred_language"]
                == mentor["generally_preferred_language"]
            ]
            # If the result of the filter is not empty:
            if filtered_mentees_list:
                # Assign the filtered list to the local copy
                local_mentees_list = filtered_mentees_list
        # Get a random choice from the local copy of the mentees list (take it
        # out of the mentees list)
        mentee = random.choice(local_mentees_list)
        mentees_list.remove(mentee)
        # Add the combination to the combinations variable
        st.session_state.combinations_assigned.append((mentor, mentee))
    # Add all the remaining people to the non-assigned people list
    st.session_state.combinations_non_assigned = mentors_list + mentees_list


def generate_participant_notification(
    participant_name,
    participant_email,
    participant_assigned,
    other_participant_name,
    other_participant_email,
    other_participant_role,
):  # pylint: disable=too-many-arguments
    """Generates the appropriate notification for every participant"""
    # Generate the message subject
    message_subject = ""
    if participant_assigned:
        message_subject = f"🎉 Congrats {participant_name}, you were assigned a {other_participant_role.lower()} 🎊"  # pylint: disable=line-too-long
    else:
        message_subject = (
            f"🔥 Hey {participant_name}, we've got news about the MM program!"
        )
    # Generate the message specific content
    specific_message_content = ""
    if participant_assigned:
        specific_message_content = f"""
You were assigned {other_participant_name} as a {other_participant_role.lower()}.
You can contact them on the following e-mail address: {other_participant_email}.
"""
    else:
        specific_message_content = f"""
Due to a shortage of participants, you were not assigned a {other_participant_role.lower()}.
You can still however join one of your peers/friends with their {other_participant_role.lower()} if you want.        
"""
    # Generate the output
    return f"""
+------------------+
| PARTICIPANT NAME |
+------------------+

{participant_name}

+-------------------+
| PARTICIPANT EMAIL |
+-------------------+

{participant_email}

+-----------------+
| MESSAGE SUBJECT |
+-----------------+

{message_subject}

+-----------------+
| MESSAGE CONTENT |
+-----------------+

Dear {participant_name},
{specific_message_content}
Don't hesitate to contact us if you have any question.

Kind regards,
MM Project Team
"""


def save_notification_to_file(file_name, notification):
    """Saves the specified notification to the specified file"""
    # Check the output directory
    output_directory = "Exported notifications"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Save the data to the file
    with open(
        f"{output_directory}/{file_name}.txt", "w", encoding="utf-8"
    ) as output_file:
        output_file.write(notification)


def notify_participants():
    """Generates the emails to send to the different participants"""
    # Generate and save a notification for every participant
    # in the list of combinations
    for mentor, mentee in st.session_state.combinations_assigned:
        # Save the mentor's notification
        save_notification_to_file(
            file_name=mentor["name"],
            notification=generate_participant_notification(
                participant_name=mentor["name"],
                participant_email=mentor["email"],
                participant_assigned=True,
                other_participant_name=mentee["name"],
                other_participant_email=mentee["email"],
                other_participant_role=mentee["role"],
            ),
        )
        # Save the mentee's notification
        save_notification_to_file(
            file_name=mentee["name"],
            notification=generate_participant_notification(
                participant_name=mentee["name"],
                participant_email=mentee["email"],
                participant_assigned=True,
                other_participant_name=mentor["name"],
                other_participant_email=mentor["email"],
                other_participant_role=mentor["role"],
            ),
        )
    # Generate and save a notification for every participant
    # in the list of remaining people
    for participant in st.session_state.combinations_non_assigned:
        save_notification_to_file(
            participant["name"],
            generate_participant_notification(
                participant_name=participant["name"],
                participant_email=participant["email"],
                participant_assigned=False,
                other_participant_name="",
                other_participant_email="",
                other_participant_role="Mentor"
                if participant["role"] == "Mentee"
                else "Mentee",
            ),
        )


if __name__ == "__main__":
    main()
