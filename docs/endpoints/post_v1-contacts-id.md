# Update contact

Update a single contact

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
      "name": "Contacts",
      "description": "Operations related to managing contacts"
    }
  ],
  "paths": {
    "/v1/contacts/{id}": {
      "post": {
        "summary": "Update contact",
        "tags": [
          "Contacts"
        ],
        "description": "Update a single contact",
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          },
          {
            "$ref": "#/components/parameters/pathParam_id"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ContactCreateSchema"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Contact updated",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "$ref": "#/components/schemas/ID"
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
      "ContactCreateSchema": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "example": "Contact name"
          },
          "ddi": {
            "type": "string",
            "example": "+55"
          },
          "phone": {
            "type": "string",
            "example": "48999999999"
          },
          "email": {
            "type": "string",
            "example": "contact@email.com"
          },
          "username": {
            "type": "string",
            "example": "Instagram ID"
          },
          "fields": {
            "type": "object",
            "additionalProperties": {
              "type": "string"
            },
            "properties": {
              "organization": {
                "type": "object",
                "additionalProperties": {
                  "type": "string"
                }
              }
            }
          }
        }
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