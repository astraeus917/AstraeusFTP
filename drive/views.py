# Imports padrão do django
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

# Imports usados no gerenciamento dos aquivos
import io, zipfile
from django.http import HttpResponse, FileResponse

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
        if request.POST.get('form_type') == 'upload_form':
            file_list = request.FILES.getlist('file_list')
            count_files = []

            if not file_list:
                messages.info(request, "Não existem arquivos para upload!")
            try:
                for file_obj in file_list:
                    # Obtem o tamanho do arquivo em bytes e depois em mb
                    size_bytes = file_obj.size
                    size_mb = round(size_bytes / (1024 * 1024), 2)

                    # Adiciona o arquivo no Banco de Dados
                    save_file, created = File.objects.objects(
                        file = file_obj,
                        file_name = file_obj,
                        size = size_mb,
                    ) 

                    count_files.append(file_obj)

                    if created:
                        save_file.owner = None
                        save_file.save()
                
                if len(count_files) >= 1:
                    messages.success(request, f"{len(count_files)} arquivo(s) salvo(s) com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro: {e}")

        if request.POST.get('form_type') == 'download_form':
            id_list = request.POST.getlist('files')
            if not id_list:
                messages.info(request, "Nenhum arquivo foi selecionado para Download!")
            
            else:
                file_list = File.objects.filter(id__in=id_list)
                if not file_list.exists():
                    messages.error(request, "Nenhum arquivo foi encontrado!")
        
                elif len(id_list) > 1:
                    # Cria um buffer de memória para o .zip
                    buffer = io.BytesIO()
                    
                    try:
                        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for file_obj in file_list:

                                save_file = file_obj.file_name or f"file_{file_obj.id}.ext"
                                zip_file.write(file_obj.file.path, arcname=save_file)

                        buffer.seek(0)

                        response = HttpResponse(buffer, content_type='application/zip')
                        response['Content-Disposition'] = 'attachment; filename="AstraeusFTP.zip"'
                        return response
                    
                    except Exception as e:
                        messages.error(request, f"Erro: {e}")

                else:
                    try:
                        file_obj = file_list[0]
                        file_path = file_obj.file.path
                        with open(file_path, 'rb') as f:
                            return FileResponse(f, as_attachment=True, filename=file_obj.file.name)

                    except Exception as e:
                        messages.error(request, f"Erro: {e}")

    return render(request, 'drive/home.html', context)
