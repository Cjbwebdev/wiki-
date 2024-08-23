from django.shortcuts import render
from markdown2 import Markdown
import markdown2
import random

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    markdowner = Markdown()
    return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry '{title}' was not found."
        }, status=404)
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == 'POST':
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        
        if html_content is not None:
            # Exact match found, render the entry page
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            # No exact match found, check for recommendations
            all_entries = util.list_entries()
            recommendations = [entry for entry in all_entries if entry_search.lower() in entry.lower()]
            
            if recommendations:
                # Render recommendations in entry.html
                return render(request, "encyclopedia/entry.html", {
                    "title": "Search Results",
                    "content": f"<p>No exact match found for '{entry_search}'. Did you mean:</p>"
                               + "".join(f"<li><a href='/wiki/{entry}'>{entry}</a></li>" for entry in recommendations)
                })
            else:
                # No recommendations found, render error page
                return render(request, "encyclopedia/error.html", {
                    "message": f"No results found for '{entry_search}'."
                }, status=404)

def new_page(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_page.html")
    
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        
        if titleExist is not None:
            return render(request, 'encyclopedia/error.html', {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = markdown2.markdown(content)
            return render(request, 'encyclopedia/entry.html', {
                'title': title,
                'content': html_content
            })


def random_entry(request):  
    all_entries = util.list_entries()  
    rand_entry = random.choice(all_entries)  
    html_content = convert_md_to_html(rand_entry)

    return render(request, 'encyclopedia/entry.html', {
        'title': rand_entry,
        'content': html_content
    })

    

def edit(request):
    if request.method == 'POST':
        title = request.POST.get('entry_title')
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': content
        })
    else:
        # Handle GET request if needed, e.g., rendering the edit form without any preloaded content
        return render(request, 'encyclopedia/edit.html')

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        
        # Convert the markdown content to HTML
        html_content = (content)
        
        # Render the entry page with the updated content
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': html_content
        })

   