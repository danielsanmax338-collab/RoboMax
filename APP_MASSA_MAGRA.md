# Aplicativo Mobile de Ganho de Massa Magra

Este documento descreve a proposta completa para um app Android/iOS focado em hipertrofia, integrando treino, nutrição, descanso e acompanhamento de evolução.

## 1) Arquitetura do App

### 1.1 Visão geral (camadas)
- **App Mobile (Flutter ou React Native)**  
  - UI/UX, onboarding, tracking de treinos, diário alimentar, progresso.
- **Backend (API + serviços)**  
  - Autenticação, lógica de personalização, recomendações, dados do usuário.
- **Banco de Dados**  
  - Perfil, treinos, refeições, métricas, progresso, metas, assinaturas.
- **Serviços de IA/ML (opcional modular)**  
  - Ajuste de treino/dieta por progresso e feedback.
- **Push/Notificações**  
  - Lembretes de treinos, refeições, hidratação, suplementação.
- **Analytics e Telemetria**  
  - Eventos de engajamento, conversão e performance.

### 1.2 Módulos principais
- **Onboarding & Perfil**
- **Treinos & Progressão**
- **Nutrição & Macros**
- **Suplementação (opcional)**
- **Acompanhamento & Evolução**
- **Motivação & Gamificação**
- **Assinaturas & Monetização**
- **Conteúdo Educativo**

### 1.3 Stack tecnológica (sugestão moderna)
**Mobile**
- Flutter (Dart) **ou** React Native (TypeScript)
- State: Riverpod/Bloc (Flutter) ou Redux/Zustand (RN)
- Local storage: Hive/SQLite (Flutter) ou MMKV/SQLite (RN)

**Backend**
- Node.js (NestJS) **ou** Python (FastAPI)
- Auth: JWT + refresh tokens
- Cache: Redis
- Jobs/filas: BullMQ (Node) ou Celery (Python)
- Notificações: Firebase Cloud Messaging

**Banco**
- PostgreSQL (principal)
- S3-compatible (fotos, vídeos)

**Analytics**
- Firebase Analytics / Amplitude

**IA/ML**
- Serviço separado com Python (recomendações e ajustes)

### 1.4 Integração com smartwatch
- **HealthKit (iOS)** e **Google Fit (Android)** para:
  - Peso, sono, frequência cardíaca
  - Calorias gastas (para ajuste de dieta)
  - Atividade diária (passos)

## 2) Fluxo de Telas (User Flow)

1. **Splash / Boas-vindas**
2. **Onboarding inteligente**
   - Dados pessoais (idade, sexo, altura, peso)
   - Objetivo (hipertrofia, recomposição, ganho limpo)
   - Nível de treino
   - Restrição alimentar
   - Equipamentos disponíveis
   - Frequência semanal
3. **Dashboard (Home)**
   - Resumo do dia: treino, macros, hidratação, progresso
4. **Treinos**
   - Plano semanal
   - Detalhe do treino com timer e progressão
5. **Nutrição**
   - TMB, calorias, macros
   - Refeições do dia e substituições
6. **Suplementação**
   - Horários e alertas
7. **Evolução**
   - Gráficos, fotos, medidas e cargas
8. **Motivação**
   - Metas, streaks, badges
9. **Conteúdo Educativo**
10. **Perfil & Assinaturas**

## 3) Estrutura de Banco de Dados (proposta)

### 3.1 Tabelas principais
- **users**
  - id, nome, email, senha_hash, sexo, data_nascimento
- **user_profile**
  - user_id, altura, peso_atual, nível_treino, objetivo, restrições
- **equipment**
  - id, nome
- **user_equipment**
  - user_id, equipment_id
- **workout_plans**
  - id, user_id, tipo_divisão (ABC, PPL, etc.), meta_semana
- **workout_days**
  - id, plan_id, dia_semana, foco_muscular
- **exercises**
  - id, nome, grupo_muscular, video_url
- **workout_exercises**
  - id, workout_day_id, exercise_id, series, reps, descanso, carga_sugerida
- **workout_logs**
  - id, user_id, exercise_id, data, carga, reps, series

- **nutrition_profiles**
  - user_id, tmb, gasto_total, calorias_alvo, proteina_g, carbo_g, gordura_g
- **meals**
  - id, user_id, nome, horario
- **meal_items**
  - id, meal_id, alimento, quantidade, macros_json
- **hydration_logs**
  - id, user_id, data, ml_consumidos

- **supplements**
  - id, nome, descricao, aviso_educativo
- **user_supplements**
  - user_id, supplement_id, horario

- **progress_photos**
  - id, user_id, data, url
- **body_measurements**
  - id, user_id, data, peito, cintura, braço, coxa, etc.
- **weight_logs**
  - id, user_id, data, peso

- **goals**
  - id, user_id, tipo, alvo, prazo
- **streaks**
  - id, user_id, tipo, contagem_atual, recorde
- **badges**
  - id, nome, descricao, icone_url
- **user_badges**
  - user_id, badge_id, data_conquista

- **subscriptions**
  - id, user_id, tipo (free/premium), inicio, fim, status

## 4) Exemplos de Telas (texto)

### Tela: Dashboard (Home)
- Saudação personalizada
- Card “Treino de hoje” com botão “Iniciar”
- Card “Macros do dia” (Proteína/Carbo/Gordura)
- Botões rápidos: “Registrar refeição”, “Registrar peso”

### Tela: Treino do Dia
- Lista de exercícios com vídeo
- Séries, repetições, carga sugerida
- Timer de descanso com som e vibração
- Botão “Concluir treino”

### Tela: Nutrição
- Meta diária de calorias e macros
- Lista de refeições com substituições
- Gráfico de consumo x meta

### Tela: Evolução
- Gráfico semanal/mensal de peso
- Galeria de fotos de progresso
- Histórico de cargas por exercício

### Tela: Motivação
- Streak atual e recorde
- Badges conquistadas
- Frases motivacionais personalizadas

## 5) Roadmap de Desenvolvimento

### Fase 1 — MVP (6–8 semanas)
- Onboarding
- Plano básico de treinos
- Nutrição com macros
- Registro de progresso (peso)

### Fase 2 — Evolução (8–12 semanas)
- Progressão automática de carga
- Fotos de evolução
- Gráficos avançados
- Gamificação (streaks/badges)

### Fase 3 — Premium & IA (12–16 semanas)
- Dietas avançadas e treinos premium
- IA ajustando treino/dieta
- Conteúdo educativo
- Integração com smartwatch

### Fase 4 — Escala
- Social/Comunidade
- Desafios coletivos
- Marketplace de planos

## 6) Diferenciais (resumo)
- **IA adaptativa**: ajusta treino e dieta conforme progresso.
- **Feedback simples e motivador**: linguagem acessível e objetiva.
- **Conteúdo educativo**: base científica sobre hipertrofia e saúde.

