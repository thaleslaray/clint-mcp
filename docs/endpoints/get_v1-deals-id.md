# Get deal

Retrieve a single deal by ID

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
    "/v1/deals/{id}": {
      "get": {
        "summary": "Get deal",
        "tags": [
          "Deals"
        ],
        "description": "Retrieve a single deal by ID",
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
            "description": "A deal object",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [
                    {
                      "type": "object",
                      "properties": {
                        "status": {
                          "type": "integer",
                          "example": "200",
                          "description": "Response status"
                        }
                      }
                    },
                    {
                      "type": "object",
                      "properties": {
                        "data": {
                          "$ref": "#/components/schemas/Deal"
                        }
                      }
                    }
                  ]
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
      "DateTime": {
        "type": "string",
        "format": "date-time",
        "example": "2020-01-01T14:15:00.000000+00:00"
      },
      "Deal": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "origin_id": {
            "$ref": "#/components/schemas/ID"
          },
          "user": {
            "type": "object",
            "properties": {
              "id": {
                "$ref": "#/components/schemas/ID"
              },
              "full_name": {
                "type": "string",
                "example": "User full name"
              }
            }
          },
          "contact": {
            "type": "object",
            "properties": {
              "id": {
                "$ref": "#/components/schemas/ID"
              },
              "name": {
                "type": "string",
                "example": "Contact name"
              },
              "email": {
                "type": "string",
                "example": "contact@email.com"
              },
              "phone": {
                "type": "string",
                "example": "+5548999999999"
              }
            }
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "stage_id": {
            "$ref": "#/components/schemas/ID"
          },
          "updated_stage_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "status": {
            "$ref": "#/components/schemas/DealStatus"
          },
          "won_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "won_by": {
            "$ref": "#/components/schemas/ID"
          },
          "lost_status_id": {
            "$ref": "#/components/schemas/ID"
          },
          "lost_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "lost_by": {
            "$ref": "#/components/schemas/ID"
          },
          "fields": {
            "$ref": "#/components/schemas/Fields"
          }
        }
      },
      "DealStatus": {
        "type": "string",
        "default": "OPEN",
        "enum": [
          "OPEN",
          "WON",
          "LOST"
        ]
      },
      "Fields": {
        "type": "object"
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