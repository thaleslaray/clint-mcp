"""Auto-generated tool registry."""
from clint_mcp.tools import account as _account  # noqa: F401
from clint_mcp.tools import channel_accounts as _channel_accounts  # noqa: F401
from clint_mcp.tools import chats as _chats  # noqa: F401
from clint_mcp.tools import contacts as _contacts  # noqa: F401
from clint_mcp.tools import dashboards as _dashboards  # noqa: F401
from clint_mcp.tools import deals as _deals  # noqa: F401
from clint_mcp.tools import groups as _groups  # noqa: F401
from clint_mcp.tools import lost_status as _lost_status  # noqa: F401
from clint_mcp.tools import message_templates as _message_templates  # noqa: F401
from clint_mcp.tools import messages as _messages  # noqa: F401
from clint_mcp.tools import organizations as _organizations  # noqa: F401
from clint_mcp.tools import origins as _origins  # noqa: F401
from clint_mcp.tools import tags as _tags  # noqa: F401
from clint_mcp.tools import users as _users  # noqa: F401

ALL_TOOLS = [
    _account.clint_account_fields_list,
    _channel_accounts.clint_channel_accounts_get,
    _channel_accounts.clint_channel_accounts_list,
    _dashboards.clint_charts_data_get,
    _chats.clint_chats_by_channel_account_list,
    _chats.clint_chats_by_contact_list,
    _chats.clint_chats_get,
    _contacts.clint_contacts_attachments_list,
    _contacts.clint_contacts_create,
    _contacts.clint_contacts_delete,
    _contacts.clint_contacts_get,
    _contacts.clint_contacts_list,
    _contacts.clint_contacts_tags_add,
    _contacts.clint_contacts_tags_remove,
    _contacts.clint_contacts_update,
    _dashboards.clint_dashboards_data_get,
    _dashboards.clint_dashboards_get,
    _dashboards.clint_dashboards_list,
    _deals.clint_deals_create,
    _deals.clint_deals_delete,
    _deals.clint_deals_get,
    _deals.clint_deals_list,
    _deals.clint_deals_update,
    _groups.clint_groups_get,
    _groups.clint_groups_list,
    _lost_status.clint_lost_status_get,
    _lost_status.clint_lost_status_list,
    _message_templates.clint_message_templates_get,
    _message_templates.clint_message_templates_list,
    _messages.clint_messages_audio_send,
    _messages.clint_messages_by_chat_list,
    _messages.clint_messages_document_send,
    _messages.clint_messages_get,
    _messages.clint_messages_image_send,
    _messages.clint_messages_template_send,
    _messages.clint_messages_text_send,
    _organizations.clint_organizations_get,
    _organizations.clint_organizations_update,
    _origins.clint_origins_get,
    _origins.clint_origins_list,
    _tags.clint_tags_create,
    _tags.clint_tags_delete,
    _tags.clint_tags_get,
    _tags.clint_tags_list,
    _users.clint_users_get,
    _users.clint_users_list,
]
