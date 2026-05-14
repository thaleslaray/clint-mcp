# List message templates

Retrieve a paginated list of message templates linked to a WhatsApp Official channel account. The channel_account_id query parameter is required and must belong to the authenticated owner.

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
    "/v2/message-templates": {
      "get": {
        "summary": "List message templates",
        "tags": [
          "Message Templates"
        ],
        "description": "Retrieve a paginated list of message templates linked to a WhatsApp Official channel account. The channel_account_id query parameter is required and must belong to the authenticated owner.",
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
            "description": "UUID of the channel account (required)",
            "in": "query",
            "name": "channel_account_id",
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
            "description": "A paginated list of message templates",
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
                            "$ref": "#/components/schemas/MessageTemplate"
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
            "description": "Missing or invalid channel_account_id",
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
                      "example": "Query param channel_account_id is required"
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
            "description": "Channel account not found",
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