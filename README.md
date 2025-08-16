# 🌊🛡️ Tide Lab Security Bot

![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)

Um bot de segurança avançado para servidores Discord, desenvolvido para o Tide Lab, com proteção contra spam, flood e links maliciosos, além de sistema de reputação de usuários.

## ✨ Recursos Principais

- **Proteção contra Spam**: Detecta e bloqueia mensagens repetidas em curto período
- **Anti-Flood**: Prevenção contra usuários que enviam mensagens em múltiplos canais rapidamente
- **Filtro de Links**: Bloqueio de URLs suspeitas e invites de Discord
- **Sistema de Reputação**: Pontuação baseada no comportamento dos membros
- **Regras Customizáveis**: Configuração flexível de limites e regras por servidor
- **Registro de Logs**: Histórico completo de ações de moderação
- **Comandos Slash**: Interface moderna e intuitiva

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** com discord.py 2.5.2
- **MongoDB** para armazenamento de dados
- **Asyncio** para operações assíncronas
- **UI Components** do Discord para interfaces interativas

## ⚙️ Configuração

### Pré-requisitos

- Python 3.10 ou superior
- MongoDB Atlas ou local
- Conta de bot Discord com privilégios adequados

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/LucasDesignerF/Security-Bot.git
cd Security-Bot
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `config.json` na raiz do projeto:
```json
{
    "bot_token": "SEU_TOKEN_DO_BOT",
    "mongodb_uri": "SUA_URI_DO_MONGODB"
}
```

5. Execute o bot:
```bash
python main.py
```

## 📋 Comandos Disponíveis

| Comando       | Descrição                                  | Permissão Requerida  |
|---------------|-------------------------------------------|----------------------|
| `/config`     | Configura regras de spam e links bloqueados | Administrador        |
| `/setlog`     | Define o canal para logs de segurança      | Administrador        |
| `/stats`      | Mostra estatísticas do bot no servidor     | Todos                |
| `/reputation` | Verifica reputação de um usuário           | Todos                |

## 🧰 Estrutura do Projeto

```
Security-Bot/
├── main.py            # Ponto de entrada do bot
├── config.json        # Configurações do bot (não versionado)
├── README.md          # Este arquivo
├── requirements.txt   # Dependências do projeto
├── cogs/
│   └── security.py    # Cog principal com toda a lógica de segurança
└── database/
    └── db.py          # Classe de conexão com o MongoDB
```

## 🤖 Funcionamento Interno

O bot utiliza vários sistemas para proteção do servidor:

1. **Cache de Mensagens**: Monitora a frequência de mensagens por usuário
2. **Detecção de Padrões**: Identifica comportamentos suspeitos como flood entre canais
3. **Regex Avançado**: Filtra URLs e invites de Discord
4. **Sistema de Reputação**: Atribui pontuação baseada no comportamento positivo/negativo
5. **Ações Automáticas**: Aplica mutes temporários ou bans conforme a gravidade

## 📊 Banco de Dados

O MongoDB é utilizado para armazenar:

- **Configurações por servidor** (limites de spam, canais de log)
- **Histórico de ações de moderação**
- **Reputação dos usuários**

Exemplo de estrutura dos documentos:

```javascript
// Configurações do servidor
{
    "guild_id": "1234567890",
    "spam_limit": 5,
    "spam_interval": 5,
    "forbidden_links": ["example.com", "badlink.org"],
    "log_channel": "9876543210"
}

// Reputação de usuário
{
    "user_id": "1122334455",
    "guild_id": "1234567890",
    "score": 42
}
```

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/incrivel`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature incrível'`)
4. Push para a branch (`git push origin feature/incrivel`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✉️ Contato

Lucas Fortes - [GitHub](https://github.com/LucasDesignerF) - ofc.rede@gmail.com - [Rede Gamer](https://discord.gg/w4RhuhrBS2)
