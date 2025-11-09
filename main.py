from datetime import datetime
from random import randint

class Cliente:
    contasRegistradas = []
    def __init__(self, endereco, saldo=0):
        self.endereco = endereco
        self.contas = []
        self.saldo = saldo
        self.agencia = f"{randint(1, 999):03d}"
        self.numero = f"{randint(1, 99999):05d}"


    def validar_cpf(self, cpf):
            return cpf.isdigit() and len(cpf) == 11

    def validar_data_nascimento(self, data_nasc_str):
        try:
            data = datetime.strptime(data_nasc_str, "%d/%m/%Y")
            return data.strftime("%d/%m/%Y")
        except ValueError:
            return False
    def calcular_idade(self, data_nasc_str):
        try:
            data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y")
            hoje = datetime.today()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            return idade
        except ValueError:
            return None
    def validar_idade(self, idade):
        if idade >= 18:
            return True
        else:
            return False
    def verificar_user_existente(self,cpf,numero):
        for conta in PessoaFisica.contasRegistradas:
            if conta["cpf"] == cpf and conta["numero_conta"] == numero:
                print("⚠️ Já existe uma conta cadastrada com esse CPF e número de conta.")
                return False
        return True

class PessoaFisica(Cliente):
    limiteSaqueValor = 500
    limiteSaquesTotal = 3

    def __init__(self, endereco, cpf, nome, data_nasc):
        super().__init__(endereco, saldo=0)
        self.cpf = cpf
        self.nome = nome
        self.data_nasc = data_nasc
        self.saquesRealizados = 0

    def criar_conta(self):
        self.nome = input("Digite seu nome: ")
        self.cpf = input("Digite seu CPF: ")

        if not self.validar_cpf(self.cpf):
            print("⚠️ CPF inválido! Deve conter 11 números.")
            return
        if not self.verificar_user_existente(self.cpf, self.numero):
            print('Conta já existente')
            return
        self.endereco = input("Digite seu endereço: ")

        while True:
            data_input = input("Digite sua data de nascimento [DD/MM/AAAA]: ")
            data_formatada = self.validar_data_nascimento(data_input)
            if data_formatada:
                self.data_nasc = data_formatada
                idade = self.calcular_idade(data_formatada)
                if not self.validar_idade(idade):
                    print('Idade abaixo do necessário')
                    return
                break
            else:
                print("⚠️ Data inválida! Use o formato DD/MM/AAAA.")

        # Cria o dicionário da conta
        self.conta = {
            "nome": self.nome,
            "cpf": self.cpf,
            "endereco": self.endereco,
            "data_nascimento": self.data_nasc,
            "numero_conta": self.numero,
            "agencia": self.agencia,
            "saques": [],
            "depositos": []
        }

        self.contasRegistradas.append(self.conta)
        print("✅ Conta criada com sucesso!")

    def depositar(self, valor):
        try:
            valor = float(valor)
        except ValueError as error:
            return "valor inválido"
        if valor <= 0:
            return "Valor inválido"
        self.saldo += valor
        self.conta["depositos"].append(valor)
        return f"Depósito de R$ {valor:.2f} realizado. Saldo atual: R$ {self.saldo:.2f}"

    def sacar(self, valor):
        try:
            valor = float(valor)
        except ValueError as error:
            return "valor inválido"
        if valor > self.saldo:
            return "Saldo insuficiente"
        if self.saquesRealizados >= self.limiteSaquesTotal:
            return "Limite de saques atingido"
        if valor > self.limiteSaqueValor:
            return "Valor acima do limite de saque"
        if valor <= 0:
            return "Valor inválido"

        self.saldo -= valor
        self.conta["saques"].append(valor)
        self.saquesRealizados += 1
        return f"Saque de R$ {valor:.2f} realizado com sucesso. Saldo atual: R$ {self.saldo:.2f}"
    def mostrar_extrato(self):
        if not self.conta['depositos'] and not self.conta['saques']:
            return "Nenhuma transação realizada."

        print("\n📜 EXTRATO")
        print("-" * 25)

        if self.conta['depositos']:
            print("💰 DEPÓSITOS:")
            for i, transacao in enumerate(self.conta['depositos'], start=1):
                print(f"  {i}° DEPÓSITO - R$ {transacao:.2f}")
        else:
            print("Nenhum depósito realizado.")

        if self.conta['saques']:
            print("\n💸 SAQUES:")
            for i, transacao in enumerate(self.conta['saques'], start=1):
                print(f"  {i}° SAQUE - R$ {transacao:.2f}")
        else:
            print("Nenhum saque realizado.")

        print("-" * 25)
        print(f"💼 Saldo atual: R$ {self.saldo:.2f}")
        return
print('-----MENU------\n[0]Sair\n[1]Criar Conta\n[2]Depositar\n[3]Sacar\n[4]Mostrar Extrato')
while True:
    try:
        escolha = int(input('Digite sua escolha: '))
        if escolha < 0 or escolha > 4:
            break
        else:
            if escolha == 0:
                print("👋 Encerrando o programa.")
                break

            elif escolha == 1:
                print("\n--- Criar Conta ---")
                cliente = PessoaFisica("", "", "", "")
                cliente.criar_conta()

            elif escolha == 2:
                if not cliente:
                    print("⚠️ Crie uma conta primeiro!")
                    continue
                valor = input("Digite o valor para depósito: ")
                print(cliente.depositar(valor))

            elif escolha == 3:
                if not cliente:
                    print("⚠️ Crie uma conta primeiro!")
                    continue
                valor = input("Digite o valor para saque: ")
                print(cliente.sacar(valor))

            elif escolha == 4:
                if not cliente:
                    print("⚠️ Crie uma conta primeiro!")
                    continue
                cliente.mostrar_extrato()
    except ValueError:
        print('Não válido')
        continue


















