class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor


    def show_info(self):
        print(f"Cor: {self.cor}, Valor: {self.valor}, Model: {self.modelo}, Year: {self.ano}")

    def buzinar(self):
        print("Prim, prim, prim!")

    def parar(self):
        print("Parando a bicicleta...")
        print("Bicicleta parada.")
    
    def correr(self):
        print("Vais laskeeeera!")

    def __str__(self):
        return f'{self.__class__.__name__}: {", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])}'


b1 = Bicicleta("vermelha", "Caloi", 2022, 600)
b1.show_info()
b1.buzinar()
b1.correr()
b1.parar()

print(b1)