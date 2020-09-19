import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
# Edited to check if an entry with same name already exists and provide an appropriate response via dict.
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return {
            "entry": f'A page already exists for "{title}."',
            "name": "ERROR"
        }
    else:
        default_storage.save(filename, ContentFile(content))
        return {
            "entry": get_entry(title).get('content'),
            "name": title
        }

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
# Edited to return python dict including encyclopedia entry and an 'ExactMatch' flag.
    try:
        f = default_storage.open(f"entries/{title}.md").read().decode("utf-8")
        return {'content': f, 'ExactMatch': True}
    except FileNotFoundError:
        return {'content': "ERROR: The requested page was not found.", 'ExactMatch': False}

def overwrite_entry(name, content):
# This function allows the client to overwrite an existing entry with info submited from edit.html.
    filename = f"entries/{name}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
    else:
        return 'File Not Found'
