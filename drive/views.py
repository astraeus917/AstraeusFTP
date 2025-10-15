from django.shortcuts import render
from django.utils.text import get_valid_filename
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
import uuid, os

def drive(request):
    """
    View da página principal do sistema
    E tratamento das funções do sistema
    """

    # Tratamento do upload de arquivos
    if request.method == 'POST':
        if request.POST.get('form_type') == 'upload_form' and request.FILES.getlist('files'):
            try:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/uploads/')
                saved_files = []

                for file in request.FILES.getlist('files'):
                    # # Gera um nome seguro para salvar o arquivo
                    # name, ext = os.path.splitext(get_valid_filename(file.name))
                    # unique_name = f'{name}_{uuid.uuid4().hex}{ext}'

                    safe_name = get_valid_filename(file.name)
                    filename = fs.save(safe_name, file)
                    saved_files.append(filename)

                messages.success(request, f"{len(saved_files)} arquivo(s) salvo(s) com sucesso!")
            except Exception as e:
                messages.error(request, f'Erro: {e}')
        
        else:
            messages.error(request, "Nenhum arquivo foi enviado!")

    return render(request, 'drive/home.html')

