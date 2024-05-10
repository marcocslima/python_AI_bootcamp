from abc import ABC, abstractmethod
from datetime import datetime

def menu():
  print('''
  Digite a opção desejada:

  1 - Depositar valor
  2 - Sacar valor
  3 - Extrato
  4 - Cadastrar usuário
  5 - Listar usuários
  6 - Cadastrar conta
  7 - Listar contas
  8 - Sair do sistema

  ''')

class ContasIterator:
  def __init__(self, contas):
    self._contas = contas
    self._index = 0

  def __next__(self):
    try:
      conta = self._contas[self._index]
      return f"""\
        Agência:\t{conta.agencia}
        C/C:\t\t{conta.numero}
        Titular:\t{conta.cliente[0]['nome']}
        Saldo:\t\tR$ {conta.saldo:.2f}
        """
    except IndexError:
      raise StopIteration()
    finally:
      self._index += 1

  def __iter__(self):
    return self

class Cliente:
  def __init__(self, endereco):
    self._endereco = endereco
    self._contas = []
  
  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)
  
  def adicionar_conta(self, conta):
    self._contas.append(conta)

class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes
  
  def adicionar_transacao(self, transacao):
    self._transacoes.append(
      {
       "tipo": transacao.__class__.__name__,
       "valor": transacao.valor,
       "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
      }
    )

class PessoaFisica(Cliente):
  def __init__(self, nome, data_nascimento, cpf, endereco):
    super().__init__(endereco)
    self._nome = nome
    self._data_nascimento = data_nascimento
    self._cpf = cpf

class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0.00
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()

  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(numero, cliente)
  
  @property
  def saldo(self):
    return self._saldo
  
  @property
  def numero(self):
    return self._numero
  
  @property
  def agencia(self):
    return self._agencia
  
  @property
  def cliente(self):
    return self._cliente
  
  @property
  def historico(self):
    return self._historico
  
  def sacar(self, valor):
    if valor <= 0.0:
        print('Valor inválido')
        return False
    if self._saldo < valor or self._saldo == 0.0:
        print('Saldo insuficiente')
        return False
    self._saldo -= valor
    print(f"Saque de R$ {valor:.2f} realizado com sucesso na conta {self._numero}.")
    return True
  
  def depositar(self, valor):
    if valor <= 0:
        print('Valor inválido')
        return
    self._saldo += valor
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso na conta {self._numero}.")
    return True

class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self._limite = limite
    self._limite_saques = limite_saques

    def sacar(self, valor):
      numero_saques = len([transacao for transacao in self._historico.transacoes if transacao.tipo == 'Saque'])
      
      if numero_saques >= self._limite_saques:
          print('Limite de saques atingido')
      elif valor > self._limite:
          print(f'Valor máximo para saque é de R$ {self._limite:.2f}')
      else:
          return super().sacar(valor)
      
      return False
  
  def __str__(self) -> str:
    return f"""\
      Agência:\t{self.agencia}
      C/C:\t\t{self.numero}
      Titular:\t{self.cliente[0]['nome']}
      """

class Transacao(ABC):
  @property
  @abstractmethod
  def valor(self):
    pass

  @abstractmethod
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    if conta.sacar(self._valor):
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    if conta.depositar(self._valor):
      conta.historico.adicionar_transacao(self)

def log_transacao(func):
  def envelope(*args, **kwargs):
      resultado = func(*args, **kwargs)
      print(f"{datetime.now()} - {func.__name__.upper()}")
      return resultado
  return envelope

def cadastrar_usuario():
  usuario = {}
  pf = PessoaFisica(
    nome=input('Nome: '),
    data_nascimento=input('Data de nascimento: '),
    cpf=input('CPF: '),
    endereco=input('Endereço: ')
  )
  usuario['nome'] = pf._nome
  usuario['data_nascimento'] = pf._data_nascimento
  usuario['cpf'] = pf._cpf
  usuario['endereco'] = pf._endereco
  
  return usuario

def nova_conta(num_conta, clientes, contas):
  cpf = input('Digite o CPF do titular: ')
  cliente = [cliente for cliente in clientes if cliente['cpf'] == cpf]
  if len(cliente) > 0:
    conta = ContaCorrente.nova_conta(cliente, num_conta)
    contas.append(conta)
  else:
    print('Cliente não encontrado!!')
    return
  
def listar_usuarios(usuarios):
   for i, usuario in enumerate(usuarios):
      print(f'Usuário {i + 1}:')
      print(f'Nome: {usuario["nome"]}')
      print(f'Data de nascimento: {usuario["data_nascimento"]}')
      print(f'CPF: {usuario["cpf"]}')
      print(f'Endereço: {usuario["endereco"]}')

def listar_contas(contas):
  for conta in contas:
    print(f"""\
      Agência:\t{conta.agencia}
      C/C:\t\t{conta.numero}
      Titular:\t{conta.cliente[0]['nome']}
      """)

@log_transacao
def depositar_valor(contas):
    numero_conta = int(input("Digite o número da conta: "))
    valor_deposito = float(input("Digite o valor a ser depositado: "))

    for conta in contas:
        if conta.numero == numero_conta:
            Deposito(valor_deposito).registrar(conta)
            return
    print("Conta não encontrada.")

@log_transacao
def sacar_valor(contas):
    numero_conta = int(input("Digite o número da conta: "))
    valor_saque = float(input("Digite o valor a ser sacado: "))

    for conta in contas:
        if conta.numero == numero_conta:
            Saque(valor_saque).registrar(conta)
            return
    print("Conta não encontrada.")

def main():
  usuarios = []
  contas = []

  while True:
      menu();
      opcao = input("Escolha uma opção: ")
      
      if opcao == '1':
          depositar_valor(contas)
          pass
      elif opcao == '2':
          sacar_valor(contas)
          pass
      elif opcao == '3':
          for conta in contas:
              print(f"Extrato da conta {conta.numero}:")
              for transacao in conta.historico.transacoes:
                  print(f"{transacao['tipo']} de R$ {transacao['valor']:.2f} em {transacao['data']}")
          pass
      elif opcao == '4':
          usuarios.append(cadastrar_usuario())
      elif opcao == '5':
          listar_usuarios(usuarios)
      elif opcao == '6':
          nova_conta(len(contas) + 1, usuarios, contas)
      elif opcao == '7':
          listar_contas(contas)
      elif opcao == '8':
          print('Saindo do sistema...')
          break
      else:
          print('Opção inválida. Por favor, escolha uma opção válida.')

main()
