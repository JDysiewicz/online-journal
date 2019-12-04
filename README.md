# online-journal

This is an online journal for my CS50 final project, based on the CS50 Finance assignment. This utilises Flask as a back-end (micro)framework, and sqlite3 for managing the databases containing user accounts and their entries. This allows users to register for an account, login, see their previous entries ordered reverse chronologically, and write new entries in a ckeditor WYSIWYG rich text editor.

## Future Ideas
- Add day/night mode
- Folders for entries
- Make the time dynamic on the page
- Customisable display
- Name the project and design a logo?

## Known Issues
- After regiestering, users must log out before being able to write entires, else be faced with a 500 error. As a temp solution, after registering users are automatically logged out and taken to the login screen - however this is not very UX friendly.

- List artifacts (bullet points, numbers...) are left aligned in the "previous entries" section, however the text is center aligned.