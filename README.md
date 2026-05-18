# 🎨 Fibonacci - Galeria de Artes (Backend)

![GitHub repo size](https://img.shields.io/github/repo-size/StephanieCaroll/Fibonacci-Backend?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/StephanieCaroll/Fibonacci-Backend?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/StephanieCaroll/Fibonacci-Backend?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/StephanieCaroll/Fibonacci-Backend?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

<img src="/image.png" width="1200" alt="Fibonacci Projeto">

> O **Fibonacci** é uma plataforma web desenvolvida com **Django e Django REST Framework** que conecta artistas locais e amantes da arte, oferecendo uma API robusta para gerenciamento de obras, perfis de artistas, usuários e sistema de pedidos.

## ✨ Sobre o Projeto

O projeto backend funciona como a espinha dorsal da plataforma Fibonacci. Ele é responsável por toda a lógica de negócio, persistência de dados e segurança, fornecendo uma API RESTful para ser consumida pelo frontend em React.

### Funcionalidades Atuais:
- **Modelagem de Dados**: Estrutura completa de modelos no app `fibonacci` para Obras (`Product`), Imagens de Obras (`ProductImage`), Comentários (`Comment`) e Perfis de Artistas (`ArtistProfile`).
- **API RESTful**: Criação de rotas modulares separadas para produtos, usuários e pedidos (`products_urls.py`, `user_urls.py`, `order_urls.py`) utilizando `serializers.py` para formatação dos dados em JSON.
- **Armazenamento de Mídia**: Configuração de diretórios `media/` para o upload seguro de imagens das obras, banners e fotos de perfil dos artistas.
- **Banco de Dados**: Integração e migrações configuradas utilizando o banco de dados SQLite3 padrão do Django.
---

### 🛠️ Em Desenvolvimento

O projeto está em fase de aprimoramento e expansão de endpoints. Os próximos passos são:

- [ ] **Autenticação e Permissões**: Refinar a segurança dos endpoints garantindo que apenas usuários autenticados (com JWT) possam criar comentários ou fazer pedidos.
- [ ] **Painel Administrativo**: Customizar o `admin.py` para facilitar o gerenciamento interno de usuários, obras cadastradas e moderação de comentários.
- [ ] **Integração de Pagamentos**: Estruturar a lógica no `order_views.py` para validar e salvar o status de pagamento vindo da integração com o PayPal no frontend.
- [ ] **Testes Automatizados**: Escrever e expandir a cobertura de testes no arquivo `tests.py` para garantir a estabilidade da API.
---

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você instalou a versão mais recente de `Python 3.x`.
- Você possui o `pip` (gerenciador de pacotes do Python) instalado.
- Recomendado: Uso de ambiente virtual (`venv`).
---

## 🚀 Instalando Fibonacci (Backend)

Para instalar e configurar o servidor localmente, siga estas etapas:

Linux, macOS e Windows:

# Clone o repositório
```bash
git clone https://github.com/StephanieCaroll/Fibonacci-Backend.git
```
# Entre no diretório
```
cd Fibonacci-Backend
```
# Crie e ative um ambiente virtual
```
python -m venv venv
# No Windows: venv\Scripts\activate
# No Linux/macOS: source venv/bin/activate
```
# Instale as dependências do projeto
```
pip install -r requeriments.txt
```
# Aplique as migrações do banco de dados
```
python manage.py migrate
```

## ☕ Usando Fibonacci
Para iniciar o servidor de desenvolvimento da API, execute:
```
python manage.py runserver
```
Acesse a API em http://127.0.0.1:8000 no seu navegador ou utilize ferramentas como Postman/Insomnia para testar os endpoints.

## 👥 Colaboradores
Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>

  
  <td align="center">
      <a href="https://github.com/EmillyMarrocos" title="Emilly Marrocos">
        <img src="https://github.com/EmillyMarrocos.png" width="100px;" alt="Foto da Emilly"/><br>
        <sub><b>Emilly Marrocos</b></sub>
      </a>
    </td>

  <td align="center">
      <a href="https://github.com/FabianneArezes" title="Fabiane">
        <img src="https://github.com/FabianneArezes.png" width="100px;" alt="Foto da Fabiane"/><br>
        <sub><b>Fabiane</b></sub>
      </a>
    </td>

  <td align="center">
      <a href="https://github.com/joanads-coder" title="Joana Daniely">
        <img src="https://github.com/joanads-coder.png" width="100px;" alt="Foto da Joana"/><br>
        <sub><b>Joana Daniely Silva</b></sub>
      </a>
    </td>

   <td align="center">
      <a href="https://github.com/k1onehub" title="Kauã de Santana Torres">
        <img src="https://github.com/k1onehub.png" width="100px;" alt="Foto do Kauã"/><br>
        <sub><b>Kauã de Santana Torres Bandeira</b></sub>
      </a>
    </td>

  <td align="center">
      <a href="https://github.com/lucasand-dev1" title="Lucas Gabriel Santos">
        <img src="https://github.com/lucasand-dev1.png" width="100px;" alt="Foto do Lucas"/><br>
        <sub><b>Lucas Gabriel Santos de Andrade</b></sub>
      </a>
    </td>

 <td align="center">
      <a href="https://github.com/StephanieCaroll" title="Stephanie Caroline">
        <img src="https://github.com/StephanieCaroll.png" width="100px;" alt="Foto da Stephanie"/><br>
        <sub><b>Stephanie Caroline</b></sub>
      </a>
    </td>
    
  </tr>
</table>


## 📫 Contribuindo para Fibonacci


Para contribuir com **Fibonacci**, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch:  
   ```bash
   git checkout -b minha-feature
   ```
3. Faça suas alterações e confirme-as:
   ```bash
   git commit -m 'feat: nova funcionalidade'
   
4. Envie para o branch original:
  ```bash
  git push origin minha-feature
```
5. Crie a solicitação de pull.
Como alternativa, consulte a documentação oficial do GitHub sobre pull requests.

## 🤝 Contribuições

Sinta-se à vontade para contribuir com este projeto!

💡 Sugira novas funcionalidades e melhorias.  
🐛 Relate bugs ou problemas encontrados.  
📚 Compartilhe recursos ou ideias para o design.

   
