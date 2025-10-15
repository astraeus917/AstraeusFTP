from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

# Imports usados no gerenciamento dos aquivos
from django.utils.text import get_valid_filename
from django.core.files.storage import FileSystemStorage
import os

# Modelos do Banco de Dados
from .models import File


def drive(request):
    """
    View da página principal do sistema
    E tratamento das funções do sistema
    """
    # Pega todos os aquivos do Banco de Dados
    all_files = File.objects.all()
    context = {
        'all_files': all_files,
    }

    # Tratamento do envio de formulários
    if request.method == 'POST':

        # Upload de arquivos
        if request.POST.get('form_type') == 'upload_form' and request.FILES.getlist('files'):
            try:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/uploads/')
                count_files = []

                for file in request.FILES.getlist('files'):
                    # Nome e estensão
                    safe_name, ext = os.path.splitext(get_valid_filename(file.name))
                    ext = ext.lower()
                    
                    # Tamanho do arquivo e conversão para MB
                    size_bytes = file.size
                    size_mb = round(size_bytes / (1024 * 1024), 2)

                    # Salva o arquivo na pasta de midias do sistema
                    filename = fs.save(file.name, file)
                    path = fs.path(filename)
                    count_files.append(filename) # lista de arquivos enviados

                    # Adiciona o arquivo ao Banco de Dados
                    save_file, created = File.objects.update_or_create(
                        file_name = filename,
                        # ext = ext,
                        size = size_mb,
                        path = path,
                    )

                    # Se o arquivo for criado, ele seta owner para None, por enquanto
                    if created:
                        save_file.owner = None
                        save_file.save()
                
                # Mensagem de sucesso do upload dos arquivos
                messages.success(request, f"{len(count_files)} arquivo(s) salvo(s) com sucesso!")

            # Mensagens de erros
            except Exception as e:
                messages.error(request, f'Erro: {e}')

        else:
            messages.error(request, "Nenhum arquivo foi enviado!")

    return render(request, 'drive/home.html', context)

