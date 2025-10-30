# 🤖 Robô de Apostas com SofaScore (100% Gratuito)

Robô automatizado que analisa jogos ao vivo usando a API pública do **SofaScore** e aplica 4 estratégias de aposta com base em estatísticas em tempo real.

## ✅ Estratégias Implementadas

1. **GOL HT – SUPER FAVORITO**  
2. **GOL HT – SEM FAVORITO**  
3. **OVER LIMITE – FAVORITO**  
4. **OVER LIMITE – SEM FAVORITO**

## 🌐 Fonte de Dados

- **SofaScore API pública** (sem chave, sem custo)
  - Ataques perigosos
  - Escanteios, finalizações
  - Placar e minuto
  - Histórico dos últimos 5 jogos

## 🚀 Como Usar

### 1. Crie um bot no Telegram
- Fale com [@BotFather](https://t.me/BotFather)
- Obtenha o `TOKEN`
- Envie uma mensagem para seu bot
- Acesse `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates` para obter seu `CHAT_ID`

### 2. Variáveis de Ambiente
Adicione no seu ambiente (Render, Railway, etc.):

```env
TELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
