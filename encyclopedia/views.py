from django.shortcuts import render
from . import util
import re

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# This function takes the name from the url string, invokes the Entry.html format, and requests the specific entry.
def title(request, name):
    return render(request, "encyclopedia/Entry.html", {
        "entry": util.get_entry(name),
        "name": name
    })

# This function supports the search feature.  If an exact match exists, it directs client to that entry.  If only partial match(es) exist, it provides a list of those results.
# TO-DO: Gracefully manage situation with 0 results.
# TO-DO: Make results lists into hyperlinks to entry pages.
def search(request):
    keyword = request.POST['q']
    x = util.get_entry(keyword)
    if x == "The requested page was not found":
        results = []
        for entry in util.list_entries():
            if re.search(keyword, entry, re.IGNORECASE):
        return render(request, "encyclopedia/results.html", {
            "results": results
        })
    else:
        return render(request, "encyclopedia/Entry.html", {
            "entry": util.get_entry(keyword),
            "name": keyword
        })


# THIS IS THE BETTER WAY
#def search(request):
#    try:
#        f = default_storage.open(f"entries/{title}.md")
#        return f.read().decode("utf-8")
#    except FileNotFoundError:
#        results = []
#        for entry in util.list_entries():
#            if re.search(keyword, entry, re.IGNORECASE):
#        return render(request, "encyclopedia/results.html", {
#            "results": results
#        })

#        return "The requested page was not found"
