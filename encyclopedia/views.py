import re
import random
from django.shortcuts import render
import markdown2
from . import util


def index(request):
    """
    Renders the index.html page with listing of entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, name):
    """
    Takes the name from the url string, invokes the Entry.html format,
    and requests the specific entry from a python dict returned
    by util.get_entry.
    """
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(util.get_entry(name).get('content')),
        "name": util.get_entry(name).get('name')
    })


def search(request):
    """
    This function supports the search feature.  It determines if an exact match
    exists via an "ExactMatch" value in util.get_entry.
    """
    keyword = request.POST['q']
    if util.get_entry(keyword).get('ExactMatch') is True:
        """
        If an exact match exists, the function directs client to that entry.
        """
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(keyword).get('content')),
            "name": keyword
        })
    """
    If client search query is not an exact match, results.html is rendered with
    a list of substring match results.
    """
    results = []
    for entry in util.list_entries():
        if re.search(keyword, entry, re.IGNORECASE):
            results.append(entry)
    return render(request, "encyclopedia/results.html", {
        "results": results
    })


def create(request):
    """
    This function just catches a redirect from urls.py and renders
    the create.html page.
    """
    return render(request, "encyclopedia/create.html")


def save(request):
    """
    Calls util.save_entry and renders the results in an Entry.html template.
    util.save_entry runs the check to see if the entry already exists.
    """
    name = request.POST['title']
    submission = util.save_entry(name, request.POST['content'])
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(submission.get('entry')),
        "name": submission.get('name')
        })


def edit(request):
    """
    Calls util.get_entry and prefills the entry onto the textarea at edit.html.
    """
    name = request.GET['name']
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(name).get('content'),
        "name": name
    })


def overwrite(request):
    """
    Calls util.overwrite_entry to save the client's updated data from edit.html
    over the existing file. Next, it calls util.get_entry to serve the
    newly-updated entry content to the Entry.html template.
    """
    name = request.POST['name']
    content = request.POST['content']
    util.overwrite_entry(name, content)
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(util.get_entry(name).get('content')),
        "name": name
        })


def random_page(request):
    """
    Selects a random entry from util.list_entries and serves the content
    to the entry.html template.
    """
    name = random.choice(util.list_entries())
    return render(request, "encyclopedia/Entry.html", {
        "entry": markdown2.markdown(util.get_entry(name).get('content')),
        "name": name
        })
