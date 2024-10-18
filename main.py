from PIL import Image
from PIL.ExifTags import TAGS
import os
import glob
import datetime
import shutil

# Define o caminho para a pasta e o padrão de arquivos
folder_path = './img/whatsapp/*'

# Recupera todos os arquivos correspondentes ao padrão
files = glob.glob(folder_path)

count = 0
count_error = 0
error_files = []

for f in files:
    image = Image.open(f)
    exifdata = image.getexif()
    
    try:
        count += 1
        ano = exifdata[306].split(":")[0]
        mes = exifdata[306].split(":")[1]
        dia = exifdata[306].split(":")[2][0:2] # Pega os dois primeiros caracteres
        print(f"Data da foto: {dia}/{mes}/{ano}")

        # Caminho para a nova pasta
        new_folder_path = f'./sorted_images/{ano}/{mes}'

        os.makedirs(f'sorted_images', exist_ok=True)
        os.makedirs(f'sorted_images/{ano}', exist_ok=True)
        os.makedirs(f'sorted_images/{ano}/{mes}', exist_ok=True)

        # Cria a nova pasta, se ela não existir
        os.makedirs(new_folder_path, exist_ok=True)

        # Caminho completo para o novo arquivo
        filename = f.split('/')[-1]
        file_path = os.path.join(new_folder_path, filename)
        image.save(file_path)
     
    except:
        filename = f.split('/')[-1]
        # metadata = {}
        # metadata['filename'] = filename
        # for tagid in exifdata:
     
        #     # getting the tag name instead of tag id
        #     tagname = TAGS.get(tagid, tagid)
        
        #     # passing the tagid to get its respective value
        #     value = exifdata.get(tagid)
            
        #     metadata[tagname] = value
        

        # count_error += 1
        error_files.append(filename)
        # print('Não foi possível recuperar a data da imagem')
        # print (f'Arquivo {filename} não foi movido')
        continue


for f in error_files:

    try:

        imgPath = f'./img/whatsapp/{f}'
        file_info = os.stat(imgPath)

        creation_time = datetime.datetime.fromtimestamp(file_info.st_mtime)

        mes = creation_time.month
        ano = creation_time.year    
        dia = creation_time.day

        print(f"Data da foto #2: {dia}/{mes}/{ano}")


        # Caminho para a nova pasta
        new_folder_path = f'./sorted_images_err/{ano}/{mes}'

        os.makedirs(f'sorted_images_err', exist_ok=True)
        os.makedirs(f'sorted_images_err/{ano}', exist_ok=True)
        os.makedirs(f'sorted_images_err/{ano}/{mes}', exist_ok=True)

        # Cria a nova pasta, se ela não existir
        os.makedirs(new_folder_path, exist_ok=True)

        source_path = f'./img/whatsapp/{f}'
        destination_path = os.path.join(new_folder_path, f)

        shutil.copy(source_path, destination_path)
    except:
        print(f"Erro remanejar arquivo {f}")

file_path = './error-log.txt'

# Abre o arquivo em modo de escrita
with open(file_path, 'w') as file:
    # Itera sobre os itens da lista
    for f in error_files:
        # Escreve cada item no arquivo seguido por uma nova linha
        file.write(f + '\n')


print(f'Foram movidos {count} arquivos')
print(f'Não foi possível recuperar a data de {count_error} arquivos')