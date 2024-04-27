from abc import ABC, abstractmethod
from datetime import datetime

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
    return True
  
  def depositar(self, valor):
    if valor <= 0:
        print('Valor inválido')
        return
    self._saldo += valor
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
      Titular:\t{self.cliente.nome}
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


