# Send template message

Send a WhatsApp message template (HSM). Template messages can be sent at any time, even when the 24-hour messaging window is closed. The template must be APPROVED by Meta and belong to the specified channel account. Variable placeholders ({{1}}, {{2}}, etc.) in the template are replaced with the provided parameter values.

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
    "/v2/messages/template": {
      "post": {
        "summary": "Send template message",
        "tags": [
          "Messages"
        ],
        "description": "Send a WhatsApp message template (HSM). Template messages can be sent at any time, even when the 24-hour messaging window is closed. The template must be APPROVED by Meta and belong to the specified channel account. Variable placeholders ({{1}}, {{2}}, etc.) in the template are replaced with the provided parameter values.",
        "servers": [
          {
            "url": "https://api.clint.digital/v2",
            "description": "Production API (v2)"
          }
        ],
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "channel_account_id",
                  "contact_id",
                  "template_id"
                ],
                "properties": {
                  "channel_account_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "UUID of the WhatsApp Official channel account",
                    "example": "550e8400-e29b-41d4-a716-446655440001"
                  },
                  "contact_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "UUID of the contact to send the template to",
                    "example": "550e8400-e29b-41d4-a716-446655440002"
                  },
                  "template_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "UUID of the message template to send. Must have APPROVED status.",
                    "example": "550e8400-e29b-41d4-a716-446655440010"
                  },
                  "chat_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically.",
                    "example": "550e8400-e29b-41d4-a716-446655440003"
                  },
                  "parameters": {
                    "type": "object",
                    "description": "Variable values to replace {{1}}, {{2}}, etc. in the template components. Each array position maps to the corresponding placeholder number.",
                    "properties": {
                      "header": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        },
                        "description": "Values for header component variables",
                        "example": [
                          "John"
                        ]
                      },
                      "body": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        },
                        "description": "Values for body component variables",
                        "example": [
                          "John",
                          "12345",
                          "2024-01-15"
                        ]
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Template message queued for sending",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer",
                      "example": 200
                    },
                    "data": {
                      "type": "object",
                      "properties": {
                        "success": {
                          "type": "boolean",
                          "example": true
                        },
                        "message_id": {
                          "type": "string",
                          "format": "uuid",
                          "example": "550e8400-e29b-41d4-a716-446655440099"
                        },
                        "chat_id": {
                          "type": "string",
                          "format": "uuid",
                          "example": "550e8400-e29b-41d4-a716-446655440003"
                        },
                        "status": {
                          "type": "string",
                          "enum": [
                            "QUEUED"
                          ],
                          "example": "QUEUED"
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Validation error",
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
                      "example": "Template must have APPROVED status"
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
            "description": "Resource not found",
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
                      "example": "Message template not found"
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