# Azure

Aplicativo em **Python** utilizando **Kivy** e **KivyMD** para monitoramento de níveis de glicemia. Permite registrar glicemias diárias, visualizar gráficos diários e mensais, criar e gerenciar perfis de usuários.

<img width="517" height="228" alt="Image" src="https://github.com/user-attachments/assets/23d83442-217b-480e-bace-24d51ceb3726" />

---

## 📝 Funcionalidades

- Registro de glicemia por usuário com data e hora.
- Visualização de gráficos:
  - **Diário**: exibe os valores registrados no dia atual.
  - **Mensal**: exibe média diária dos níveis de glicemia.
- Cadastro e login de usuários.
- Salva automaticamente o último usuário logado.
- Interface moderna usando **KivyMD**:
  - Tela de login e registro
  - Tela de perfil com gráficos
  - Tela de guia/tutorial
- Sistema de notificações visuais e status para feedback do usuário.

---

## ⚙️ Tecnologias Utilizadas

- **Python 3**
- **Kivy** – Framework para desenvolvimento de apps gráficos
- **KivyMD** – Extensão de Kivy com componentes Material Design
- **Kivy Garden Graph** – Para plotagem de gráficos de linha
- **JSON** – Armazenamento local de dados dos usuários e glicemias

---
## 🔐 Cadastro e Login

Para criar um usuário:

Preencha o Nome de Usuário e Senha na tela de login.

Clique em Cadastrar.

Será feito login automático após o registro.

Para logar:

Preencha Nome de Usuário e Senha.

Clique em Log-In.

É possível mostrar ou ocultar a senha com o checkbox.

---
## 📊 Gráficos

Diário: mostra os valores do dia atual, com pontos destacados.

Mensal: mostra a média diária para o mês corrente.

Gráficos atualizados automaticamente ao registrar nova glicemia.

---
### 📂 Armazenamento de Dados

Usuários são salvos em userdata/user_reg.json.

Dados de glicemia de cada usuário ficam em userdata/<username>_main/<username>_data.json.

Último usuário logado é salvo em last_user.json.

---
## Planos para o Futuro

Estamos constantemente planejando novas funcionalidades para tornar o aplicativo mais completo e útil:

- **Monitoramento de Insulina:** permitir o registro e acompanhamento das doses de insulina.
- **Perfis Médico x Paciente:** criar perfis diferenciados para melhorar comunicação e acompanhamento do tratamento.
- **Base de Dados Alimentar:** permitir que o usuário registre os alimentos ingeridos, com informações nutricionais.
- **Integração com Aparelhos de Insulina:** conectar dispositivos para registrar automaticamente doses e medições.
- **Fórum de Perguntas e Respostas:** criar uma comunidade ativa onde usuários podem tirar dúvidas e compartilhar experiências.
