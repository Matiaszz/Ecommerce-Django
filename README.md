# Ecommerce

Este é um projeto de ecommerce desenvolvido em Django. O objetivo deste repositório é fornecer uma plataforma básica de ecommerce, onde os usuários podem navegar, adicionar produtos ao carrinho e realizar compras.
## Índice
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Instalar](#como-instalar)
- [Contribuições](#contribuições)

## Funcionalidades

- **Cadastro de Usuário:** Permite que novos usuários se registrem e façam login.
- **Catálogo de Produtos:** Exibe uma lista de produtos disponíveis para compra.
- **Carrinho de Compras:** Os usuários podem adicionar produtos ao carrinho e visualizar o total da compra.
- **Checkout:** Processo para finalizar a compra.
- **Integração com API de Pagamento:** O sistema conta com uma integração direta com uma API de pagamento confiável e segura, possibilitando aos usuários finalizar compras com tranquilidade. Esse recurso é essencial para proporcionar uma experiência de compra completa, permitindo pagamentos rápidos e protegidos com suporte para várias formas de pagamento, incluindo cartões de crédito, débito e carteiras digitais. Com uma interface simplificada, o checkout é fácil de usar e visa garantir segurança e conveniência aos compradores.

## Tecnologias Utilizadas

- **Django:** Framework web para desenvolvimento em Python.
- **SQLite:** Banco de dados utilizado para armazenar informações do projeto.
- **HTML/CSS:** Para a construção da interface do usuário.

## Como Instalar

1. Clone o repositório:
   ```
   git clone https://github.com/Matiaszz/Ecommerce-Django.git
   ```

2. Navegue até o diretório do projeto:
   ```
   cd Ecommerce-Django
   ```

3. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Execute as migrações do banco de dados:
   ```
   python manage.py migrate
   ```

6. Inicie o servidor:
   ```
   python manage.py runserver
   ```

7. Acesse a aplicação em `http://127.0.0.1:8000/`.


8. Realizar uma compra:
   Numero do cartão: 4242 4242 4242 4242
   MM/AA -> Qualquer data
   CVC -> Qualquer digito
   Nome -> Qualquer nome
   Email -> Qualquer email que contenha "@" e ".com"


## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
