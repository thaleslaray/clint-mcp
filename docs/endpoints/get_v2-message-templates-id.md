# Get message template

Retrieve a single message template by ID. Validates that the template belongs to a WhatsApp Official channel account owned by the authenticated user.

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
      "name": "Message Templates",
      "description": "Operations related to WhatsApp Official message templates (v2)"
    }
  ],
  "paths": {
    "/v2/message-templates/{id}": {
      "get": {
        "summary": "Get message template",
        "tags": [
          "Message Templates"
        ],
        "description": "Retrieve a single message template by ID. Validates that the template belongs to a WhatsApp Official channel account owned by the authenticated user.",
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
          }
        ],
        "responses": {
          "200": {
            "description": "A message template object",
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
                          "$ref": "#/components/schemas/MessageTemplate"
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
            "description": "Message template not found",
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
      "ID": {
        "type": "string",
        "format": "uuid",
        "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8"
      },
      "MessageTemplate": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "external_id": {
            "type": "string",
            "example": "123456789",
            "description": "Template ID on Meta"
          },
          "name": {
            "type": "string",
            "example": "welcome_message",
            "description": "Template name"
          },
          "status": {
            "type": "string",
            "enum": [
              "APPROVED",
              "PENDING",
              "REJECTED"
            ],
            "example": "APPROVED",
            "description": "Template approval status"
          },
          "language": {
            "type": "string",
            "example": "pt_BR",
            "description": "Language code"
          },
          "category": {
            "type": "string",
            "enum": [
              "MARKETING",
              "UTILITY",
              "AUTHENTICATION"
            ],
            "example": "MARKETING",
            "description": "Template category"
          },
          "components": {
            "type": "array",
            "description": "Template components (HEADER, BODY, FOOTER, BUTTONS)",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "HEADER",
                    "BODY",
                    "FOOTER",
                    "BUTTONS"
                  ],
                  "example": "BODY"
                },
                "text": {
                  "type": "string",
                  "example": "Hello {{1}}, welcome!"
                },
                "format": {
                  "type": "string",
                  "example": "TEXT"
                }
              }
            }
          },
          "variables": {
            "type": "object",
            "nullable": true,
            "description": "Variable mapping by component",
            "example": {
              "body": [
                "{{1}}"
              ]
            }
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