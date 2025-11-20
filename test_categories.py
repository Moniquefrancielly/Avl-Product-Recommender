import json

with open("banco_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Listar todas as categorias para verificar nomes
print("Nomes de categorias encontrados:")
for categoria in data:
    if categoria.get('tipo') == 'Categoria':
        print(categoria.get('nome'))

# Buscar por "Moda Masculina"
nome_pesquisa = "Moda Masculina"
resultado = [
    categoria for categoria in data
    if categoria.get('tipo') == 'Categoria' and categoria.get('nome') == nome_pesquisa
]

if resultado:
    print(f"\nEncontrado(s) {len(resultado)} categoria(s):")
    for cat in resultado:
        print(f"ID: {cat['id']} | Nome: {cat['nome']}")
else:
    print("\nNenhuma categoria encontrada com esse nome.")
