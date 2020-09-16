from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#This function takes the name from the url string, invokes the Entry.html format, and requests the specific entry.
def Title(request, name):
    return render(request, "encyclopedia/Entry.html", {
        "entry": util.get_entry(name),
        "name": name
    })
