# Imports padrão do django
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

# Imports usados no gerenciamento dos aquivos
import os
from django.utils.text import get_valid_filename
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse, Http404

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
                count_files = []

                for f in request.FILES.getlist('files'):
                    # Nome e estensão
                    safe_name, ext = os.path.splitext(get_valid_filename(f.name))
                    ext = ext.lower()
                    
                    # Tamanho do arquivo e conversão para MB
                    size_bytes = f.size
                    size_mb = round(size_bytes / (1024 * 1024), 2)

                    # Adiciona o arquivo ao Banco de Dados
                    save_file, created = File.objects.update_or_create(
                        file = f,
                        file_name = f,
                        # ext = ext,
                        size = size_mb,
                    )

                    count_files.append(f) # lista de arquivos enviados

                    # Se o arquivo for criado, ele seta owner para None, por enquanto
                    if created:
                        save_file.owner = None
                        save_file.save()
                
                # Mensagem de sucesso do upload dos arquivos
                messages.success(request, f"{len(count_files)} arquivo(s) salvo(s) com sucesso!")

            # Mensagens de erros
            except Exception as e:
                messages.error(request, f'Erro: {e}')

        # Download do arquivo selecionado
        elif request.POST.get('form_type') == 'download_form':
            try:
                file_id = request.POST.get('file_id')
                get_file = get_object_or_404(File, id=file_id)
                file_path = get_file.file.path

                if os.path.exists(file_path):
                    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=get_file.file.name)

                else:
                    raise Http404("Não foi possível encontrar o arquivo!")

            except Exception as e:
                messages.error(request, F"Erro: {e}")

        # Deleta o arquivo selecionado
        elif request.POST.get('form_type') == 'delete_form':
            try:
                file_id = request.POST.get('file_id')
                get_file = get_object_or_404(File, id=file_id)
                get_file.file.delete()
                get_file.delete()
                messages.success(request, "Arquivo deletado com sucesso!")
            
            except Exception as e:
                messages.error(request, f"Erro: {e}")

        else:
            messages.error(request, "Nenhuma requisição foi solicitada!")

    return render(request, 'drive/home.html', context)

