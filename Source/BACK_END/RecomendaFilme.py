import requests
import json
import unidecode
from os import walk

def compatibilidade():
    id = 101
    l1 = ['v', 'e', 'l', 'o', 'z', 'e', 's', 'e', 'f', 'u', 'r', 'i', 'o', 's', 'o', 's', '8']
    l2 = ['v', 'e', 'l', 'o', 'z', 'e', 's', 'f', 'u', 'r', 'i', 'o', 's', 'o', 's', '8']
    vetor, lista = l1, l2
    t1 = len(vetor)
    t2 = len(lista)
    #print(vetor)
    #print(lista)
    #print(t1, t2)
    if t1 == t2:
        for indice, vl in enumerate(vetor):
            if vetor[indice] != lista[indice]:
                break
            else:
                return id
    else:
        contador = 0
        aux = []
        if t1 > t2:
            for l in lista:
                print(lista.count(l))
                if l == vetor[contador]:
                    contador += 1
            if contador >= len(lista) // 2:
                return id
        else:
            for v in vetor:
                if v == lista[contador]:
                    contador += 1
            if contador >= len(vetor) // 2:
                return id
    return False

def comparar_string(strings, filme):
    print(strings)
    print(filme)
    string = unidecode.unidecode(filme[0])
    vetor = [letra.lower() for letra in string if letra.isalnum() == True]
    for id, jsonn in enumerate(strings):
        #print(jsonn)
        for chave, valor in jsonn.items():
            if chave == 'release_date':
                if valor[:4] != filme[1]:
                    break
            if chave == 'overview':
                if valor == '':
                    break
            if chave == 'title':
                valor = unidecode.unidecode(valor)
                lista = [letra.lower() for letra in valor if letra.isalnum() == True]
                t1 = len(vetor)
                t2 = len(lista)
                #print(vetor,t1)
                #print(lista,t2)
                if t1 == t2:
                    for indice, vl in enumerate(vetor):
                        if vetor[indice] != lista[indice]:
                            break
                        else:
                            return id
                else:
                    contador = 0
                    if t1 > t2:
                        for l in lista:
                            if l == vetor[contador]:
                                contador += 1
                        if contador >= (t1 // 2)-1:
                            return id
                    else:
                        for v in vetor:
                            if v == lista[contador]:
                                contador += 1
                        if contador >= (t2 // 2)-1:
                            return id
    return False

def informacoes(arquivo, ano=True):
    API_KEY = '9ccf9fd2aaa2811eabe3d8060d4b6e9f'
    filme = arquivo.split(' (')
    filme[1] = filme[1][:4]
    if ano:
        response = requests.get(
            f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page=1&year={filme[1]}')
    else:
        response = requests.get(
            f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page=1')
    titulo, data, genero, sinopse, imgURL = '','','','',''
    if response.ok:
        resposta = response.json()
        if len(resposta['results']) == 0:
            print('Filme não Encontrado')
        print(len(resposta))
        indice = comparar_string(resposta['results'], filme)
        data = resposta['results'][indice]['release_date']
        titulo = resposta['results'][indice]['title']
        genero = generos(resposta['results'][indice]['genre_ids'])
        sinopse = resposta['results'][indice]['overview']
        imgURL = 'http://image.tmdb.org/t/p/w500' + resposta['results'][indice]['poster_path']
        return [titulo, genero, data, sinopse, imgURL]

def informacoes2(arquivo, ano=True,pagina=1):
    API_KEY = '9ccf9fd2aaa2811eabe3d8060d4b6e9f'
    filme = arquivo.split(' (')
    filme[1] = filme[1][:4]
    if ano:
        response = requests.get(
            f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page={pagina}&year={filme[1]}')
    else:
        response = requests.get(
            f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page={pagina}')
    titulo, data, genero, sinopse, imgURL = '','','','',''
    if response.ok:
        resposta = response.json()
        tamanho = resposta['total_results']
        if tamanho <= 0:
            print('Filme não Encontrado')
        elif tamanho == 1:
            data = resposta['results'][0]['release_date']
            titulo = resposta['results'][0]['title']
            genero = generos(resposta['results'][0]['genre_ids'])
            sinopse = resposta['results'][0]['overview']
            imgURL = 'http://image.tmdb.org/t/p/w500' + resposta['results'][0]['poster_path'] if resposta['results'][0]['poster_path'] != None else None
            return [titulo, genero, data, sinopse, imgURL]
        else:
            lista = []
            if tamanho > 20:
                inicio = 0
                while (tamanho - inicio) > 0:
                    fim = inicio+20 if (tamanho > inicio+20) else tamanho
                    for indice in range(inicio,fim):
                        try:
                            data = resposta['results'][indice]['release_date']
                        except:
                            print(indice,'data')
                            data = 'null'
                        try:
                            titulo = resposta['results'][indice]['title']
                        except:
                            print(indice,fim,'\n')
                            print(len(resposta['results']))
                            exit()
                        genero = generos(resposta['results'][indice]['genre_ids'])
                        sinopse = resposta['results'][indice]['overview']
                        imgURL = 'http://image.tmdb.org/t/p/w500' + resposta['results'][indice]['poster_path'] if resposta['results'][indice]['poster_path'] != None else None
                        lista.append([titulo, genero, data, sinopse, imgURL])
                    inicio+=20
            else:
                for indice in range(tamanho):
                    data = resposta['results'][indice]['release_date']
                    titulo = resposta['results'][indice]['title']
                    genero = generos(resposta['results'][indice]['genre_ids'])
                    sinopse = resposta['results'][indice]['overview']
                    imgURL = 'http://image.tmdb.org/t/p/w500' + resposta['results'][indice]['poster_path'] if resposta['results'][indice]['poster_path'] != None else None
                    lista.append([titulo, genero, data, sinopse, imgURL])
        return lista

def informacoes3(arquivo):
    API_KEY = '9ccf9fd2aaa2811eabe3d8060d4b6e9f'
    filme = arquivo.split(' (')
    filme[1] = filme[1][:4]
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page=1&year={filme[1]}')
    if response.ok:
        resposta = response.json()
        tamanho = resposta['total_pages']
        if tamanho <= 0:
            return 'Filme não Encontrado'
        elif tamanho == 1:
            lista = []
            fim = resposta['total_results']
            for indice in range(fim):
                id = resposta['results'][indice]['id']
                data = resposta['results'][indice]['release_date']
                titulo = resposta['results'][indice]['title']
                genero = generos(resposta['results'][indice]['genre_ids'])
                sinopse = resposta['results'][indice]['overview']
                imgURL = 'http://image.tmdb.org/t/p/w500' + resposta['results'][indice]['poster_path'] if \
                    resposta['results'][indice]['poster_path'] != None else 'None'
                lista.append([titulo, genero, data, sinopse, imgURL, id])
            return lista
        else:
            lista = []
            pagina = 1
            while True:
                if response.ok:
                    tam = len(resposta['results'])%20 if pagina == tamanho else 20
                    for indice in range(tam):
                        try:
                            id = resposta['results'][indice]['id']
                        except:
                            print(indice)
                            print(resposta)
                            exit()
                        data = resposta['results'][indice]['release_date']
                        titulo = resposta['results'][indice]['title']
                        genero = generos(resposta['results'][indice]['genre_ids'])
                        sinopse = resposta['results'][indice]['overview']
                        imgURL = 'http://image.tmdb.org/t/p/w500' + resposta['results'][indice]['poster_path'] if \
                            resposta['results'][indice]['poster_path'] != None else 'None'
                        lista.append([titulo, genero, data, sinopse, imgURL, id])
                else:
                    return 'ERRO'

                if pagina >= tamanho:
                    return lista
                elif pagina < tamanho:
                    pagina+=1

                response = requests.get(
                    f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page={pagina}&year={filme[1]}')
                resposta = response.json()

def generos(ids):
    with open("BACK_END/generos.json", encoding='utf-8') as meu_json:
        genero = json.load(meu_json)
    juncao = ''
    for i in ids:
        juncao+=genero[str(i)]+'/'
    #print('GENERO = ',juncao[:-1])
    return juncao[:-1]

if __name__ == '__main__':
    arquivo = 'Capitão América - O Primeiro Vingador (2011)'
    arquivo2 = 'Mortal (2021)'
    #arquivo5 = 'Que Família é Essa (2021)'
    #comparar_string2(arquivo1,arquivo2,arquivo3)
    #print(informacoes(arquivo))
    lista = informacoes3(arquivo2)
    for i in lista:
        for j in i:
            print(j)
        print('-'*100)
    #print(compatibilidade())
    """
    filmes = verificar_arquivos(r'D:\Filmes')
    cont = 0
    for filme in filmes:
        erro = informacoes(filme)
        for valor in erro:
            if valor == '':
                print('erro no filme =',filme)
                break
        else:
            cont+=1
        print(cont)
    """
"""
        for indice in range(len(resposta['results'])):
            #print(resposta['results'][indice])
            if len(resposta['results'][indice]['genre_ids']) <= 0 or resposta['results'][indice]['overview'] == ''\
                    or resposta['results'][indice]['poster_path'] == '' or type(resposta['results'][indice]['poster_path']) == None:
                continue
            data = resposta['results'][indice]['release_date']
            if data[:4] != filme[1]:
                continue
            titulo = resposta['results'][indice]['title']
            if titulo != filme[0]:
                continue
            #print('ID = ', resposta['results'][indice]['id'])
            genero = generos(resposta['results'][indice]['genre_ids'])
            sinopse = resposta['results'][indice]['overview']
            imgURL = 'http://image.tmdb.org/t/p/w500'+resposta['results'][indice]['poster_path']
            return [titulo,genero,data,sinopse,imgURL]

    return [titulo,genero,data,sinopse,imgURL]

if response.ok:
    resposta = response.json()
    for indice in range(len(resposta['results'])):
        if len(resposta['results'][indice]['genre_ids']) <= 0 or resposta['results'][indice]['overview'] == '':
            continue
        print('ID = ',resposta['results'][indice]['id'])
        print('TITULO = ',resposta['results'][indice]['title'])
        generos(resposta['results'][indice]['genre_ids'])
        print('DATA = ',resposta['results'][indice]['release_date'])
        print('SINOPSE = ', resposta['results'][indice]['overview'])
        print('IMAGEM = ', resposta['results'][indice]['poster_path'])
        url = f"https://image.tmdb.org/t/p/original{resposta['results'][indice]['poster_path']}"
        
        with open('teste.jpg', 'wb') as imagem:
            respost = requests.get(url, stream=True)

            if not respost.ok:
                print("Ocorreu um erro, status:", respost.status_code)
            else:
                for dado in respost.iter_content(1024):
                    if not dado:
                        break

                    imagem.write(dado)

                print("Imagem salva! =)")
"""