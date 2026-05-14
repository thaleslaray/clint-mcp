# Create tag

Create a new tag

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
      "name": "Tags",
      "description": "Operations related to managing tags"
    }
  ],
  "paths": {
    "/v1/tags": {
      "post": {
        "summary": "Create tag",
        "description": "Create a new tag",
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          }
        ],
        "tags": [
          "Tags"
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/TagCreateSchema"
              }
            }
          }
        },
        "responses": {
          "200": {
            "$ref": "#/components/responses/200"
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
    "responses": {
      "200": {
        "description": "OK"
      }
    },
    "schemas": {
      "TagColor": {
        "type": "string",
        "default": "#f44336",
        "enum": [
          "#f44336",
          "#e91e63",
          "#9c27b0",
          "#673ab7",
          "#3f51b5",
          "#2196f3",
          "#03a9f4",
          "#00bcd4",
          "#009688",
          "#4caf50",
          "#8bc34a",
          "#faa200",
          "#ff9800",
          "#ff5722",
          "#795548",
          "#607d8b"
        ]
      },
      "TagCreateSchema": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "example": "Tag name"
          },
          "color": {
            "$ref": "#/components/schemas/TagColor"
          }
        },
        "required": [
          "name",
          "color"
        ]
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