# List chats by channel account

Retrieve a paginated list of chats for a specific channel account. Results are sorted by last_message_at descending.

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
      "name": "Chats",
      "description": "Operations related to WhatsApp Official chats via OpenSearch (v2)"
    }
  ],
  "paths": {
    "/v2/chats/channel-account/{channelAccountId}": {
      "get": {
        "summary": "List chats by channel account",
        "tags": [
          "Chats"
        ],
        "description": "Retrieve a paginated list of chats for a specific channel account. Results are sorted by last_message_at descending.",
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
            "description": "UUID of the channel account",
            "in": "path",
            "name": "channelAccountId",
            "schema": {
              "type": "string",
              "format": "uuid",
              "example": "550e8400-e29b-41d4-a716-446655440000"
            },
            "required": true
          },
          {
            "$ref": "#/components/parameters/queryParam_limit_200"
          },
          {
            "$ref": "#/components/parameters/queryParam_offset"
          },
          {
            "$ref": "#/components/parameters/queryParam_page"
          }
        ],
        "responses": {
          "200": {
            "description": "A paginated list of chats",
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
                            "$ref": "#/components/schemas/Chat"
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
                      "example": "Param channel_account_id must be a valid UUID"
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
      "queryParam_limit_200": {
        "description": "Max number of rows returned",
        "in": "query",
        "name": "limit",
        "schema": {
          "default": 200,
          "maximum": 200,
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
      "Chat": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "contact_id": {
            "$ref": "#/components/schemas/ID"
          },
          "user_id": {
            "$ref": "#/components/schemas/ID"
          },
          "status": {
            "type": "string",
            "enum": [
              "OPEN",
              "CLOSED",
              "WAITING",
              "SNOOZED",
              "REOPENED"
            ],
            "example": "OPEN"
          },
          "seen": {
            "type": "boolean",
            "example": false
          },
          "unread": {
            "type": "boolean",
            "example": true
          },
          "replied": {
            "type": "boolean",
            "example": false
          },
          "unseen_count": {
            "type": "integer",
            "example": 3
          },
          "last_message_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "last_response_at": {
            "type": "string",
            "format": "date-time",
            "nullable": true,
            "example": "2024-01-15T09:00:00.000Z"
          },
          "last_status_at": {
            "type": "string",
            "format": "date-time",
            "nullable": true,
            "example": "2024-01-15T10:30:00.000Z"
          },
          "first_response_at": {
            "type": "string",
            "format": "date-time",
            "nullable": true,
            "example": "2024-01-14T08:00:00.000Z"
          },
          "channel_account_id": {
            "$ref": "#/components/schemas/ID"
          },
          "team_id": {
            "type": "string",
            "format": "uuid",
            "nullable": true,
            "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8"
          },
          "closed_at": {
            "type": "string",
            "format": "date-time",
            "nullable": true,
            "example": null,
            "description": "Timestamp when the chat was closed"
          },
          "first_customer_message_at": {
            "type": "string",
            "format": "date-time",
            "nullable": true,
            "example": null,
            "description": "Timestamp of the first customer message in the chat"
          },
          "close_window_at": {
            "type": "string",
            "format": "date-time",
            "nullable": true,
            "example": "2024-01-16T10:30:00.000Z",
            "description": "Timestamp when the WhatsApp messaging window closes (24h after last customer message)"
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