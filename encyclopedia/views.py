from django.shortcuts import render
from . import util
import re
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
# This function takes the name from the url string, invokes the Entry.html format, and requests the specific entry from a python dict returned by util.get_entry.
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(util.get_entry(name).get('content')),
        "name": name
    })

def search(request):
# This function supports the search feature.  It determines if an exact match exists via an "ExactMatch" value I added to util.get_entry.
# If an exact match exists, the function directs client to that entry.  If client search query only matches a substring, it provides a list of those results.
# TO-DO: Gracefully manage situation with 0 results.
    keyword = request.POST['q']
    if util.get_entry(keyword).get('ExactMatch') == True:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(keyword).get('content')),
            "name": keyword
        })
    else:
        results = []
        for entry in util.list_entries():
            if re.search(keyword, entry, re.IGNORECASE):
                results.append(entry)
        return render(request, "encyclopedia/results.html", {
            "results": results
            })

def create(request):
# This function just catches the redirect from urls.py and renders the create.html page.
    return render(request, "encyclopedia/create.html")


#TO-DO: Work on this error handling...
def new(request):
# This function calls util.save_entry and renders the results in an Entry.html template.
# util.save_entry runs the check to see if the entry already exists.
    name = request.POST['title']
    submission = util.create_entry(name, request.POST['content'])
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(submission.get('entry')),
        "name": name
        })

def edit(request):
# This function calls util.get_entry and serves the entry to the pre-filled field on edit.html.
    name = request.GET['name']
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(name).get('content'),
        "name": name
    })

def overwrite(request):
# This function calls util.overwrite_entry to save the client's data from edit.html over the existing file.
# Next, it calls util.get_entry to serve the newly-saved entry content to the Entry.html template.
    name = request.POST['name']
    content = request.POST['content']
    util.overwrite_entry(name, content)
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(util.get_entry(name).get('content')),
        "name": name
        })

def random_page(request):
# This function selects a random entry from util.list_entries and serves the content to the entry.html template.
    name= random.choice(util.list_entries())
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(util.get_entry(name).get('content')),
        "name": name
        })
