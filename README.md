📦 Compra Fácil - Sistema de Recomendação de Produtos

💡 Descrição

Compra Fácil é uma aplicação desktop em Python para gerenciar usuários, itens, compras e oferecer recomendações personalizadas de produtos.
O sistema permite cadastrar, listar e remover usuários e itens, registrar compras e recomendar produtos com base no histórico de compras e similaridade entre usuários.

🎯 Funcionalidades 


✅ Cadastro de novos usuários 

✅ Listagem e remoção de usuários 

✅ Cadastro, listagem e remoção de itens 

✅ Realização de compras com vinculação ao usuário 

✅ Recomendações para novos usuários baseadas na popularidade dos produtos 

✅ Recomendações personalizadas baseadas no histórico de compras 

✅ Interface gráfica moderna e responsiva com customtkinter

Tecnologias Utilizadas

Python 3.x

Tkinter (interface gráfica)

Pillow (PIL) para manipulação de imagens

NumPy para cálculos de similaridade e manipulação de matrizes

Estrutura do Projeto

compra_facil/ 

├── data/ 

│  ├── itens.db # Banco de dados de produtos

│  └── users.db # Banco de dados de usuários e compras 

├── images/ 

│  └── comprafacil.png # Imagem do sistema 

├── modules/

│  ├── item.py # Lógica de itens/produtos 

│  ├── recommendation.py # Sistema de recomendação

│  └── user.py # Lógica de usuários e compras 

├── main.py # Arquivo principal, interface gráfica 

└── readme.md # Instruções para uso do programa

⚙️ Como Executar o Projeto

Clone o repositório: git clone (https://github.com/wcguii/Compra_Facil)

Instale as dependências: 

pip install pillow

numpy pip install 

customtkinter pillow 

Obs: O SQLite já está embutido no Python.

3.Execute o aplicativo:

python main.py

📊 Algoritmos de Recomendação Para novos usuários: sugestões baseadas na popularidade dos itens mais comprados.

Para usuários existentes: recomendações baseadas no histórico de compras.

👤 Autor Guilherme Cardoso da Silva

https://github.com/wcguii
