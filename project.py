"""MM Assigner: App that matches mentors and mentees"""

# Import relevant modules
# pylint: disable=import-error
import streamlit as st
from pycountry import languages as LANGUAGES

# Set data variable for dev (will be replaced by the session state)
DATA = {"mentors": [], "mentees": []}

# Define a main function that just defines the general format
def main():
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
def set_page_config():
    """Set the main page configuration"""
    st.set_page_config(
        page_title="MM Assigner", layout="wide", initial_sidebar_state="collapsed"
    )


def add_person():
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


def col_1_content():
    """Defines the content of the first column"""
    st.write("# MM Assigner")
    st.write("This app allows you to assigns mentors to mentees.")
    add_person()


def col_2_content():
    """Defines the content of the second column"""
    st.write("Col 2 content")
    st.json(DATA)


def col_3_content():
    """Defines the content of the third column"""
    st.write("Col 3 content")


if __name__ == "__main__":
    main()
