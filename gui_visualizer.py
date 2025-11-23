import tkinter as tk
from tkinter import ttk
import re 

# Dicionário de contexto para rastrear a necessidade de linhas verticais
_CONTEXT_LINES = {}

# Paleta de cores sutis para as faixas de nível
LEVEL_COLORS = ["#FFFFFF", "#F0F0F0", "#E0E0E0", "#D0D0D0"] # Cores brancas a cinza claro

def build_hierarchy_text(root, tree, level=0, lines=None):
    """Gera uma lista de linhas formatadas da hierarquia usando caracteres ASCII simples."""
    if lines is None:
        lines = []

    if root:
        # 1. Desenha o Lado Direito (Nós Menores / Sub-árvore Direita)
        if root.right:
            _CONTEXT_LINES[level] = True 
            build_hierarchy_text(root.right, tree, level + 1, lines)
            _CONTEXT_LINES[level] = False 

        # 2. Constrói a linha do nó atual
        prefixo = ""
        # Percorre os níveis de indentação anteriores (os ancestrais)
        for i in range(level):
            if _CONTEXT_LINES.get(i):
                # Caractere ASCII simples para linha vertical
                prefixo += "|   " 
            else:
                prefixo += "    "
        
        # Conector para o nó atual: '`--' se for o último, '+--' se tiver mais.
        node_connector = "`--" if not root.left else "+--" 
             
        # Montagem da linha (FORMATO TABULAR)
        nome = root.data.get("nome", "N/A")
        fb = tree._get_balance(root)
        h = root.height
        
        # Estrutura limpa: Chave: Nome | Altura: Valor | FB: Valor
        lines.append(f"{prefixo}{node_connector} {root.key}: {nome} | H: {h} | FB: {fb}")

        # 3. Desenha o Lado Esquerdo (Nós Maiores / Sub-árvore Esquerda)
        if root.left:
            _CONTEXT_LINES[level] = False 
            build_hierarchy_text(root.left, tree, level + 1, lines)

    return lines


def open_visualizer(tree):
    """Abre uma janela Tkinter exibindo a estrutura hierárquica com faixas de cor por nível."""

    if tree.root is None:
        print("Árvore vazia. Nada para exibir.")
        return

    # Janela principal e Tamanho
    window = tk.Tk()
    window.title("Visualizador de Árvore AVL — Estrutura Hierárquica OTIMIZADA FINAL")
    window.geometry("1200x800") 

    frame = ttk.Frame(window)
    frame.pack(fill="both", expand=True)

    # Canvas e Barras de Rolagem
    canvas = tk.Canvas(frame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = ttk.Scrollbar(window, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    
    # É fundamental configurar 'xscrollincrement' para garantir que a rolagem horizontal
    # funcione corretamente com a fonte monoespaçada.
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, xscrollincrement=1) 

    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    _CONTEXT_LINES.clear() 
    lines = build_hierarchy_text(tree.root, tree)
    
    MAX_LEVEL_COLORS = len(LEVEL_COLORS)

    # Widget de Texto
    # 'wrap="none"' é crucial para evitar quebras de linha que estragam a estrutura
    text_widget = tk.Text(inner_frame, wrap="none", font=("Consolas", 14), width=100, height=50, bg="#fcfcfc")
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)

    # 🎨 CONFIGURAÇÃO DE CORES E ESTILOS (Tags)
    # A cor do conector é agora mais clara, já que ele é um caractere simples
    text_widget.tag_configure("connector", foreground="#A0A0A0") 
    text_widget.tag_configure("key", foreground="#2C3E50", font=("Consolas", 14, "bold")) 
    text_widget.tag_configure("name", foreground="#16A085") 
    text_widget.tag_configure("separator", foreground="#BDBDBD") 
    text_widget.tag_configure("info_h", foreground="#9B59B6") 
    text_widget.tag_configure("fb_ok", foreground="#27AE60", font=("Consolas", 14, "bold")) 
    text_widget.tag_configure("fb_danger", foreground="#C0392B", font=("Consolas", 14, "bold", "underline")) 

    # Insere e aplica tags
    for i, line in enumerate(lines):
        start_index = text_widget.index(tk.END)
        text_widget.insert(tk.END, line + "\n")
        
        try:
            # 1. Calcular o Nível (Profundidade)
            # A lógica é baseada no caractere '|' ou ' '
            prefix_length = 0
            for char in line:
                if char in ('|', ' '):
                    prefix_length += 1
                else:
                    break # Encontrou o conector (+-- ou `--), para a contagem.
            
            # O conector tem 3 caracteres (+-- ou `--).
            level = int((prefix_length - 3) / 4) if prefix_length > 3 else 0
            
            # 2. Aplicar a Cor de Fundo por Nível
            bg_tag = f"level_bg_{level % MAX_LEVEL_COLORS}"
            if bg_tag not in text_widget.tag_names():
                text_widget.tag_configure(bg_tag, background=LEVEL_COLORS[level % MAX_LEVEL_COLORS])

            text_widget.tag_add(bg_tag, start_index, f"{start_index} lineend") 
            
            # 3. Aplicar tags de cor de texto (Baseado na versão tabular anterior)

            # O conteúdo principal começa logo após o conector ('+-- ' ou '`-- ')
            idx_content_start = line.index('--') + 3
            prefix_and_connector = line[:idx_content_start]
            
            # Aplica tag de conector ao prefixo
            text_widget.tag_add("connector", start_index, f"{start_index}+{len(prefix_and_connector)}c")

            # ... [Lógica de Regex para colorir o texto (ID, Nome, H, FB)] ...
            
            # Key (ID) - Ex: 10:
            match_key = re.search(r"(\d+):", line)
            key_end_pos = 0
            if match_key:
                key_start_pos = match_key.start(1)
                key_end_pos = match_key.end(1)
                text_widget.tag_add("key", f"{start_index}+{key_start_pos}c", f"{start_index}+{key_end_pos}c")
                text_widget.tag_add("separator", f"{start_index}+{key_end_pos}c", f"{start_index}+{key_end_pos+1}c") # Separador ':'
                
            # Name - Ex: Calçados (tudo entre ': ' e ' | H:')
            match_name = re.search(r":\s*(.?)\s\|", line)
            if match_name:
                name_start_pos = match_name.start(1)
                name_end_pos = match_name.end(1)
                text_widget.tag_add("name", f"{start_index}+{name_start_pos}c", f"{start_index}+{name_end_pos}c")

            # Altura (H) - Apenas o valor
            match_h = re.search(r"H:\s*(\d+)", line)
            if match_h:
                h_value_start = match_h.start(1)
                h_value_end = match_h.end(1)
                text_widget.tag_add("info_h", f"{start_index}+{h_value_start}c", f"{start_index}+{h_value_end}c")

            # Balance Factor (FB) - Valor + Destaque condicional
            match_fb = re.search(r"FB:\s*([\-]?\d+)", line)
            if match_fb:
                fb_value = int(match_fb.group(1))
                fb_start_pos = match_fb.start(1)
                fb_end_pos = match_fb.end(1)
                
                fb_tag = "fb_ok"
                if abs(fb_value) > 1:
                    fb_tag = "fb_danger"
                    
                text_widget.tag_add(fb_tag, f"{start_index}+{fb_start_pos}c", f"{start_index}+{fb_end_pos}c")

                # Repintar os separadores '|' e ':'
                first_colon_end = key_end_pos + 1 if match_key else 0
                for sep_match in re.finditer(r"\||:", line):
                    sep_start = sep_match.start()
                    sep_end = sep_match.end()
                    if sep_start >= first_colon_end: 
                        text_widget.tag_add("separator", f"{start_index}+{sep_start}c", f"{start_index}+{sep_end}c")
                
        except ValueError:
            pass
            
    text_widget.configure(state="disabled")

    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    text_widget.see("1.0") 

    window.mainloop()