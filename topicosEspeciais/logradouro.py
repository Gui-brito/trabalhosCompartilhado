import os
import requests
import json
import zipfile
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector import errorcode

inicia = True
admin = False
login = None

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def mensagemBemVindo():
    print('-'*30+'\n'+'-'*30)
    print('-'*10+'Bem vindo!'+'-'*10)

def conexao():
    try:
        cnx = MySQLConnection(host='localhost',database='topicosEspeciais',user='root',password='root')
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro ao conectar Database")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erro Database inexistente")
        else:
            print(err)
        return None

def busca_usuarios():
    cnx = conexao()
    cursor = cnx.cursor()
    cursor.execute("SELECT usuario, senha, user_admin FROM userLogin")
    lista = []
    for (usuario, senha, user_admin) in cursor:
        lista.append({'Login': usuario, 'Senha':senha, "user_admin":user_admin})
    cnx.close()
    return lista

def login():
    global inicia
    global admin
    global login
    ver_login = False
    ver_senha = False
    cnx = conexao()
    if cnx == None:
        inicia = False

    usuario = busca_usuarios()

    #Inicia recebe True para validação OK
    #Inicia recebe False para saida do programa

    while inicia == True:
        print('-'*30+'\n'+'-'*30)
        print('Efetue o login ou '+'-'*12)
        print('digite [0] para sair.'+'-'*9)
        print('-'*30+'\n'+'-'*30)    
        
        login = input('-'*5+"Login: ")

        if login == '0':
            inicia = False
            break

        #Verifica login do usuário
        for i in range(len(usuario)):
            if usuario[i]['Login'] == login:
                ver_login = True
                print('-'*30)
                print('-'*5+"Usuário encontrado"+7*'-')
                print('-'*30)

                #Verifica senha do usuário

                senha = input('-'*5+"Senha: ")
                if usuario[i]['Senha'] != senha:
                    ver_senha = False
                    print('-'*30)
                    print('-'*7+"Senha incorreta"+8*'-')
                    print('-'*30)
                else:
                    ver_senha = True
                    if usuario[i]['user_admin'] == 1:
                        admin = True

        if (ver_login == True) and (ver_senha==True):
            cls()
            print('-'*30+'\n'+'-'*30)
            print('\tValidação OK!')
            print('-'*30+'\n'+'-'*30)
        
            break
        
        else:            
            cls()
            if ver_login == False:
                print('-'*4+'Usuário não encontrado'+'-'*4)
            elif ver_senha == False:
                print('-'*7+'Senha incorreta'+'-'*8)
            else:
                print('Falta informação')

            print('-'*30+'\n'+'-'*30)

def desenhaMenuPrincipal():
    cls()
    print('-'*13+'Menu'+'-'*13)
    print('-'*30+'\n'+'-'*30)
    print('-'*4+'Escolha uma opição abaixo:')
    print('-'*4+'[0] > Sobre')
    print('-'*4+'[1] > Achar endereço')
    print('-'*4+'[2] > Ver histórico da pesquisa')
    print('-'*4+'[3] > Exportar lista')
    print('-'*4+'[4] > Importar lista')
    if(admin==1):
        print('-'*4+'[5] > Adicionar usuario')
        print('-'*4+'[6] > Remover usuario')
    print('-'*4+'[9] > Sair')
    print('-'*30+'\n'+'-'*30)

def defineOpicao(opicao):
    global inicia 
    global admin
    if opicao == '9':
        inicia = False

    elif opicao == '0':
        #[0] > Sobre
        sobre()

    elif opicao == '1':
        #[1] > Achar endereço
        acharEndereco(anotacao)
        
    elif opicao == '2':
        #[2] > Ver histórico da pesquisa
        historico(anotacao)

    elif opicao == '3':
        #[3] > Exportar lista
        exportarLista(anotacao)
       
    elif opicao == '4':        
        #[4] > Importar lista
        importarLista()
    
    elif admin == True and opicao == '5':
        #[5] > Adicionar usuario
        adicionarUsuarios()

    elif admin == True and opicao == '6':
        #[6] > Remover usuario
        removerUsuarios()


    else:
        print('Indice inválido.')

def sobre():
    cls()
    print('Desenvolvedor:\tOtávio de Mattos Júnior\n'+
        'RA:\t\t2840481813032\n'+
        'Desenvolvedor:\tGuilherme Moisés de Oliveira Brito\n'+
        'RA:\t\t2840481813018\n'+
        '\nTema: Busca de endereço.\n'+
        '\nObjetivo: O projeto consiste \n'+
        'em auxiliar o usuário na busca\n'+
        'de um edereço desejado. Por \n'+
        'meio de uma API.\n')
    continua = input("Pressione Enter para continuar")

def acharEndereco(anotacao):
    while True:           
        cls()
        print('-'*30+'\n'+'-'*30)
        print('-'*3+'Escolha a maneira de busca:')
        print('-'*4+'[0] > CEP')
        print('-'*4+'[1] > Logradouro')
        print('-'*4+'[9] > Voltar para o Menu')
        print('-'*30+'\n'+'-'*30)
        opicao1 = input('Digite:')

        if opicao1 == '0':
            #[0] > CEP
            print('-'*30+'\n'+'-'*30)                
            cep = input('Digite o cep sendo\noito digitos seguidos:')
            req = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            anotacao.append(req.json())
            cls()
            print(req.json())
            print('-'*30+'\n'+'-'*30)                                          
            pausa = input('Enter pra continuar')

        elif opicao1 == '1':
            #[1] > Logradouro                
            print('-'*30+'\n'+'-'*30)
            estado = input('Digite o Estado:')
            cidade = input('Digite o Cidade:')
            logradouro = input('Digite o Logradouro:')
            req = requests.get(f'https://viacep.com.br/ws/{estado}/{cidade}/{logradouro}/json/')
            anotacao += req.json()
            cls()
            print(req.json())
            print('-'*30+'\n'+'-'*30)
            print('\n')      
            pausa = input('Enter pra continuar')          
        elif opicao1 == '9':
            break                
        else:
            print('Erro dentro da [1] Achar endereço')

def historico(anotacao):
    cls()
    print('Relatorio----')
    print('Logradouros pesquisados:')
    print(anotacao)
    print('\ntotal de ', len(anotacao)-1, 'logradouros pesquisados')
    pausa = input('Enter pra continuar')

def exportarLista(anotacao):
    cls()
    print('exportando lista de endereços')

    nome_log = input('Nome do arquivo: ')

    with open(f'{nome_log}.json','w') as fp:
        json.dump(anotacao, fp)

    zi = zipfile.ZipFile(f'{nome_log}_{login}.zip','w', zipfile.ZIP_DEFLATED)
    zi.write('./logradouros.json')

    pausa = input('Enter pra continuar')

def importarLista():
    cls()
    print('importando lista de endereços')
    arquivo = input('Digite o nome do arquivo: ')
    with open(f'{arquivo}.json', 'r') as fp:
        data = json.load(fp)
    print(data)
    print('\nlogradouros pesquisados: [', len(data)-1, ']\n')
    
    for i in range(1,len(data)):
        print('Estado: ',data[i]['uf'])
        print('Logradouro: ',data[i]['logradouro'])
        print('cep: ',data[i]['cep'])
        print('-'*30+'\n')

    pausa = input('Enter pra continuar')

def adicionarUsuarios():
    cls()
    cnx = conexao()
    print('Adicionar Usuario:\n\n')
    user = input("Digite o nome do usuario para adicionar: ")
    password = input("Digite a senha do usuario: ")
    user_admin = input("Digite 1 para Super Usuario: ")
    if(user_admin != '1'):
        user_admin = 0
    cursor = cnx.cursor()
    sql = 'INSERT INTO userLogin (usuario, senha, user_admin) values (%s, %s, %s)'
    valores = (user, password, user_admin)
    cursor.execute(sql, valores)
    cursor.close()
    cnx.commit()
    print('Usuario adicionado com sucesso\n')
    continua = input("Aperte enter para continuar")

def removerUsuarios():
    cls()
    cnx = conexao()
    lista = busca_usuarios()
    print('Lista dos usuarios cadastrados:\n\n')
    for i in range(len(lista)):
        aux = 'Normal'
        if lista[i]['user_admin'] == 1:
            aux = 'Admin'
        print(('#{0} - {1} - {2}').format(i,lista[i]['Login'],aux))
    deleteUser = input('Digite o nome do usuario que quer deletar: ')
    for i in range(len(lista)):
        if(lista[i]['Login'] == deleteUser):
            sql = ("DELETE FROM userLogin WHERE usuario='{0}'").format(deleteUser)
            cursor = cnx.cursor()
            cursor.execute(sql)
            cursor.close()
            certeza = input("Digite Y para confirmar a exclusão: ")
            if (certeza == 'Y'):
                cnx.commit()
                print('Registro deletado com sucesso\n')
                continua = input("Aperte enter para continuar")

cls()
mensagemBemVindo()
login()

#Registro de informações do usuário
anotacao = [login]

while inicia == True:
    #Menu principal
    desenhaMenuPrincipal()
    #Define Opção escolhida
    opicao = input('Digite: ')
    defineOpicao(opicao)
    

