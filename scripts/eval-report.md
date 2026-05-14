# Clint MCP — Eval Report

Total prompts: 414
Tool hit rate:  100.0%  (414/414)
Param hit rate: 97.3%  (403/414)
Both correct:   97.3%  (403/414)

**Threshold (skill): both_correct ≥ 0.95** — ✅ PASS

## By persona

| Persona | n | tool_hit | param_hit | both |
|---|---|---|---|---|
| A | 138 | 100.0% | 97.1% | 97.1% |
| B | 138 | 100.0% | 97.8% | 97.8% |
| C | 138 | 100.0% | 97.1% | 97.1% |

## By tool (sorted by worst both)

| Tool | n | tool_hit | param_hit | both |
|---|---|---|---|---|
| clint_contacts_tags_add | 9 | 100.0% | 77.8% | 77.8% |
| clint_messages_image_send | 9 | 100.0% | 77.8% | 77.8% |
| clint_messages_text_send | 9 | 100.0% | 77.8% | 77.8% |
| clint_tags_create | 9 | 100.0% | 77.8% | 77.8% |
| clint_deals_create | 9 | 100.0% | 88.9% | 88.9% |
| clint_messages_audio_send | 9 | 100.0% | 88.9% | 88.9% |
| clint_messages_document_send | 9 | 100.0% | 88.9% | 88.9% |

## Failures (sample, max 30)

- **A_clint_contacts_tags_add_v1**
  - prompt: "marca essa daí como quente"
  - target: `clint_contacts_tags_add`  |  candidate: `clint_contacts_tags_add`
  - param fails: ['extra param: tag_id']
- **A_clint_deals_create_v3**
  - prompt: "bota essa lead no funil"
  - target: `clint_deals_create`  |  candidate: `clint_deals_create`
  - param fails: ["missing required: ['origin_id']"]
- **A_clint_messages_audio_send_v1**
  - prompt: "manda esse áudio pra ela aí"
  - target: `clint_messages_audio_send`  |  candidate: `clint_messages_audio_send`
  - param fails: ["missing required: ['channel_account_id', 'url']", 'extra param: audio_url']
- **A_clint_messages_text_send_v3**
  - prompt: "dispara essa mensagem de texto pra cliente"
  - target: `clint_messages_text_send`  |  candidate: `clint_messages_text_send`
  - param fails: ["missing required: ['channel_account_id', 'message']", 'extra param: text']
- **B_clint_messages_document_send_v2**
  - prompt: "envia o contrato em PDF pro contato"
  - target: `clint_messages_document_send`  |  candidate: `clint_messages_document_send`
  - param fails: ["missing required: ['channel_account_id', 'filename', 'url']", 'extra param: document_url']
- **B_clint_messages_image_send_v3**
  - prompt: "dispara o print do resultado do aluno pro contato"
  - target: `clint_messages_image_send`  |  candidate: `clint_messages_image_send`
  - param fails: ["missing required: ['channel_account_id', 'url']", 'extra param: image_url']
- **B_clint_tags_create_v3**
  - prompt: "cria a tag 'webinar-jun' pra eu marcar a galera"
  - target: `clint_tags_create`  |  candidate: `clint_tags_create`
  - param fails: ["missing required: ['color']"]
- **C_clint_contacts_tags_add_v3**
  - prompt: "marca o contato 91120 com a tag champion-identified pra cross-ref no playbook ABM"
  - target: `clint_contacts_tags_add`  |  candidate: `clint_contacts_tags_add`
  - param fails: ['extra param: tag_id']
- **C_clint_messages_image_send_v1**
  - prompt: "envia o asset visual do case study pro contato 88321 via WhatsApp Official, dentro da messaging window"
  - target: `clint_messages_image_send`  |  candidate: `clint_messages_image_send`
  - param fails: ["missing required: ['channel_account_id', 'url']", 'extra param: image_url']
- **C_clint_messages_text_send_v2**
  - prompt: "dispara mensagem pro lead 44012 confirmando call de quinta às 14h via WABA principal"
  - target: `clint_messages_text_send`  |  candidate: `clint_messages_text_send`
  - param fails: ["missing required: ['channel_account_id', 'message']", 'extra param: text']
- **C_clint_tags_create_v2**
  - prompt: "registra label nova 'webinar-blackfriday-attendee' pra atribuir nos leads do evento ontem"
  - target: `clint_tags_create`  |  candidate: `clint_tags_create`
  - param fails: ["missing required: ['color']"]
