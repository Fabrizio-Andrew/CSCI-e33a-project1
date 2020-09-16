from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def Title(request, name):
#This bit is broken
    return render(request, f"/entries/{name}")
