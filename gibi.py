import img2pdf
from PIL import Image
import sys
from os import listdir, rename, mkdir, rmdir
from os.path import isfile, join, exists
from shutil import rmtree

# Lista de arquivos na pasta
pasta = str(sys.argv[1])
arquivos = [join(pasta,f) for f in listdir(pasta) if isfile(join(pasta, f))]
# Renomear aquivos
for i in range(len(arquivos)):
    rename(arquivos[i], join(pasta, '{:0>2d}.jpg'.format(i+1)))



# Abrir as imagens e encontrar a menor das alturas
listaImagens = list()
menorAltura = 0
menorLargura = 0
for i in range(len(arquivos)):
    listaImagens.append(Image.open(arquivos[i]))
    if i == 0:
        menorLargura, menorAltura = listaImagens[i].size

    larguraAtual = listaImagens[i].size[0]
    if(larguraAtual < menorLargura):
        menorLargura = larguraAtual
    alturaAtual = listaImagens[i].size[1]
    if(alturaAtual < menorAltura):
        menorAltura = alturaAtual


# Cortar todas as imagens para ficar da mesma altura
imagensCortadas = list()
for i in listaImagens:
    imagensCortadas.append(i.crop((0, 0, menorLargura, menorAltura)))


# Salvar imagens cortadas numa pasta
pastaCortadas = join(pasta, 'cortadas')

if exists(pastaCortadas):
    rmtree(pastaCortadas)
mkdir(pastaCortadas)

nomeCortadas = list()
for i in range(len(imagensCortadas)):
    nomeCortadas.append('{}\\{:0>2d}.jpg'.format(pastaCortadas, i + 1))
    imagensCortadas[i].save(join(pastaCortadas, nomeCortadas[i]))


for i in nomeCortadas:
    print(i)

# Converter em pdf
quantidade = len(imagensCortadas)
#if quantidade % 4 != 0:
#    print(f'Remova {quantidade % 4} imagem ou adicione {4 - quantidade % 4}')
#else:
with open('final.pdf', "wb") as f:
    f.write(img2pdf.convert(nomeCortadas))

