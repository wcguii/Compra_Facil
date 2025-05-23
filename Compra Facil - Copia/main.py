import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from modules import user, item, recommendation

class CompraFacilApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compra Fácil")

        # Frame topo para a imagem
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        try:
            img_path = os.path.join("assets", "comprafacil.png")
            img = Image.open(img_path)
            max_width = 300
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.ANTIALIAS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(self.top_frame, image=self.logo_img)
            logo_label.pack()
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

        # Título
        tk.Label(root, text="Sistema Compra Fácil", font=("Arial", 16)).pack(pady=10)

        # Frame dos botões
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        # Botões principais
        btns = [
            ("Cadastrar Usuário", self.show_cadastrar_usuario),
            ("Listar Usuários", self.listar_usuarios),
            ("Remover Usuário", self.show_remover_usuario),
            ("Adicionar Item", self.show_adicionar_item),
            ("Listar Itens", self.listar_itens),
            ("Remover Item", self.show_remover_item),
            ("Realizar Compra", self.show_realizar_compra),
            ("Sair", root.destroy)
        ]

        # Ajuste: 4 botões por linha
        for idx, (text, cmd) in enumerate(btns):
            row = idx // 4
            col = idx % 4
            btn = tk.Button(btn_frame, text=text, width=20, command=cmd)
            btn.grid(row=row, column=col, padx=5, pady=5)

        # Frame para conteúdo dinâmico
        self.content_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=2, width=600, height=300)
        self.content_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.clear_content()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_message(self, msg):
        self.clear_content()
        tk.Label(self.content_frame, text=msg, justify=tk.LEFT).pack(anchor='nw', padx=10, pady=10)

    def show_cadastrar_usuario(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Cadastrar Usuário", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="Nome:").pack(anchor='w', padx=10)
        nome_entry = tk.Entry(self.content_frame, width=40)
        nome_entry.pack(padx=10)

        def cadastrar():
            nome = nome_entry.get().strip()
            if not nome:
                self.show_message("Por favor, insira um nome.")
                return
            user.add_user(nome)
            self.show_message(f"Usuário '{nome}' cadastrado com sucesso!")
            new_user_id = user.list_users()[-1][0]
            self.recomendar_para_novo(new_user_id)

        tk.Button(self.content_frame, text="Cadastrar", command=cadastrar).pack(pady=10)

    def recomendar_para_novo(self, user_id):
        self.clear_content()
        tk.Label(self.content_frame, text="Novo Usuário - Qual tipo de produto procura?", font=("Arial", 14)).pack(pady=5)
        tipo_var = tk.StringVar(value=item.TYPES[0])
        tipo_combo = ttk.Combobox(self.content_frame, values=item.TYPES, textvariable=tipo_var, state='readonly', width=37)
        tipo_combo.pack(padx=10)

        def mostrar_recomendacoes():
            tipo = tipo_var.get()
            recs = recommendation.recommend_for_new(tipo)
            if recs:
                texto = "Recomendações para você:\n\n"
                texto += "\n".join([f"- {r[1]} ({r[2]})" for r in recs])
            else:
                texto = "Nenhum item encontrado para esse tipo."
            self.show_message(texto)

        tk.Button(self.content_frame, text="Mostrar Recomendações", command=mostrar_recomendacoes).pack(pady=10)

    def listar_usuarios(self):
        users = user.list_users()
        if not users:
            texto = "Nenhum usuário cadastrado."
        else:
            texto = "Lista de Usuários:\n\n"
            texto += "\n".join([f"ID {u[0]} - {u[1]}" for u in users])
        self.show_message(texto)

    def show_remover_usuario(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Remover Usuário", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="ID do usuário:").pack(anchor='w', padx=10)
        id_entry = tk.Entry(self.content_frame, width=40)
        id_entry.pack(padx=10)

        def remover():
            try:
                user_id = int(id_entry.get())
            except ValueError:
                self.show_message("ID inválido.")
                return
            user.remove_user(user_id)
            self.show_message(f"Usuário com ID {user_id} removido (se existia).")

        tk.Button(self.content_frame, text="Remover", command=remover).pack(pady=10)

    def show_adicionar_item(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Adicionar Item", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="Nome do item:").pack(anchor='w', padx=10)
        nome_entry = tk.Entry(self.content_frame, width=40)
        nome_entry.pack(padx=10)

        tk.Label(self.content_frame, text="Tipo do item:").pack(anchor='w', padx=10)
        tipo_var = tk.StringVar(value=item.TYPES[0])
        tipo_combo = ttk.Combobox(self.content_frame, values=item.TYPES, textvariable=tipo_var, state='readonly', width=37)
        tipo_combo.pack(padx=10)

        def adicionar():
            nome = nome_entry.get().strip()
            tipo = tipo_var.get()
            if not nome:
                self.show_message("Por favor, insira o nome do item.")
                return
            if tipo not in item.TYPES:
                self.show_message("Tipo inválido.")
                return
            item.add_item(nome, tipo)
            self.show_message(f"Item '{nome}' do tipo '{tipo}' adicionado com sucesso!")

        tk.Button(self.content_frame, text="Adicionar", command=adicionar).pack(pady=10)

    def listar_itens(self):
        items = item.list_items()
        if not items:
            texto = "Nenhum item cadastrado."
        else:
            texto = "Lista de Itens:\n\n"
            texto += "\n".join([f"ID {i[0]} - {i[1]} ({i[2]})" for i in items])
        self.show_message(texto)

    def show_remover_item(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Remover Item", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="ID do item:").pack(anchor='w', padx=10)
        id_entry = tk.Entry(self.content_frame, width=40)
        id_entry.pack(padx=10)

        def remover():
            try:
                item_id = int(id_entry.get())
            except ValueError:
                self.show_message("ID inválido.")
                return
            item.remove_item(item_id)
            self.show_message(f"Item com ID {item_id} removido (se existia).")

        tk.Button(self.content_frame, text="Remover", command=remover).pack(pady=10)

    def show_realizar_compra(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Realizar Compra", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="ID do usuário:").pack(anchor='w', padx=10)
        user_id_entry = tk.Entry(self.content_frame, width=40)
        user_id_entry.pack(padx=10)

        produtos = item.list_items()
        if not produtos:
            self.show_message("Nenhum item cadastrado para realizar compra.")
            return

        tk.Label(self.content_frame, text="Selecione o produto:").pack(anchor='w', padx=10)

        produto_var = tk.StringVar()
        produto_nomes = [f"{p[0]} - {p[1]} ({p[2]})" for p in produtos]
        produto_combo = ttk.Combobox(self.content_frame, values=produto_nomes, textvariable=produto_var, state='readonly', width=50)
        produto_combo.pack(padx=10)

        def realizar():
            try:
                user_id = int(user_id_entry.get())
            except ValueError:
                self.show_message("ID do usuário inválido.")
                return

            produto_selecionado = produto_var.get()
            if not produto_selecionado:
                self.show_message("Por favor, selecione um produto.")
                return

            produto_id = int(produto_selecionado.split(" - ")[0])

            produto_info = next((p for p in produtos if p[0] == produto_id), None)
            if not produto_info:
                self.show_message("Produto não encontrado.")
                return

            tipo = produto_info[2]
            user.add_purchase(user_id, tipo)
            self.show_message(f"Compra do produto '{produto_info[1]}' registrada para usuário ID {user_id}.")
            self.nova_recomendacao(user_id)

        tk.Button(self.content_frame, text="Registrar Compra", command=realizar).pack(pady=10)

    def nova_recomendacao(self, user_id):
        recs = recommendation.recommend_for_existing(user_id)
        if recs:
            texto = "Recomendações baseadas nas suas compras:\n\n"
            texto += "\n".join([f"- {r[1]} ({r[2]})" for r in recs])
        else:
            texto = "Nenhuma recomendação disponível."
        self.show_message(texto)

def setup():
    user.init_user_db()
    item.init_item_db()

def create_test_data_if_empty():
    if len(user.list_users()) == 0 and len(item.list_items()) == 0:
        names = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo", "Fernanda", "Gustavo", "Helena", "Igor", "Julia"]
        for nome in names:
            user.add_user(nome)
        predefined_items = [
            ("Smartphone XYZ", "Eletrônicos"),
            ("Notebook ABC", "Eletrônicos"),
            ("Camiseta Polo", "Vestuário"),
            ("Calça Jeans", "Vestuário"),
            ("Livro: Python para Iniciantes", "Livros"),
            ("Fones de Ouvido", "Eletrônicos"),
            ("Tênis Esportivo", "Vestuário"),
            ("Cafeteira Elétrica", "Eletrodomésticos"),
            ("Jogo de Panelas", "Eletrodomésticos"),
            ("Bolsa Feminina", "Vestuário"),
            ("Monitor 24\"", "Eletrônicos"),
            ("Livro: Aprenda Machine Learning", "Livros"),
            ("Cadeira Gamer", "Móveis"),
            ("Mesa de Escritório", "Móveis"),
            ("Relógio de Pulso", "Acessórios"),
            ("Óculos de Sol", "Acessórios"),
            ("Smartwatch", "Eletrônicos"),
            ("Blusa de Frio", "Vestuário"),
            ("Livro: Gestão de Projetos", "Livros"),
            ("Micro-ondas", "Eletrodomésticos")
        ]
        for nome, tipo in predefined_items:
            item.add_item(nome, tipo)

        import random
        for u in user.list_users():
            user_id = u[0]
            for _ in range(10):
                tipo = random.choice(item.TYPES)
                user.add_purchase(user_id, tipo)

def main():
    setup()
    create_test_data_if_empty()
    root = tk.Tk()
    app = CompraFacilApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
