from django.shortcuts import render

def drive(request):
    """View da página principal do sistema"""

    return render(request, 'drive/home.html')
