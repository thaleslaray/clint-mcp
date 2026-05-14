# List messages by chat

Retrieve a paginated list of messages for a specific chat. Messages are sorted by created_at descending.

# OpenAPI definition

```json
{
  "openapi": "3.0.2",
  "info": {
    "title": "Clint API",
    "description": "API for managing contacts, deals, and tags in the Clint application",
    "contact": {
      "name": "API Support",
      "url": "http://www.example.com/support",
      "email": "support@example.com"
    },
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://api.clint.digital",
      "description": "Production API"
    }
  ],
  "tags": [
    {
      "name": "Messages",
      "description": "Operations related to WhatsApp Official messages (v2)"
    }
  ],
  "paths": {
    "/v2/messages/chat/{chatId}": {
      "get": {
        "summary": "List messages by chat",
        "tags": [
          "Messages"
        ],
        "description": "Retrieve a paginated list of messages for a specific chat. Messages are sorted by created_at descending.",
        "servers": [
          {
            "url": "https://api.clint.digital/v2",
            "description": "Production API (v2)"
          }
        ],
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          },
          {
            "description": "UUID of the chat",
            "in": "path",
            "name": "chatId",
            "schema": {
              "type": "string",
              "format": "uuid",
              "example": "550e8400-e29b-41d4-a716-446655440000"
            },
            "required": true
          },
          {
            "$ref": "#/components/parameters/queryParam_limit"
          },
          {
            "$ref": "#/components/parameters/queryParam_offset"
          },
          {
            "$ref": "#/components/parameters/queryParam_page"
          },
          {
            "name": "content_type",
            "in": "query",
            "required": false,
            "description": "Filter messages by content type",
            "schema": {
              "type": "string",
              "enum": [
                "TEXT",
                "IMAGE",
                "AUDIO",
                "VIDEO",
                "DOCUMENT"
              ],
              "example": "TEXT"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "A paginated list of messages",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [
                    {
                      "$ref": "#/components/schemas/PaginatedV2"
                    },
                    {
                      "type": "object",
                      "properties": {
                        "data": {
                          "type": "array",
                          "items": {
                            "$ref": "#/components/schemas/Message"
                          }
                        }
                      }
                    }
                  ]
                }
              }
            }
          },
          "400": {
            "description": "Invalid UUID format",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer",
                      "example": 400
                    },
                    "message": {
                      "type": "string",
                      "example": "Param chat_id must be a valid UUID"
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Authentication error - invalid or missing api-token"
          }
        }
      }
    }
  },
  "components": {
    "parameters": {
      "headerParamXAPIKey": {
        "description": "API Token",
        "in": "header",
        "name": "api-token",
        "schema": {
          "type": "string"
        },
        "required": true
      },
      "queryParam_limit": {
        "description": "Max number of rows returned",
        "in": "query",
        "name": "limit",
        "schema": {
          "default": 200,
          "maximum": 1000,
          "minimum": 1,
          "type": "integer"
        }
      },
      "queryParam_offset": {
        "description": "Number of rows skipped of the result",
        "in": "query",
        "name": "offset",
        "schema": {
          "default": 0,
          "minimum": 0,
          "type": "integer"
        }
      },
      "queryParam_page": {
        "description": "Select the page of the result",
        "in": "query",
        "name": "page",
        "schema": {
          "default": 1,
          "minimum": 1,
          "type": "integer"
        }
      }
    },
    "schemas": {
      "Message": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "chat_id": {
            "type": "string",
            "format": "uuid",
            "nullable": true,
            "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8"
          },
          "user_id": {
            "type": "string",
            "format": "uuid",
            "nullable": true,
            "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8"
          },
          "content": {
            "type": "string",
            "example": "Hello, how can I help you?"
          },
          "type": {
            "type": "string",
            "enum": [
              "USER",
              "CUSTOMER",
              "EVENT",
              "NOTE"
            ],
            "example": "USER"
          },
          "sent": {
            "type": "boolean",
            "example": true
          },
          "seen": {
            "type": "boolean",
            "example": false
          },
          "delivered": {
            "type": "boolean",
            "example": true
          },
          "content_type": {
            "type": "string",
            "example": "TEXT"
          },
          "content_url": {
            "type": "string",
            "nullable": true,
            "example": "https://example.com/file.jpg"
          },
          "external_id": {
            "type": "string",
            "nullable": true,
            "example": "wamid.HBgNNTU0ODk..."
          },
          "content_object": {
            "type": "object",
            "nullable": true
          },
          "content_action": {
            "type": "object",
            "nullable": true
          },
          "status": {
            "type": "string",
            "enum": [
              "QUEUED",
              "SENT",
              "DELIVERED",
              "READ"
            ],
            "example": "DELIVERED",
            "description": "Derived from sent/delivered/seen flags"
          },
          "source": {
            "type": "string",
            "nullable": true,
            "example": "API",
            "description": "Origin of the message (e.g. API, CAMPAIGN, WEB)"
          }
        }
      },
      "DateTime": {
        "type": "string",
        "format": "date-time",
        "example": "2020-01-01T14:15:00.000000+00:00"
      },
      "ID": {
        "type": "string",
        "format": "uuid",
        "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8"
      },
      "PaginatedV2": {
        "type": "object",
        "description": "V2 paginated response with snake_case keys",
        "properties": {
          "status": {
            "type": "integer",
            "example": 200,
            "description": "Response status"
          },
          "total_count": {
            "type": "integer",
            "example": 50,
            "description": "Total items based on current filters"
          },
          "page": {
            "type": "integer",
            "example": 1,
            "description": "Current page"
          },
          "total_pages": {
            "type": "integer",
            "example": 10,
            "description": "Total pages based on current filters"
          },
          "has_next": {
            "type": "boolean",
            "example": true,
            "description": "Indicates that has next page"
          },
          "has_previous": {
            "type": "boolean",
            "example": false,
            "description": "Indicates that has previous page"
          }
        }
      }
    }
  },
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "_id": {
    "buffer": {
      "0": 101,
      "1": 120,
      "2": 110,
      "3": 160,
      "4": 240,
      "5": 131,
      "6": 105,
      "7": 0,
      "8": 119,
      "9": 234,
      "10": 190,
      "11": 194
    }
  }
}
```