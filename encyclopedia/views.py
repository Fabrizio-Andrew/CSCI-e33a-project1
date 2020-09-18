from django.shortcuts import render
from . import util
import re
from django.core.files.storage import default_storage


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# This function takes the name from the url string, invokes the Entry.html format, and requests the specific entry from a python dict returned by util.get_entry.
def title(request, name):
    x = util.get_entry(name)
    return render(request, "encyclopedia/Entry.html", {
        "entry": x.get('content'),
        "name": name
    })

# This function supports the search feature.  It determines if an exact match exists via an "ExactMatch" value I added to util.get_entry.
# If an exact match exists, the function directs client to that entry.  If client search query only matches a substring, it provides a list of those results.
# TO-DO: Gracefully manage situation with 0 results.
def search(request):
    keyword = request.POST['q']
    if util.get_entry(keyword).get('ExactMatch') == True: # Check for match
        return render(request, "encyclopedia/entry.html", { # Get the entry html template
            "entry": util.get_entry(keyword).get('content'), # Get entry text from util.views dict.
            "name": keyword
        })
    else:
        results = []
        for entry in util.list_entries(): # cycles through util.list_entries().
            if re.search(keyword, entry, re.IGNORECASE):  # Looks for 'q' substring
                results.append(entry)  # if substring found, adds to results list
        return render(request, "encyclopedia/results.html", {
            "results": results
            })

# This function just catches the redirect from urls.py and renders the create.html page.
def create(request):
    return render(request, "encyclopedia/create.html")

# This function calls util.save_entry and renders the results in an Entry.html template.
# util.save_entry runs the check to see if the entry exists.
def new(request):
    response = util.save_entry(request.POST['title'], request.POST['content'])
    return render(request, "encyclopedia/Entry.html", {
        "entry": response.get("entry"),
        "name": response.get("name")
        })
