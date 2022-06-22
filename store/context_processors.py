
from .forms import SearchForm
def search(request):
    search_form = SearchForm
    if request.method =='POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_form.save()
    return{'search_form':search_form}