# Send document message

Send a document message via WhatsApp Official. The document URL is sent directly to the Meta API. Filename is required and will be displayed to the recipient. Returns immediately with QUEUED status.

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
    "/v2/messages/document": {
      "post": {
        "summary": "Send document message",
        "tags": [
          "Messages"
        ],
        "description": "Send a document message via WhatsApp Official. The document URL is sent directly to the Meta API. Filename is required and will be displayed to the recipient. Returns immediately with QUEUED status.",
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
                  "url",
                  "filename"
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
                    "description": "UUID of the contact to send the document to",
                    "example": "550e8400-e29b-41d4-a716-446655440002"
                  },
                  "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "Direct URL of the document to send",
                    "example": "https://example.com/report.pdf"
                  },
                  "filename": {
                    "type": "string",
                    "description": "Filename displayed to the recipient",
                    "example": "report.pdf"
                  },
                  "caption": {
                    "type": "string",
                    "description": "Optional caption for the document",
                    "example": "Monthly report"
                  },
                  "chat_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Optional UUID of an existing chat. If not provided, the system will find or create a chat automatically.",
                    "example": "550e8400-e29b-41d4-a716-446655440003"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Document message queued for sending",
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
                      "example": "Param filename is required"
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
                      "example": "Channel account not found"
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