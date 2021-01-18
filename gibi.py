import img2pdf
from PIL import Image
import sys
from os import listdir, rename, mkdir, rmdir
from os.path import isfile, join, exists
from shutil import rmtree

def getListaImagens(pasta):
  # Lista de arquivos na pasta
  arquivos = [join(pasta,f) for f in listdir(pasta) if isfile(join(pasta, f))] 
  imagens = list()
  for a in arquivos:
    imagens.append(Image.open(a))
  return imagens
    
def separarImagem(original, linhas=1, colunas=1):
    partesDaImagem = list()
    largura, altura = original.size
    nomeOriginal = original.filename
    i_extensao = original.filename.rfind(".")
    alturaParte = altura//linhas
    larguraParte = largura//colunas

    y = 0
    l = 0
    while y <= altura - alturaParte:
        x = 0
        c = 0
        while x <= largura - larguraParte:
            i = original.copy()
            i = i.crop((x, y, x + larguraParte, y + alturaParte))            
            i.filename = nomeOriginal[:i_extensao] + '-' + str(l) + str(c) + nomeOriginal[i_extensao:]
            partesDaImagem.append(i)
            
            x += larguraParte
            c += 1
        y += alturaParte
        l += 1

    return partesDaImagem

def separarPaginasMultiplas(listaImagens):
    menorLargura = 0
    menorAltura = 0
    
    # Percorre toda a lista para descobrir qual o menor tamanho
    for i in range(len(listaImagens)):
        if i == 0:
            menorLargura, menorAltura = listaImagens[i].size
        
        larguraAtual, alturaAtual = listaImagens[i].size
        
        if(larguraAtual < menorLargura):
            menorLargura = larguraAtual
        if(alturaAtual < menorAltura):
            menorAltura = alturaAtual
    
    # Percorre novamente para separar as páginas
    listaRecortada = list()
    for i in range(len(listaImagens)):
        larguraAtual, alturaAtual = listaImagens[i].size
        
        numPáginasHoriz = larguraAtual // menorLargura
        numPáginasVert = alturaAtual // menorAltura
        
        if numPáginasHoriz <= 1 and numPáginasVert <= 1:
            listaRecortada.append(listaImagens[i])
        else:
            listaRecortada += separarImagem(listaImagens[i], numPáginasVert, numPáginasHoriz)
  
    # Percorre pela terceira vez para deixar todas as imagens do mesmo tamanho
    listaMesmoTamanho = list()
    for i in listaRecortada:
        im = i.crop((0, 0, menorLargura, menorAltura))
        im.filename = i.filename
        listaMesmoTamanho.append(im)
    
    return listaMesmoTamanho

def salvarImagens(listaImagens, nomePasta='final'):
    i_pasta = listaImagens[0].filename.rfind('\\')
    pastaDasImagens = listaImagens[0].filename[:i_pasta+1]
    pastaCriada = pastaDasImagens + nomePasta + '\\'
    print(pastaCriada)
    
    # Remover a pasta se já existir
    if exists(pastaCriada):
        rmtree(pastaCriada)
    mkdir(pastaCriada)
    
    for im in listaImagens:
        im.save(pastaCriada + im.filename[i_pasta+1:])
    
    """for im in listaImagens:

        #print(im.filename[:x+1] + nomePasta + '\\' + im.filename[x+1:])
        im.save(im.filename[:x+1] + nomePasta + '\\' + im.filename[x+1:])
"""

a = getListaImagens(sys.argv[1])
b = separarPaginasMultiplas(a)

salvarImagens(b)


"""
# Converter em pdf
quantidade = len(imagensCortadas)
#if quantidade % 4 != 0:
#    print(f'Remova {quantidade % 4} imagem ou adicione {4 - quantidade % 4}')
#else:
with open('final.pdf', "wb") as f:
    f.write(img2pdf.convert(nomeCortadas))

"""
