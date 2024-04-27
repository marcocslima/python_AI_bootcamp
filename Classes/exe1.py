class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor

    def buzinar(self):
        return f"{self.modelo} - BIBI!"

    def correr(self):
        return f"{self.modelo} - Correndo!"
    
    def parar(self):
        return f"{self.modelo} - Parando!"
    
    def __str__(self):
        return f"{self.__class__.__name__}:{', '.join([f'{key}={value}' for key, value in self.__dict__.items()])}"
    
bicicleta = Bicicleta('Azul', 'Caloi', 2021, 500.00)

print(bicicleta)