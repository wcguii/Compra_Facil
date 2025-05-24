import customtkinter as ctk
from PIL import Image, ImageTk
import os
from modules import recommendation

ctk.set_appearance_mode("light")  # Modo claro ou escuro ("light" ou "dark")
ctk.set_default_color_theme("blue")  # Tema azul moderno

class CompraFacilApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compra Fácil")

        self.top_frame = ctk.CTkFrame(root)
        self.top_frame.pack(pady=10)

        try:
            img_path = os.path.join("images", "comprafacil.png")
            img = Image.open(img_path)
            max_width = 300
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = ctk.CTkLabel(self.top_frame, image=self.logo_img, text="")
            logo_label.pack()
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

        ctk.CTkLabel(root, text="Compra Fácil", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        btn_frame = ctk.CTkFrame(root)
        btn_frame.pack()

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

        for idx, (text, cmd) in enumerate(btns):
            row = idx // 4
            col = idx % 4
            btn = ctk.CTkButton(btn_frame, text=text, width=180, height=40, command=cmd, corner_radius=12)
            btn.grid(row=row, column=col, padx=8, pady=8)

        self.content_frame = ctk.CTkFrame(root, width=600, height=300, corner_radius=10)
        self.content_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.clear_content()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_message(self, msg):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text=msg, justify="left", wraplength=580).pack(anchor='nw', padx=10, pady=10)

    def show_cadastrar_usuario(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Cadastrar Usuário", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(self.content_frame, text="Nome:").pack(anchor='w', padx=10)
        nome_entry = ctk.CTkEntry(self.content_frame, width=400)
        nome_entry.pack(padx=10)

        def cadastrar():
            nome = nome_entry.get().strip()
            if not nome:
                self.show_message("Por favor, insira um nome.")
                return
            user_id = recommendation.add_user(nome)
            self.show_message(f"Usuário '{nome}' cadastrado com sucesso!")
            self.recomendar_para_novo(user_id)

        ctk.CTkButton(self.content_frame, text="Cadastrar", command=cadastrar, corner_radius=12).pack(pady=10)

    def recomendar_para_novo(self, user_id):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Recomendações para você", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        recs = recommendation.recommend_for_user(user_id)
        if recs:
            texto = "Recomendações populares para novos usuários:\n\n"
            texto += "\n".join([f"- {r['nome']} ({r['tipo']})" for r in recs])
        else:
            texto = "Nenhuma recomendação disponível."
        self.show_message(texto)

    def listar_usuarios(self):
        users = recommendation.list_users()
        if not users:
            texto = "Nenhum usuário cadastrado."
        else:
            texto = "Lista de Usuários:\n\n"
            texto += "\n".join([f"ID {u['id']} - {u['nome']}" for u in users])
        self.show_message(texto)

    def show_remover_usuario(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Remover Usuário", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(self.content_frame, text="ID do usuário:").pack(anchor='w', padx=10)
        id_entry = ctk.CTkEntry(self.content_frame, width=400)
        id_entry.pack(padx=10)

        def remover():
            try:
                user_id = int(id_entry.get())
            except ValueError:
                self.show_message("ID inválido.")
                return
            recommendation.remove_user(user_id)
            self.show_message(f"Usuário com ID {user_id} removido (se existia).")

        ctk.CTkButton(self.content_frame, text="Remover", command=remover, corner_radius=12).pack(pady=10)

    def show_adicionar_item(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Adicionar Item", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(self.content_frame, text="Nome do item:").pack(anchor='w', padx=10)
        nome_entry = ctk.CTkEntry(self.content_frame, width=400)
        nome_entry.pack(padx=10)

        ctk.CTkLabel(self.content_frame, text="Tipo do item:").pack(anchor='w', padx=10)
        tipo_var = ctk.StringVar(value=recommendation.TYPES[0])
        tipo_combo = ctk.CTkComboBox(self.content_frame, values=recommendation.TYPES, variable=tipo_var, width=400)
        tipo_combo.pack(padx=10)

        def adicionar():
            nome = nome_entry.get().strip()
            tipo = tipo_var.get()
            if not nome:
                self.show_message("Por favor, insira o nome do item.")
                return
            if tipo not in recommendation.TYPES:
                self.show_message("Tipo inválido.")
                return
            recommendation.add_item(nome, tipo)
            self.show_message(f"Item '{nome}' do tipo '{tipo}' adicionado com sucesso!")

        ctk.CTkButton(self.content_frame, text="Adicionar", command=adicionar, corner_radius=12).pack(pady=10)

    def listar_itens(self):
        items = recommendation.list_items()
        if not items:
            texto = "Nenhum item cadastrado."
        else:
            texto = "Lista de Itens:\n\n"
            texto += "\n".join([f"ID {i['id']} - {i['nome']} ({i['tipo']})" for i in items])
        self.show_message(texto)

    def show_remover_item(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Remover Item", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(self.content_frame, text="ID do item:").pack(anchor='w', padx=10)
        id_entry = ctk.CTkEntry(self.content_frame, width=400)
        id_entry.pack(padx=10)

        def remover():
            try:
                item_id = int(id_entry.get())
            except ValueError:
                self.show_message("ID inválido.")
                return
            recommendation.remove_item(item_id)
            self.show_message(f"Item com ID {item_id} removido (se existia).")

        ctk.CTkButton(self.content_frame, text="Remover", command=remover, corner_radius=12).pack(pady=10)

    def show_realizar_compra(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Realizar Compra", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        usuarios = recommendation.list_users()
        if not usuarios:
            self.show_message("Nenhum usuário cadastrado para realizar compra.")
            return
        itens = recommendation.list_items()
        if not itens:
            self.show_message("Nenhum item cadastrado para compra.")
            return

        ctk.CTkLabel(self.content_frame, text="Selecione o usuário:").pack(anchor='w', padx=10)
        user_var = ctk.StringVar()
        user_combo = ctk.CTkComboBox(self.content_frame, values=[f"{u['id']} - {u['nome']}" for u in usuarios], variable=user_var, width=400)
        user_combo.pack(padx=10)

        ctk.CTkLabel(self.content_frame, text="Selecione o item:").pack(anchor='w', padx=10)
        item_var = ctk.StringVar()
        item_combo = ctk.CTkComboBox(self.content_frame, values=[f"{i['id']} - {i['nome']} ({i['tipo']})" for i in itens], variable=item_var, width=400)
        item_combo.pack(padx=10)

        def comprar():
            try:
                user_id = int(user_var.get().split(" - ")[0])
                item_id = int(item_var.get().split(" - ")[0])
            except (IndexError, ValueError):
                self.show_message("Selecione usuário e item válidos.")
                return
            recommendation.add_purchase(user_id, item_id)
            # Mostrar compra registrada com detalhes
            comprado = next((i for i in itens if i['id'] == item_id), None)
            comprado_text = f"Compra registrada: Usuário {user_id} comprou o item '{comprado['nome']}' ({comprado['tipo']})." if comprado else "Compra registrada."
            self.show_message(comprado_text)
            self.nova_recomendacao(user_id)

        ctk.CTkButton(self.content_frame, text="Registrar Compra", command=comprar, corner_radius=12).pack(pady=10)

    def nova_recomendacao(self, user_id):
        recs = recommendation.recommend_for_user(user_id)
        self.clear_content()

        title_label = ctk.CTkLabel(self.content_frame, 
                                   text="Recomendações baseadas nas suas compras:", 
                                   font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)

        if recs:
            for rec in recs:
                rec_label = ctk.CTkLabel(self.content_frame, 
                                         text=f"{rec['nome']} ({rec['tipo']})", 
                                         font=ctk.CTkFont(size=14))
                rec_label.pack(anchor="w", padx=20, pady=3)
        else:
            no_rec_label = ctk.CTkLabel(self.content_frame, 
                                        text="Nenhuma recomendação disponível.", 
                                        font=ctk.CTkFont(size=14, slant="italic"))
            no_rec_label.pack(pady=10)


if __name__ == "__main__":
    recommendation.init_test_data()

    root = ctk.CTk()
    root.geometry("700x600")
    app = CompraFacilApp(root)
    root.mainloop()
