from django.shortcuts import render
from django import forms
from . import util
import markdown2
import random


class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Title"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Add Markdown Content"}))
class EditEntryForm(forms.Form):
    edit = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, entry):
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
    content = util.get_entry(entry)
    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(initial={"edit": content}),
        "entry": entry
    })

def rand(request):
    entries = util.list_entries()
    lucky = random.choice(entries)
    content = markdown2.markdown(util.get_entry(lucky))
    return render(request, "encyclopedia/content.html", {
        "content": content,
        "entry": lucky
    })