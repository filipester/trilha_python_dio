import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d=%m-%Y %H:%M:%s"),
            }
        )

class Conta:
    def __init__(self, numero: int, cliente: str):
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0.0
        self._historico = Historico()

    @classmethod
    def nova_conta(self, cliente: str, numero: int):
        pass
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico

    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor

            # extrato += f"Depósito:\t R$ {valor:.2f}\n"
            # print(extrato)
            print("\n === Depósito realizado com sucesso! ===")
            return True
        else:
            print("O valor informado é inválido! Use apenas números e o ponto decimal.")
            return False

    def sacar(self, valor: float):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nSaldo insuficiente para esta operação.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("Por favor, digite um valor válido.")
        
        return False

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: str, limite: float = 500.0, limite_saques: int =3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        numeo_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_saques = numeo_saques >= self._limite_saques

        if excedeu_limite:
            print("\nLimite não é suficiente para esta operação.")

        elif excedeu_saques:
            print("\nLimite de saques excedido.")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """
        print("=" * 50)

class Cliente():
    def __init__(self, endereco: str, contas: list = []):
        self._endereco = endereco
        self._contas = contas
    
    def realizar_transacao(conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco: str, contas: list, cpf: str, nome:str, data_nascimento: datetime):
        super().__init__(endereco, contas)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento






















def menu():
    menu = """\n
    ======== MENU ========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [x]\tSair

    => """
    return input(textwrap.dedent(menu))


def exibir_extrato(saldo, /, *, extrato):
    print("\n============= EXTRATO =============")
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"\nSaldo:\t\t R$ {saldo:.2f}")
    print("===================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com este CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nUsuário não encontrado, não foi possível criar a conta.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas =[]

    while True:

        opcao = menu()

        if not ['d', 's', 'e', 'nu', 'nc', 'lc', 'x'].count(opcao):
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            continue

        elif opcao == "d":
            valor = float(input("Quanto você quer depositar? "))

           # saldo, extrato = depositar(saldo, valor, extrato)
            

        elif opcao == "s":
            valor = float(input("Quanto você quer sacar? "))
 
        #     saldo, extrato, numero_saques = sacar(
        #         saldo=saldo, 
        #         valor=valor, 
        #         extrato=extrato, 
        #         limite=limite, 
        #         numero_saques=numero_saques, 
        #         limite_saques=LIMITE_SAQUES
        #     )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "x":
            break






main()