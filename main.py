class ContaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R${valor:.2f} realizado.")
        else:
            print("O valor do depósito deve ser maior que zero.")

    def sacar(self, valor):
        if valor <= 0:
            print("O valor do saque deve ser maior que zero.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        else:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f} realizado.")

    def transferir(self, conta_destino, valor):
        if valor <= 0:
            print("O valor da transferência deve ser maior que zero.")
        elif valor > self.saldo:
            print("Saldo insuficiente para realizar a transferência.")
        else:
            self.saldo -= valor
            conta_destino.saldo += valor
            print(f"Transferência de R${valor:.2f} realizada.")


def obter_valor(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Por favor, insira um valor numérico válido.")


def obter_saldo_inicial(mensagem):
    while True:
        saldo = obter_valor(mensagem)
        if saldo >= 0:
            return saldo
        print("O saldo inicial não pode ser negativo.")


conta1 = ContaBancaria(
    obter_saldo_inicial("Informe o saldo inicial da Conta 1: R$")
)
conta2 = ContaBancaria(
    obter_saldo_inicial("Informe o saldo inicial da Conta 2: R$")
)

while True:
    print("\nOpções:")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Transferir")
    print("4. Sair")

    escolha = input("Escolha uma opção (1-4): ")

    if escolha == "1":
        numero_conta = input("Em qual conta deseja depositar (1 ou 2)? ")
        valor = obter_valor("Informe o valor do depósito: R$")

        if numero_conta == "1":
            conta1.depositar(valor)
        elif numero_conta == "2":
            conta2.depositar(valor)
        else:
            print("Conta inválida.")

    elif escolha == "2":
        numero_conta = input("De qual conta deseja sacar (1 ou 2)? ")
        valor = obter_valor("Informe o valor do saque: R$")

        if numero_conta == "1":
            conta1.sacar(valor)
        elif numero_conta == "2":
            conta2.sacar(valor)
        else:
            print("Conta inválida.")

    elif escolha == "3":
        conta_origem = input("Qual é a conta de origem (1 ou 2)? ")
        valor = obter_valor("Informe o valor da transferência: R$")

        if conta_origem == "1":
            conta1.transferir(conta2, valor)
        elif conta_origem == "2":
            conta2.transferir(conta1, valor)
        else:
            print("Conta inválida.")

    elif escolha == "4":
        break

    else:
        print("Opção inválida.")

print("\nSaldos finais:")
print(f"Conta 1: R${conta1.saldo:.2f}")
print(f"Conta 2: R${conta2.saldo:.2f}")
