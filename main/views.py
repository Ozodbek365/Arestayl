from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'index.html')
        return render(request, 'index-unauth.html')