import datetime

menu = '''
Digite a opção desejada:

1 - Depositar valor
2 - Sacar valor
3 - Extrato
4 - Sair do sistema

'''

opcao = 0
saldo = 0
historico_operacoes = []
num_max_saques_diarios = 3
LIMITE_SAQUE = 500

def depositar(valor):
    global saldo
    if valor <= 0:
        print('Valor inválido')
        return
    saldo += valor
    data_hora = datetime.datetime.now()
    historico_operacoes.append(f'Depósito de R$ {valor:.2f} em {data_hora.strftime("%d/%m/%Y %H:%M:%S")}')

def sacar(valor):
    global saldo
    global num_max_saques_diarios
    for s in historico_operacoes:
        if 'Saque' in s:
            data_atual = datetime.datetime.now()
            if data_atual.strftime('%d/%m/%Y') in s:
                num_max_saques_diarios -= 1
    if valor <= 0:
        print('Valor inválido')
        return
    if valor > LIMITE_SAQUE:
        print(f'Valor máximo para saque é de R$ {LIMITE_SAQUE:.2f}')
        return
    if num_max_saques_diarios < 0:
        print('Limite de saques diários atingido')
        return
    if saldo < valor or saldo == 0:
        print('Saldo insuficiente')
        return
    saldo -= valor
    data_hora = datetime.datetime.now()
    historico_operacoes.append(f'Saque de R$ {valor:.2f} em {data_hora.strftime("%d/%m/%Y %H:%M:%S")}')

def extrato():
    for i in historico_operacoes:
        print(i)
    print(f'\nSaldo: R$ {saldo:.2f}\n')

while opcao != 4:
    opcao = int(input(menu))
    if opcao == 1:
        valor = float(input('Digite o valor a ser depositado: '))
        depositar(valor)
    elif opcao == 2:
        valor = float(input('Digite o valor a ser sacado: '))
        sacar(valor)
    elif opcao == 3:
        extrato()
    elif opcao == 4:
        print('Saindo do sistema')
    else:
        print('Opção inválida')