from django.shortcuts import render


def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html with the data in the context variable
    print("AAAAAAAAAAAAAAAAAA")
    return render(request, "index.html")
