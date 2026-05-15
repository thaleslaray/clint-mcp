# Clint CRM — Prefab App Candidates

Análise dos 46 endpoints da Clint CRM identificando combinações que merecem visualização Prefab (UI rica) ao invés de JSON cru.

Personas atendidas: SDR, Closer, Gestor Comercial, Infoprodutor.

---

## PRIORIDADE ALTA

### 1. Pipeline Dashboard (Funil de Vendas)
- **Tipo:** dashboard
- **Endpoints:**
  - `GET /v2/dashboards` (lista)
  - `GET /v2/dashboards/:id`
  - `GET /v2/dashboards/:id/data`
  - `GET /v2/charts/:id/data`
  - `GET /v1/deals` (agregação por status/origem)
- **User stories:**
  - "Gestor, mostra como tá o funil da equipe esse mês — quanto entrou, quanto fechou, quanto perdeu por motivo."
  - "Quero ver o dashboard de conversão por origem (Hotmart, Eduzz, orgânico) das últimas 4 semanas."
- **Components:** Tabs (por dashboard), Metric (MRR, ticket médio, win rate, ciclo médio), BarChart (deals por etapa), LineChart (evolução semanal), PieChart (perda por motivo), DataTable (top deals em risco)
- **Prioridade:** alta

---

### 2. Deal Inbox & Triagem (Visão SDR)
- **Tipo:** table
- **Endpoints:**
  - `GET /v1/deals` (filtros por owner, status, origem, valor)
  - `GET /v1/origins`
  - `GET /v1/lost-status`
  - `GET /v1/users`
  - `GET /v1/tags`
  - `POST /v1/deals/:id` (update inline)
- **User stories:**
  - "Lista os leads novos da última hora que vieram do Hotmart e ainda não foram tocados."
  - "Mostra meus deals abertos com valor acima de 5k ordenados por última atividade."
- **Components:** DataTable (com filtros facetados: owner, origin, tag, status, valor, idade), Form inline (atribuir owner, mover etapa), Drawer (preview do deal), Metric (total filtrado, valor somado)
- **Prioridade:** alta

---

### 3. Contact 360 (Detalhe Cliente/Lead)
- **Tipo:** detail
- **Endpoints:**
  - `GET /v1/contacts/:id`
  - `GET /v1/contacts/:id/attachments`
  - `GET /v1/deals?contact_id=` (deals do contato)
  - `GET /v2/chats/contact/:contactId`
  - `GET /v2/messages/chat/:chatId`
  - `GET /v1/organizations/:id` (se vinculado)
  - `POST /v1/contacts/:id/tags`
- **User stories:**
  - "Abre o perfil do João — quero ver todos deals, conversa do WhatsApp e arquivos antes da call."
  - "Adiciona tag VIP nesse contato e mostra o histórico completo."
- **Components:** Header com avatar/metadata, Tabs (Overview, Deals, Conversas, Anexos, Tags, Org), Timeline (atividades), DataTable (deals do contato), ChatBubble (preview WhatsApp), Form (edição inline), Metric (LTV, # deals, ticket médio)
- **Prioridade:** alta

---

### 4. WhatsApp Conversations (Inbox Unificado)
- **Tipo:** detail (split view)
- **Endpoints:**
  - `GET /v2/channel-accounts`
  - `GET /v2/chats/channel-account/:channelAccountId`
  - `GET /v2/chats/:id`
  - `GET /v2/messages/chat/:chatId`
  - `POST /v2/messages/text|image|document|audio|template`
  - `GET /v2/message-templates`
- **User stories:**
  - "Abre minha caixa do WhatsApp business — quero responder os 5 leads que mandaram mensagem hoje cedo."
  - "Manda o template de follow-up pro lead do deal #4521."
- **Components:** SplitPane (lista chats + thread), DataTable de chats (com badge de não lidas), ChatThread, MessageComposer (com seletor de template, upload anexo), Tabs (por channel account), Metric (não lidas, tempo médio resposta)
- **Prioridade:** alta

---

### 5. Sales Performance (Leaderboard Comercial)
- **Tipo:** dashboard
- **Endpoints:**
  - `GET /v1/users`
  - `GET /v1/deals` (agregação por owner, status=won/lost)
  - `GET /v2/charts/:id/data`
- **User stories:**
  - "Quem fechou mais essa semana? Ranking de closer com receita e # deals."
  - "Compara meu time de SDRs: quantos leads cada um qualificou e quantos viraram deals."
- **Components:** Leaderboard (DataTable ranqueada com avatar), BarChart (revenue por owner), Metric por user (deals won, conversão, ciclo médio), LineChart (evolução individual), Tabs (SDR vs Closer)
- **Prioridade:** alta

---

## PRIORIDADE MÉDIA

### 6. Lost Deals Autopsy (Análise de Perda)
- **Tipo:** dashboard
- **Endpoints:**
  - `GET /v1/lost-status`
  - `GET /v1/deals?status=lost`
  - `GET /v1/origins`
- **User stories:**
  - "Por que perdemos deals esse mês? Quero ver agrupado por motivo e por origem."
  - "Quanto dinheiro deixou na mesa por motivo 'preço' nos últimos 90 dias?"
- **Components:** PieChart (perda por motivo), BarChart (perda por origem), Metric (total perdido em R$, ticket médio perdido), DataTable (deals perdidos com filtro), Heatmap (motivo x origem)
- **Prioridade:** média

---

### 7. Origin/Source Attribution
- **Tipo:** comparison
- **Endpoints:**
  - `GET /v1/origins`
  - `GET /v1/deals` (group by origin)
  - `GET /v1/contacts` (group by origin)
- **User stories:**
  - "Compara Hotmart vs Eduzz vs orgânico: qual origem traz lead mais barato e qual converte melhor?"
  - "Quero saber qual canal tá puxando o resultado esse trimestre."
- **Components:** ComparisonTable (origens lado a lado), BarChart (volume vs conversão), Metric por origem (CAC, ticket médio, win rate), Funnel (lead→deal→won por origem)
- **Prioridade:** média

---

### 8. Contact Segmentation by Tags
- **Tipo:** table
- **Endpoints:**
  - `GET /v1/tags`
  - `GET /v1/contacts?tag=`
  - `POST /v1/contacts/:id/tags`
  - `DELETE /v1/contacts/:id/tags`
- **User stories:**
  - "Mostra todos os contatos com tag 'comprou-curso-X' que ainda não pegaram o upsell."
  - "Quero criar uma lista de VIPs e adicionar tag em batch."
- **Components:** TagCloud / chips com counts, DataTable filtrada por tag, MultiSelect para tag em batch, Metric (# contatos por tag), Venn-ish (intersecção de tags)
- **Prioridade:** média

---

### 9. Organizations Overview (B2B)
- **Tipo:** detail
- **Endpoints:**
  - `GET /v1/organizations/:id`
  - `GET /v1/contacts?organization_id=`
  - `GET /v1/deals?organization_id=`
- **User stories:**
  - "Mostra tudo da empresa Acme: pessoas, deals abertos, receita histórica."
  - "Quem é o decisor na Acme e quais deals estão em aberto com eles?"
- **Components:** Header da org, Tabs (Pessoas, Deals, Histórico), DataTable de contatos e de deals, Metric (TCV, # deals, # pessoas), Timeline de eventos
- **Prioridade:** média

---

### 10. Message Templates Manager
- **Tipo:** table
- **Endpoints:**
  - `GET /v2/message-templates`
  - `GET /v2/message-templates/:id`
  - `GET /v2/channel-accounts`
- **User stories:**
  - "Lista os templates aprovados que posso usar nessa conta de WhatsApp."
  - "Quero ver quais templates de marketing têm variáveis e como preencher."
- **Components:** DataTable (templates com status, categoria, idioma), Preview pane (renderiza template com placeholders), Tabs por channel account, Filter (status, categoria)
- **Prioridade:** média

---

## PRIORIDADE BAIXA

### 11. Account Custom Fields Inspector
- **Tipo:** detail
- **Endpoints:**
  - `GET /v1/account/fields`
- **User stories:**
  - "Quais custom fields eu tenho configurados em contatos e deals?"
  - "Lista os campos personalizados pra eu mapear pra integração."
- **Components:** Tabs (por entidade: contact/deal/org), DataTable (nome, tipo, opções), Detail pane
- **Prioridade:** baixa

---

### 12. Groups & Team Structure
- **Tipo:** table
- **Endpoints:**
  - `GET /v1/groups`
  - `GET /v1/groups/:id`
  - `GET /v1/users`
- **User stories:**
  - "Mostra a estrutura de grupos/equipes e quem tá em cada um."
  - "Quero ver quantos users por grupo e seus papéis."
- **Components:** Tree/List de grupos, DataTable de users por grupo, Metric (# users por grupo)
- **Prioridade:** baixa

---

### 13. Deal Quick-Create Wizard
- **Tipo:** wizard
- **Endpoints:**
  - `POST /v1/contacts` (ou reuse)
  - `POST /v1/deals`
  - `GET /v1/origins`, `GET /v1/users`, `GET /v1/tags`
- **User stories:**
  - "Cria um deal novo: contato Maria, R$ 3k, origem Hotmart, owner eu."
  - "Quero registrar uma oportunidade rápido sem abrir 5 telas."
- **Components:** Wizard (Steps: Contato → Deal info → Owner/Tags → Confirm), Form com autocomplete, Combobox (origin/owner)
- **Prioridade:** baixa

---

### 14. Channel Accounts Status
- **Tipo:** dashboard
- **Endpoints:**
  - `GET /v2/channel-accounts`
  - `GET /v2/channel-accounts/:id`
- **User stories:**
  - "Quais números de WhatsApp tenho conectados e estão saudáveis?"
  - "Status da minha conta WhatsApp Official — quality rating, limite de templates."
- **Components:** Grid de cards por channel account, Metric (status, quality, msgs/dia), Badge (connected/disconnected)
- **Prioridade:** baixa

---

Done — 14 candidatos.
