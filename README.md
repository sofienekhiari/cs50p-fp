# MM Assigner

## Demo

The app demo can be found following [this link]().

## Description

### Code and design explanation

#### The `main` function

The main function is a simple one that sets up the page configuration and the general layout of the app.
The choice of such a main function was made for the purpose of `seperation of concerns`.
This way, the code is easier to write, read and test.
The functions with the format `col_*_content` contain the UI code and functions calls for each related section and functionality.

#### The `add_person` function

This function adds a `person` entry to the database.
It generates the needed `UI` elements to collect the data about the person.
Then, it formats said data and adds it to the database depending on the role of the person.

In the case of this app, roles consist of simple `strings` instead of possible `enums`.
This design choice is explained by the later usage of the `GUI` interface by the users and not the functions themselves directly and the relatively small size of the project so the introduction of the `enums` didn't seem necessary.

No verification of the data (number of characters, email format) has been implemented in this version but it could be implemented in the future.

#### The `filter_mentees` function

This function takes the `list of mentees` as an input and the specified `language`.
It then creates a filtered list of mentees that have the same `language` value and returns it.
