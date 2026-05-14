# Create deal

Create a new Deal

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
      "name": "Deals",
      "description": "Operations related to managing deals"
    }
  ],
  "paths": {
    "/v1/deals": {
      "post": {
        "summary": "Create deal",
        "tags": [
          "Deals"
        ],
        "description": "Create a new Deal",
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
                "$ref": "#/components/schemas/DealCreateSchema"
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Deal created",
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
      }
    },
    "schemas": {
      "DealCreateSchema": {
        "type": "object",
        "properties": {
          "origin_id": {
            "$ref": "#/components/schemas/ID"
          },
          "name": {
            "type": "string",
            "example": "Contact name"
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
          "value": {
            "type": "number",
            "example": "200.5"
          },
          "stage_id": {
            "$ref": "#/components/schemas/ID"
          },
          "user_id": {
            "$ref": "#/components/schemas/ID"
          },
          "contact_id": {
            "$ref": "#/components/schemas/ID"
          },
          "fields": {
            "type": "object",
            "additionalProperties": {
              "type": "string"
            },
            "properties": {
              "contact": {
                "type": "object",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "organization": {
                "type": "object",
                "additionalProperties": {
                  "type": "string"
                }
              }
            }
          }
        },
        "required": [
          "origin_id"
        ]
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