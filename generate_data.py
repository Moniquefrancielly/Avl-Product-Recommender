import json
import random

NUM_CATEGORIES = 10
NUM_SUBCATEGORIES_PER_CATEGORY = 5
TOTAL_PRODUCTS_TARGET = 9940
FILE_NAME = "banco_data.json"

ADJETIVOS = ["Premium", "Max", "Ultra", "Lite", "Smart", "Ergonômico", "Pro", "Econômico", "Compacto", "Novo"]
TIPOS_PRODUTO = ["Camiseta", "Fones", "Notebook", "Cadeira", "Tênis", "Relógio", "Kit", "Mesa", "Lâmpada", "Controle"]
CARACTERISTICAS = ["Bluetooth", "4K", "LED", "Gamer", "Algodão", "Digital", "Modular", "Sem Fio", "Aço Inox", "Recarregável"]


def generate_categories(start_id, num_categories):

    nomes_categorias = ["Eletrônicos", "Moda Masculina", "Moda Feminina", "Casa & Cozinha", 
                        "Esportes", "Ferramentas", "Automotivo", "Saúde & Beleza", 
                        "Livros & Mídia", "Brinquedos"]
    categories = []
    current_id = start_id
    for i in range(num_categories):
        nome = nomes_categorias[i % len(nomes_categorias)]
        categories.append({
            "id": current_id,
            "tipo": "Categoria",
            "nome": nome,
            "descricao": f"Produtos principais da categoria: {nome}."
        })
        current_id += 1
    return categories, current_id

def generate_subcategories(categories, start_id):

    subcategories = []
    current_id = start_id
    

    subcat_map = {
        "Eletrônicos": ["Smartphones", "TVs e Vídeo", "Áudio Portátil"],
        "Moda Masculina": ["Camisas", "Calças Jeans", "Calçados Esportivos"],
        "Casa & Cozinha": ["Eletrodomésticos", "Utensílios", "Mobiliário"],
        "Esportes": ["Futebol", "Musculação", "Ciclismo"]

    }
    
    for category in categories:
        parent_id = category["id"]

        nomes_sub = subcat_map.get(category["nome"], [f"SubGrupo {i+1}" for i in range(NUM_SUBCATEGORIES_PER_CATEGORY)])
        
        for i in range(NUM_SUBCATEGORIES_PER_CATEGORY):
            nome_sub = nomes_sub[i % len(nomes_sub)]
            subcategories.append({
                "id": current_id,
                "tipo": "Subcategoria",
                "nome": f"{nome_sub} ({category['nome']})",
                "pai_id": parent_id,
                "descricao": f"Subcategoria de detalhe para {nome_sub}."
            })
            current_id += 1
    return subcategories, current_id

def generate_products(subcategories, start_id, num_products):

    products = []
    current_id = start_id
    
    subcategory_ids = [sub["id"] for sub in subcategories]
    
    for i in range(num_products):
        parent_id = random.choice(subcategory_ids)
        price = round(random.uniform(5.00, 5000.00), 2)
        relevance = random.randint(1, 5)

        parte1 = random.choice(TIPOS_PRODUTO)
        parte2 = random.choice(ADJETIVOS)
        parte3 = random.choice(CARACTERISTICAS)
        
        nome_produto = f"{parte1} {parte2} {parte3}"
        
        products.append({
            "id": current_id,
            "tipo": "Produto",
            "nome": nome_produto,
            "pai_id": parent_id,
            "preco": price,
            "relevancia": relevance,
            "descricao": f"Produto gerado automaticamente: {nome_produto}. Ideal para {random.choice(['uso diário', 'profissionais', 'hobby', 'esportes'])}."
        })
        current_id += 1
    return products

categories, next_id_subcat = generate_categories(start_id=10000, num_categories=NUM_CATEGORIES)
subcategories, next_id_product = generate_subcategories(categories, start_id=20000)
products = generate_products(subcategories, start_id=30000, num_products=TOTAL_PRODUCTS_TARGET)

all_data = categories + subcategories + products
total_itens = len(all_data)

with open(FILE_NAME, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"✅ Geração de dados concluída!")
print(f"Número total de itens gerados: {total_itens} (um pouco mais que 10k)")
print(f"Arquivo salvo como: {FILE_NAME}")