menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
invalido = "O valor informado é inválido! Use apenas números e o ponto decimal."

while True:

    opcao = input(menu).lower()

    if opcao == "d":
        valor = float(input("Quanto você quer depositar? "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print(invalido)

    elif opcao == "s":
        valor = float(input("Quanto você quer sacar? "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print(f"Seu saldo de R$ {saldo:.2f} não é suficiente para este saque.")

        elif excedeu_limite:
            print(f"O valor do saque excede seu limite de R$ {limite:.2f}.")

        elif excedeu_saques:
            print(f"Você atingiu seu limite de {LIMITE_SAQUES} saques diários.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print(invalido)

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "x":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")