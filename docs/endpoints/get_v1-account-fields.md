# List fields

Retrieve a list of fields

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
  "paths": {
    "/v1/account/fields": {
      "get": {
        "summary": "List fields",
        "tags": [
          "Account"
        ],
        "description": "Retrieve a list of fields",
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          }
        ],
        "responses": {
          "200": {
            "description": "A list of fields",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [
                    {
                      "type": "object",
                      "properties": {
                        "data": {
                          "type": "array",
                          "items": {
                            "$ref": "#/components/schemas/AccountFields"
                          }
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
      }
    },
    "schemas": {
      "AccountFields": {
        "type": "object",
        "properties": {
          "groups": {
            "type": "object",
            "properties": {
              "DEAL": {
                "type": "object",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "CONTACT": {
                "type": "object",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "ORGANIZATION": {
                "type": "object",
                "additionalProperties": {
                  "type": "string"
                }
              }
            }
          },
          "fields": {
            "type": "object",
            "properties": {
              "DEAL": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "example": "TEXT"
                  },
                  "group": {
                    "type": "string",
                    "example": "default"
                  },
                  "label": {
                    "type": "string",
                    "example": "notes"
                  }
                }
              },
              "CONTACT": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "example": "TEXT"
                  },
                  "group": {
                    "type": "string",
                    "example": "default"
                  },
                  "label": {
                    "type": "string",
                    "example": "notes"
                  }
                }
              },
              "ORGANIZATION": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "example": "TEXT"
                  },
                  "group": {
                    "type": "string",
                    "example": "default"
                  },
                  "label": {
                    "type": "string",
                    "example": "notes"
                  }
                }
              }
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