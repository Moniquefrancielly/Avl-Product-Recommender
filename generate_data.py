import json
import random

# --- CONFIGURAÇÕES DO SISTEMA ---
NUM_CATEGORIES = 10
NUM_SUBCATEGORIES_PER_CATEGORY = 5
# Ajuste para manter o total próximo de 10.000 itens (a meta do projeto)
TOTAL_PRODUCTS_TARGET = 9940 
FILE_NAME = "banco_data.json"

# --- RECURSOS PARA NOMES DE PRODUTOS ---
ADJETIVOS = ["Premium", "Max", "Ultra", "Lite", "Smart", "Ergonômico", "Pro", "Econômico", "Compacto", "Novo", "Básico", "Avançado"]
TIPOS_PRODUTO = ["Camiseta", "Fones", "Notebook", "Cadeira", "Tênis", "Relógio", "Kit", "Mesa", "Lâmpada", "Controle", "Calça", "Vestido", "Óculos"]
CARACTERISTICAS = ["Bluetooth", "4K", "LED", "Gamer", "Algodão", "Digital", "Modular", "Sem Fio", "Aço Inox", "Recarregável", "Infantil", "Adulto"]


def generate_categories(start_id):
    """Gera as categorias de Nível 1."""
    nomes_categorias = [
        "Eletrônicos", "Moda Masculina", "Moda Feminina", "Casa & Cozinha", 
        "Esportes", "Ferramentas", "Automotivo", "Saúde & Beleza", 
        "Livros & Mídia", "Brinquedos"
    ]
    categories = []
    current_id = start_id
    
    # Criar a categoria Raiz (ID 0) para onde todas as Nível 1 se conectarão
    # Isso facilita a navegação no nível mais alto
    categories.append({
        "id": 1, 
        "tipo": "Categoria Raiz", 
        "nome": "CATÁLOGO PRINCIPAL", 
        "pai_id": 0, 
        "descricao": "Nível mais alto da hierarquia de produtos."
    })
    current_id += 1 # Inicia a partir do ID 2, pois 1 é a raiz

    for nome in nomes_categorias:
        categories.append({
            "id": current_id,
            "tipo": "Categoria",
            "nome": nome,
            "pai_id": 1, # Todas as categorias principais se conectam à Raiz (ID 1)
            "descricao": f"Produtos principais da categoria: {nome}."
        })
        current_id += 1
    return categories, current_id

def generate_subcategories(categories, start_id):
    """Gera subcategorias de Nível 2, conectando-as ao PAI (Nível 1)."""
    subcategories = []
    current_id = start_id
    
    # Mapeamento expandido para subcategorias
    subcat_map = {
        "Eletrônicos": ["Smartphones", "TVs e Vídeo", "Áudio Portátil", "Acessórios", "Computadores"],
        "Moda Masculina": ["Camisas", "Calças Jeans", "Calçados Esportivos", "Agasalhos", "Underwear"],
        "Moda Feminina": ["Vestidos", "Blusas", "Saias", "Calçados Elegantes", "Acessórios"],
        "Casa & Cozinha": ["Eletrodomésticos", "Utensílios", "Mobiliário", "Decoração", "Cama e Banho"],
        "Esportes": ["Futebol", "Musculação", "Ciclismo", "Natação", "Corrida"],
        "Ferramentas": ["Manuais", "Elétricas", "Jardinagem", "Medição", "Segurança"],
        "Automotivo": ["Pneus", "Óleos e Fluidos", "Acessórios Internos", "Som Automotivo", "Limpeza"],
        "Saúde & Beleza": ["Cabelo", "Pele", "Maquiagem", "Suplementos", "Higiene"],
        "Livros & Mídia": ["Ficção", "Não-Ficção", "Infantil", "Aulas Online", "Revistas"],
        "Brinquedos": ["Montar", "Eletrônicos", "Jogos de Tabuleiro", "Bonecos", "Ar Livre"],
    }
    
    parent_id_map = {} # Usado para armazenar o ID do PAI (Nível 1)
    
    for category in categories:
        # Pula a categoria Raiz
        if category['id'] == 1:
            continue
        
        parent_id = category["id"]
        # Usa o mapeamento, garantindo 5 subcategorias para cada PAI
        nomes_sub = subcat_map.get(category["nome"], [f"{category['nome']} - Grupo {i+1}" for i in range(NUM_SUBCATEGORIES_PER_CATEGORY)])
        
        for nome_sub in nomes_sub:
            subcategories.append({
                "id": current_id,
                "tipo": "Subcategoria",
                # Remove o nome da Categoria PAI do nome da subcategoria para busca mais limpa
                "nome": nome_sub, 
                "pai_id": parent_id,
                "descricao": f"Subcategoria de detalhe para {nome_sub} da categoria {category['nome']}."
            })
            # Mapeia o ID da subcategoria para o ID da categoria PAI. Útil para o random.choice
            parent_id_map[current_id] = parent_id
            current_id += 1
            
    return subcategories, current_id, parent_id_map

def generate_products(subcategories, start_id, num_products):
    """Gera produtos, conectando-os aleatoriamente às Subcategorias (Nível 2)."""
    products = []
    current_id = start_id
    
    # IDs das subcategorias (que serão os PAIs dos produtos)
    subcategory_ids = [sub["id"] for sub in subcategories]
    
    for i in range(num_products):
        # Escolhe uma subcategoria PAI aleatoriamente
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
            "pai_id": parent_id, # PAI é uma Subcategoria
            "preco": price,
            "relevancia": relevance,
            "descricao": f"Produto gerado: {nome_produto}. Ideal para {random.choice(['uso diário', 'profissionais', 'hobby', 'esportes'])}."
        })
        current_id += 1
    return products

# --- FLUXO PRINCIPAL DE GERAÇÃO ---
# Categorias Nível 1: ID 2 a 11 (ID 1 é a Raiz)
categories, next_id_cat = generate_categories(start_id=2) 

# Subcategorias Nível 2: Começa do ID 12 (10 categorias * 5 subcategorias = 50 subcategorias)
subcategories, next_id_product, _ = generate_subcategories(categories, start_id=next_id_cat)

# Produtos: Começa após as subcategorias, totalizando 10.000 itens.
products = generate_products(subcategories, start_id=next_id_product, num_products=TOTAL_PRODUCTS_TARGET)

all_data = categories + subcategories + products
total_itens = len(all_data)

# Salva o arquivo JSON
with open(FILE_NAME, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"✅ Geração de dados concluída!")
print(f"Número total de itens gerados: {total_itens}")
print(f"Arquivo salvo como: {FILE_NAME}")
print("\nInstruções para Teste de Usabilidade:")
print("1. Salve este arquivo (generate.py) e execute-o para gerar o novo 'banco_data.json'.")
print("2. Rode o 'main.py' e escolha a Opção 1 (Inserir).")
print("3. Na pesquisa do PAI, use nomes como: 'Smartphones', 'Feminina', 'Calçados Esportivos'.")
print("4. A busca O(n) deve agora retornar os IDs esperados!")