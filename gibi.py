import img2pdf
from PIL import Image
import sys
from math import ceil
from os import listdir, rename, mkdir, rmdir
from os.path import isfile, join, exists, splitext, basename, dirname
from shutil import rmtree


IGUALAR = True
PAGINAS_DUPLAS = False
NOVA_PASTA = '_pdf'


def getListaImagens(pasta):
  # Lista de arquivos na pasta
  
  arquivos = [join(pasta,f) for f in listdir(pasta) if isfile(join(pasta, f))]
  imagens = list()
  for a in arquivos:
    if splitext(a)[1] not in ['.png', '.jpg', '.jpeg']:
        continue
    imagens.append(Image.open(a))
  return imagens
    
def separarImagem(original, linhas=1, colunas=1):
    partesDaImagem = list()
    largura, altura = original.size
    pasta = dirname(original.filename)
    nomeArquivo = original.filename
    i_extensao = nomeArquivo.rfind(".")
    alturaParte = altura//linhas
    larguraParte = largura//colunas

    y = 0
    l = 0
    # Percorre no seguinte sentido
    #   1 2 3
    #   4 5 6
    #   7 8 9
    while y <= altura - alturaParte:
        x = 0
        c = 0
        while x <= largura - larguraParte:
            i = original.copy()
            i = i.crop((x, y, x + larguraParte, y + alturaParte))
            # Nomeia as partes
            i.filename = nomeArquivo[:i_extensao] + '-' + str(l) + str(c) + nomeArquivo[i_extensao:]
            #print(i.filename)
            partesDaImagem.append(i)
            
            x += larguraParte
            c += 1
        y += alturaParte
        l += 1

    return partesDaImagem

def separarPaginasMultiplas(listaImagens):
    menorLargura = 0
    menorAltura = 0
    
    print('\n' + '~~'*15)
    print(f'Verificando {len(listaImagens)} paginas: ', end='')
    # Percorre toda a lista para descobrir qual o menor tamanho
    for i in range(len(listaImagens)):
        if i == 0:
            menorLargura, menorAltura = listaImagens[i].size
        
        larguraAtual, alturaAtual = listaImagens[i].size
        
        if(larguraAtual < menorLargura):
            menorLargura = larguraAtual
        if(alturaAtual < menorAltura):
            menorAltura = alturaAtual
    print('OK')
    
    # Percorre novamente para separar as páginas
    print('Recortanto... ')
    listaRecortada = list()
    for i in range(len(listaImagens)):
        larguraAtual, alturaAtual = listaImagens[i].size
        
        numColunas = round(larguraAtual / menorLargura)
        numLinhas = round(alturaAtual / menorAltura)

        if numColunas <= 1 and numLinhas <= 1:
            listaRecortada.append(listaImagens[i])
        else:
            #print(f'Separando pagina {i} em {numLinhas} linhas e {numColunas} colunas')
            listaRecortada += separarImagem(listaImagens[i], numLinhas, numColunas)
    print('OK')
    print(f'Total de {len(listaRecortada)} paginas')
    
    if IGUALAR == False:
        return listaRecortada
    else:
        print('Igualhando tamanhos: ', end='')
        # Percorre pela terceira vez para deixar todas as imagens do mesmo tamanho
        listaMesmoTamanho = list()
        for i in listaRecortada:
            im = i.crop((0, 0, menorLargura, menorAltura))
            im.filename = i.filename
            listaMesmoTamanho.append(im)
        print(f'({menorLargura}x{menorAltura}) OK')
            
        return listaMesmoTamanho

def separarPaginasDuplas(listaImagens):
    metadeDaLargura = listaImagens[0].size
    
    # Gera uma lista de meias imagens
    listaMetades = list()
    for i in listaImagens:
        listaMetades += separarImagem(i, 1, 2) # uma linha, duas colunas
            
    return listaMetades

def salvarImagens(listaImagens, pastaEntrada, novaPasta):
    #i_pasta = listaImagens[0].filename.rfind('\\')
    #pastaDasImagens = listaImagens[0].filename[:i_pasta+1]
    #pastaCriada = pastaDasImagens + nomePasta + '\\'
    novaPasta = join(pastaEntrada, novaPasta)
    
    print('\n' + '~~'*15)
    print(f'Salvando {len(listaImagens)} imagens\nDe: \"{pastaEntrada}\"\nEm: \"{novaPasta}\"')
    
    # Remover a pasta se já existir
    if exists(novaPasta):
        rmtree(novaPasta)
    mkdir(novaPasta)
    
    for im in listaImagens:
        #print(f'Salvando {im.filename}')
        im.save(join(novaPasta, basename(im.filename)))
    
    print('OK')

def converterEmPdf(pastaEntrada, pastaSaida):
    # Cria um arquivo pdf usando imagens contidas em pastaEntrada
    # e salva em pastaSaida
    print('\n' + '~~'*15)
    print(f'Gerando pdf')
    print(f'De: {pastaEntrada}')
    print(f'Em: {pastaSaida}\n')
    
    listaImagens = getListaImagens(pastaEntrada)
    nomes = [n.filename for n in listaImagens]

    # O arquivo tem o mesmo nome da pasta
    nomePdf = basename(pastaSaida) + '.pdf'

    print(f'Criando arquivo: {join(pastaSaida, nomePdf)}')
    with open(join(pastaSaida, nomePdf), "wb") as f:
        f.write(img2pdf.convert(nomes))

    print('OK')



pastaAtual = sys.argv[1]


# Somente converte uma pasta de imagens em pdf
if sys.argv[1] == '-p':
    print('Convertendo em pdf')
    pastaAtual = sys.argv[2]
    converterEmPdf(pastaAtual, pastaAtual)
    print('Pronto!')
    exit()
# Separar páginas duplicadas
if sys.argv[1] == '-d':
    print('Paginas duplas')
    PAGINAS_DUPLAS = True
    pastaAtual = sys.argv[2]



a = getListaImagens(pastaAtual)

if PAGINAS_DUPLAS:
    b = separarPaginasDuplas(a)
else:
    b = separarPaginasMultiplas(a)

salvarImagens(b, pastaAtual, NOVA_PASTA)
converterEmPdf(join(pastaAtual, NOVA_PASTA), pastaAtual)