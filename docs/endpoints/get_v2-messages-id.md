# Get message

Retrieve a single message by ID. Only returns messages belonging to the authenticated owner.

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
    "/v2/messages/{id}": {
      "get": {
        "summary": "Get message",
        "tags": [
          "Messages"
        ],
        "description": "Retrieve a single message by ID. Only returns messages belonging to the authenticated owner.",
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
            "$ref": "#/components/parameters/pathParam_id"
          },
          {
            "name": "content_type",
            "in": "query",
            "required": false,
            "description": "Filter message by content type",
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
            "description": "A message object",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [
                    {
                      "type": "object",
                      "properties": {
                        "status": {
                          "type": "integer",
                          "example": 200,
                          "description": "Response status"
                        }
                      }
                    },
                    {
                      "type": "object",
                      "properties": {
                        "data": {
                          "$ref": "#/components/schemas/Message"
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
                      "example": "Param ID must be a valid UUID"
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Authentication error - invalid or missing api-token"
          },
          "404": {
            "description": "Message not found",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer",
                      "example": 404
                    },
                    "message": {
                      "type": "string",
                      "example": "Message not found"
                    }
                  }
                }
              }
            }
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
      "pathParam_id": {
        "description": "UUID",
        "in": "path",
        "name": "id",
        "schema": {
          "type": "string",
          "format": "uuid",
          "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8"
        },
        "required": true
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