from django.shortcuts import render
from django import forms
from . import util
import markdown2
import random


# The NewEntryForm class is a form that allows users to create new entries
class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Title"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Add Markdown Content"}))
# This class is used to edit the entry
class EditEntryForm(forms.Form):
    edit = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control"}))


def index(request):
    """
    This function takes in a request and returns a response
    
    :param request: The HTTP request that Django received from the user
    :return: A render function.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, entry):
    """
    This is checking if the request method is POST, and if it is, it will take the form data and
    save it to the database else, it takes in a request and an entry, and if the entry exists, it renders the content.html page with
    the entry and content. If the entry does not exist, it renders the error.html page with the title
    and content.
    
    :param request: The HTTP request that we're processing
    :param entry: the entry that the user clicked on to get to the content page
    :return: A dictionary with the content and entry.
    """
    content = util.get_entry(entry)
    if request.method == "POST":
        content = EditEntryForm(request.POST)
        if content.is_valid():
            title = entry
            content = content.cleaned_data["edit"]            
            util.save_entry(title, content)
            content = markdown2.markdown(content)
            return render(request, "encyclopedia/content.html", {
            "content": content,
            "entry": title
            })
    elif content:
        html = markdown2.markdown(content)
        return render(request, "encyclopedia/content.html", {
            "content": html,
            "entry": entry
        })
    else:        
        return render(request, "encyclopedia/error.html",{
            "title": "Page Not Found!",
            "content": "Sorry, the page you requested for does not exist."
        })

def search(request):
    """
    If the user is searching for an entry, it will return the entry if it exists. If the user is
    searching for a topic, it will return a list of all entries that contain the topic
    
    :param request: The HTTP request that we're processing
    :return: A list of matches.
    """
    if request.method == "POST":
        query = request.POST.get("q")
        entries = util.list_entries()
        if query in entries:
            content = util.get_entry(query)            
            html = markdown2.markdown(content)
            return render(request, "encyclopedia/content.html", {
                "content": html,
                "entry": query
            })
        else:
            matches = []
            for entry in entries:
                if query.lower() in entry.lower():
                    matches.append(entry)
            return render(request, "encyclopedia/search.html", {
                "matches": matches,
                "query": query
            })

def new_entry(request):
    """
    This function is called when the user clicks the "New Entry" button on the main page. It checks to
    see if the user has submitted a form. If so, it checks to see if the form is valid. If so, it saves
    the entry
    
    :param request: The HTTP request that we're processing
    :return: A form.
    """
    if request.method == "POST":
        entries = util.list_entries()
        entry = NewEntryForm(request.POST)
        if entry.is_valid():
            title = entry.cleaned_data["title"]
            content = entry.cleaned_data["content"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                "title": "Page Already Exists!",
                "content": "Sorry, this wiki entry already exists."
                })
            else:
                util.save_entry(title, content)
                content = markdown2.markdown(content)
                return render(request, "encyclopedia/content.html", {
                "content": content,
                "entry": title
                })
    else:
        return render(request, "encyclopedia/entry.html", {
        "form": NewEntryForm().as_p()
        })

def edit(request, entry):
    """
    This function renders the edit.html page with the form filled out with the content of the entry
    
    :param request: The HTTP request that Django received from the user
    :param entry: The entry that we want to edit
    :return: The form with the content of the entry.
    """
    content = util.get_entry(entry)
    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(initial={"edit": content}),
        "entry": entry
    })

def rand(request):
    """
    This function takes a random entry from the list of entries and returns the content of that entry.
    
    :param request: The HTTP request that Django received from the user
    :return: A random entry from the list of entries.
    """
    entries = util.list_entries()
    lucky = random.choice(entries)
    content = markdown2.markdown(util.get_entry(lucky))
    return render(request, "encyclopedia/content.html", {
        "content": content,
        "entry": lucky
    })