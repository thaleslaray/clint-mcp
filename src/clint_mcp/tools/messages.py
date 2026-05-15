"""Auto-generated tools for messages. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_messages_audio_send(channel_account_id: Annotated[str, Field(description="""UUID of the WhatsApp Official channel account. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440001'""")], contact_id: Annotated[str, Field(description="""UUID of the contact to send the audio to. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440002'""")], url: Annotated[str, Field(description="""Direct URL of the audio file to send. Example: 'https://example.com/audio.ogg'. ⚠️ Field name is EXACTLY `url` (single field, regardless of media type). Do NOT pass `audio_url`, `image_url`, or `document_url` — none of those exist""")], chat_id: Annotated[str | None, Field(description="""Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440003'""")] = None) -> Any:
    """Send audio message

    Send an audio message via WhatsApp Official. The audio URL is sent directly to the Meta API. No caption support for audio messages. Returns immediately with QUEUED status.

    Endpoint: POST /v2/messages/audio
    """
    _params = None
    _body = {
        "channel_account_id": channel_account_id,
        "contact_id": contact_id,
        "url": url,
        "chat_id": chat_id,
    }
    return await request("POST", f"/v2/messages/audio", params=_params, json_body=_body)


async def clint_messages_by_chat_list(chat_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440000'""")], limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None, content_type: Annotated[str | None, Field(description="""Filter messages by content type. Allowed values (case-sensitive, pass EXACTLY as listed):
  - 'TEXT'
  - 'IMAGE'
  - 'AUDIO'
  - 'VIDEO'
  - 'DOCUMENT'""")] = None) -> Any:
    """List messages by chat

    Retrieve a paginated list of messages for a specific chat. Messages are sorted by created_at descending.

    Endpoint: GET /v2/messages/chat/{chatId}
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
        "content_type": content_type,
    }
    _body = None
    return await request("GET", f"/v2/messages/chat/{chat_id}", params=_params, json_body=_body)


async def clint_messages_document_send(channel_account_id: Annotated[str, Field(description="""UUID of the WhatsApp Official channel account. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440001'""")], filename: Annotated[str, Field(description="""Filename displayed to the recipient. Example: 'report.pdf'""")], contact_id: Annotated[str, Field(description="""UUID of the contact to send the document to. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440002'""")], url: Annotated[str, Field(description="""Direct URL of the document to send. Example: 'https://example.com/report.pdf'. ⚠️ Field name is EXACTLY `url` (single field, regardless of media type). Do NOT pass `audio_url`, `image_url`, or `document_url` — none of those exist""")], caption: Annotated[str | None, Field(description="""Optional caption for the document. Example: 'Monthly report'""")] = None, chat_id: Annotated[str | None, Field(description="""Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440003'""")] = None) -> Any:
    """Send document message

    Send a document message via WhatsApp Official. The document URL is sent directly to the Meta API. Filename is required and will be displayed to the recipient. Returns immediately with QUEUED status.

    Endpoint: POST /v2/messages/document
    """
    _params = None
    _body = {
        "channel_account_id": channel_account_id,
        "contact_id": contact_id,
        "url": url,
        "filename": filename,
        "caption": caption,
        "chat_id": chat_id,
    }
    return await request("POST", f"/v2/messages/document", params=_params, json_body=_body)


async def clint_messages_get(message_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], content_type: Annotated[str | None, Field(description="""Filter message by content type. Allowed values (case-sensitive, pass EXACTLY as listed):
  - 'TEXT'
  - 'IMAGE'
  - 'AUDIO'
  - 'VIDEO'
  - 'DOCUMENT'""")] = None) -> Any:
    """Get message

    Retrieve a single message by ID. Only returns messages belonging to the authenticated owner.

    Endpoint: GET /v2/messages/{id}
    """
    _params = {
        "content_type": content_type,
    }
    _body = None
    return await request("GET", f"/v2/messages/{message_id}", params=_params, json_body=_body)


async def clint_messages_image_send(channel_account_id: Annotated[str, Field(description="""UUID of the WhatsApp Official channel account. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440001'""")], contact_id: Annotated[str, Field(description="""UUID of the contact to send the image to. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440002'""")], url: Annotated[str, Field(description="""Direct URL of the image to send. Example: 'https://example.com/photo.jpg'. ⚠️ Field name is EXACTLY `url` (single field, regardless of media type). Do NOT pass `audio_url`, `image_url`, or `document_url` — none of those exist""")], caption: Annotated[str | None, Field(description="""Optional caption for the image. Example: 'Check out this photo!'""")] = None, chat_id: Annotated[str | None, Field(description="""Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440003'""")] = None) -> Any:
    """Send image message

    Send an image message via WhatsApp Official. The image URL is sent directly to the Meta API (no upload required). Returns immediately with QUEUED status.

    Endpoint: POST /v2/messages/image
    """
    _params = None
    _body = {
        "channel_account_id": channel_account_id,
        "contact_id": contact_id,
        "url": url,
        "caption": caption,
        "chat_id": chat_id,
    }
    return await request("POST", f"/v2/messages/image", params=_params, json_body=_body)


async def clint_messages_template_send(channel_account_id: Annotated[str, Field(description="""UUID of the WhatsApp Official channel account. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440001'""")], contact_id: Annotated[str, Field(description="""UUID of the contact to send the template to. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440002'""")], template_id: Annotated[str, Field(description="""UUID of the message template to send. Must have APPROVED status. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440010'. ⚠️ Field name is EXACTLY `template_id`. Do NOT pass `template_name` or `message_template_id`""")], chat_id: Annotated[str | None, Field(description="""Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440003'""")] = None, parameters: Annotated[dict | None, Field(description="""Variable values to replace {{1}}, {{2}}, etc. in the template components. Each array position maps to the corresponding placeholder number""")] = None) -> Any:
    """Send template message

    Send a WhatsApp message template (HSM). Template messages can be sent at any time, even when the 24-hour messaging window is closed. The template must be APPROVED by Meta and belong to the specified channel account. Variable placeholders ({{1}}, {{2}}, etc.) in the template are replaced with the provided parameter values.

    Endpoint: POST /v2/messages/template
    """
    _params = None
    _body = {
        "channel_account_id": channel_account_id,
        "contact_id": contact_id,
        "template_id": template_id,
        "chat_id": chat_id,
        "parameters": parameters,
    }
    return await request("POST", f"/v2/messages/template", params=_params, json_body=_body)


async def clint_messages_text_send(channel_account_id: Annotated[str, Field(description="""UUID of the WhatsApp Official channel account. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440001'""")], message: Annotated[str, Field(description="""Text content of the message. Example: 'Hello, how can I help you?'. ⚠️ Field name is EXACTLY `message`. Do NOT pass `text` — that field does not exist""")], contact_id: Annotated[str, Field(description="""UUID of the contact to send the message to. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440002'""")], chat_id: Annotated[str | None, Field(description="""Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440003'""")] = None) -> Any:
    """Send text message

    Send a text message via WhatsApp Official. Reuses the existing message sending flow — validates channel account, contact, and messaging window, then dispatches to the WhatsApp provider. Returns immediately with QUEUED status.

    Endpoint: POST /v2/messages/text
    """
    _params = None
    _body = {
        "channel_account_id": channel_account_id,
        "contact_id": contact_id,
        "message": message,
        "chat_id": chat_id,
    }
    return await request("POST", f"/v2/messages/text", params=_params, json_body=_body)
