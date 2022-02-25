import sys

if not "{{ cookiecutter.author_name }}":
    print("Error: author_name is required")
    sys.exit(1)

if not "{{ cookiecutter.author_email }}":
    print("Error: author_email is required")
    sys.exit(1)
