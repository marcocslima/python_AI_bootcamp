import datetime

menu = '''
Digite a opção desejada:

1 - Depositar valor
2 - Sacar valor
3 - Extrato
4 - Cadastrar usuário
5 - Listar usuários
6 - Cadastrar conta
7 - Listar contas
8 - Sair do sistema

'''

estados_brasileiros = [
    "AC",  # Acre
    "AL",  # Alagoas
    "AP",  # Amapá
    "AM",  # Amazonas
    "BA",  # Bahia
    "CE",  # Ceará
    "DF",  # Distrito Federal
    "ES",  # Espírito Santo
    "GO",  # Goiás
    "MA",  # Maranhão
    "MT",  # Mato Grosso
    "MS",  # Mato Grosso do Sul
    "MG",  # Minas Gerais
    "PA",  # Pará
    "PB",  # Paraíba
    "PR",  # Paraná
    "PE",  # Pernambuco
    "PI",  # Piauí
    "RJ",  # Rio de Janeiro
    "RN",  # Rio Grande do Norte
    "RS",  # Rio Grande do Sul
    "RO",  # Rondônia
    "RR",  # Roraima
    "SC",  # Santa Catarina
    "SP",  # São Paulo
    "SE",  # Sergipe
    "TO"   # Tocantins
]

saldo = 0
historico_operacoes = []
usuarios = []
contas = []
NUM_MAX_SAQUES_DIA = 3
LIMITE_SAQUE = 500

def limpar_numeros(texto):
    return ''.join(caractere for caractere in texto if caractere.isdigit())

def registro(operacao, valor):
    data_hora = datetime.datetime.now()
    reg = f'{operacao} de R$ {valor:.2f} em {data_hora.strftime("%d/%m/%Y %H:%M:%S")}'
    return reg

def depositar(valor, saldo, /):
    if valor <= 0:
        print('Valor inválido')
        return
    saldo += valor
    return saldo

def sacar(*, valor, saldo, historico):
    global NUM_MAX_SAQUES_DIA
    for h in historico:
        if 'Saque' in h:
            data_atual = datetime.datetime.now()
            if data_atual.strftime('%d/%m/%Y') in h:
                NUM_MAX_SAQUES_DIA -= 1
    if valor <= 0.0:
        print('Valor inválido')
        return
    if valor > LIMITE_SAQUE:
        print(f'Valor máximo para saque é de R$ {LIMITE_SAQUE:.2f}')
        return
    if NUM_MAX_SAQUES_DIA < 0.0:
        print('Limite de saques diários atingido')
        return
    if saldo < valor or saldo == 0.0:
        print('Saldo insuficiente')
        return
    saldo -= valor
    return saldo

def extrato(historico_operacoes, /, *, saldo):
    for i in historico_operacoes:
        print(i)
    print(f'\nSaldo: R$ {saldo:.2f}\n')

def criar_usuario(*, nome, data_nascimento, cpf, endereco):
    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco,
    }
    return usuario

def listar_usuarios():
    for usuario in usuarios:
        print(usuario)

def montar_endereco(*, logradouro, numero, bairro, cidade, estado):
    endereco = f'{logradouro}, {numero} - {bairro}, {cidade} - {estado}'
    return endereco

def verifica_sigla_estados(sigla):
    while True:
      if sigla.upper() not in estados_brasileiros:
          print('Sigla de estado inválida')
          sigla = input('Digite uma sigla de estado válida: ')
          continue
      else:
        return sigla.upper()
      
def criar_conta(cpf):
    if len(usuarios) == 0:
      print('Nenhum usuário cadastrado')
    else:
      for usuario in usuarios:
          if limpar_numeros(cpf) == limpar_numeros(usuario['cpf']):
            contas.append(dict(agencia='0001', conta=len(contas)+1, usuario=usuario))
            print('Conta criada com sucesso')
          else:
            print('CPF não encontrado')
            break

def listar_contas():
    for conta in contas:
        print(conta)

while True:
    opcao = int(input(menu))
    if opcao == 1:
        valor_input = float(input('Digite o valor da operação: '))
        saldo = depositar(valor_input, saldo)
        historico_operacoes.append(registro('Depósito', valor_input))
    elif opcao == 2:
        valor_input = float(input('Digite o valor da operação: '))
        saldo = sacar(valor=valor_input, saldo=saldo, historico=historico_operacoes)
        historico_operacoes.append(registro('Saque', valor_input))
    elif opcao == 3:
        extrato(historico_operacoes, saldo=saldo)
    elif opcao == 4:
        nome = input('Digite o nome: ')
        data_nascimento = input('Digite a data de nascimento: ')
        cpf = input('Digite o CPF: ')
        logradouro=input('Digite o logradouro: ')
        numero=input('Digite o número: ')
        bairro=input('Digite o bairro: ')
        cidade=input('Digite a cidade: ')
        estado=verifica_sigla_estados(input('Digite a sigla estado: '))
        endereco = montar_endereco(logradouro=logradouro, numero=numero, bairro=bairro, cidade=cidade, estado=estado)
        usuario = criar_usuario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        usuarios.append(usuario)
        print(usuario)
    elif opcao == 5:
        listar_usuarios()
    elif opcao == 6:
        criar_conta(input('Digite o CPF do usuário: '))
    elif opcao == 7:
        listar_contas()
    elif opcao == 8:
        print('Saindo do sistema')
        break
    else:
        print('Opção inválida')