📦 Compra Fácil
Sistema de recomendação de produtos com interface gráfica em Tkinter e banco de dados SQLite.

Permite gerenciar usuários, produtos, realizar compras e sugerir produtos com base no histórico de compras.

✅ Funcionalidades

📋 Cadastro, listagem e remoção de usuários


💰 Registro de compras com seleção direta de produtos

🤖 Sistema de recomendação:

Para novos usuários → com base na categoria de interesse

Para usuários existentes → com base no histórico de compras

🖼️ Interface gráfica com Tkinter, organizada e intuitiva

🗃️ Banco de dados SQLite3 para persistência de dados

🏗️ Estrutura do Projeto

compra_facil/

├── data/

│      └── users.db                # Banco de dados de usuários e compras


│      └── items.db                # Banco de dados de produtos

├── images/
  
 │  └── comprafacil.png         # Imagem do sistema

├── modules/

│      ├── user.py                 # Lógica de usuários e compras

│      ├── item.py                 # Lógica de itens/produtos

│      └── recommendation.py       # Sistema de recomendação


├── main.py                     # Arquivo principal, interface gráfica


└── README.md                   # Documentação


🛠️ Tecnologias Utilizadas
Python 3.10+

Tkinter - Interface gráfica

SQLite3 - Banco de dados

Pillow - Manipulação de imagens

ttk - Componentes gráficos avançados

🚀 Como Executar
1 - Clone o repositório:

git clone (https://github.com/wcguii/Compra_Facil)
cd compra_facil

2- Instale as dependências:
 
no seu console do visual code 
pip install pillow

3- Execute o sistema:

python main.py

✅ Ao iniciar, o sistema cria os bancos automaticamente e insere dados de exemplo se estiverem vazios.

🖼️ Interface
Topo: Logotipo e título

Centro: Painel dinâmico para formulários e mensagens

Botões:
→ Organizados em 2 linhas com 4 opções cada:

Cadastrar Usuário | Listar Usuários | Remover Usuário | Adicionar Item  
Listar Itens      | Remover Item    | Realizar Compra | Sair  


🧑‍💻 Principais Módulos
1. modules/user.py
Funções para:

Cadastrar, listar, remover usuários

Registrar compras

Recuperar histórico

2. modules/item.py
Funções para:

Cadastrar, listar, remover itens

Definir categorias de produtos

3. modules/recommendation.py
Geração de recomendações:

Baseadas em interesse ou histórico

Sugere até 3 produtos relevantes

🎯 Como Usar
1️⃣ Cadastrar usuário → Nome
2️⃣ Adicionar itens → Nome + Tipo
3️⃣ Realizar compra → Seleciona usuário e produto
4️⃣ Sistema exibe recomendações personalizadas


📝 Exemplo de fluxo:
✅ Cadastrar: "Maria"
✅ Adicionar: "Smartphone X", tipo "Eletrônicos"
✅ Realizar compra → Escolher "Maria" e o "Smartphone"
✅ Sistema recomenda mais "Eletrônicos" para "Maria"!

👨‍💻 Autor
Desenvolvido por Guilherme Cardoso Da Silva
GitHub: https://github.com/wcguii
