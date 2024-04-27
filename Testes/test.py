itens = []

conta_item = 0

while conta_item < 3:
    item = input('Digite um item: ')
    itens.append(item)
    conta_item += 1

print("Lista de Equipamentos:")
for item in itens:
    print(f"- {item}")