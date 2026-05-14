# List contact attachments

Retrieve a paginated list of attachments (documents) for a specific contact. Each attachment includes a public document URL that can be used directly for download or rendering.

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
    "/v1/contacts/{id}/attachments": {
      "get": {
        "summary": "List contact attachments",
        "tags": [
          "Contacts"
        ],
        "description": "Retrieve a paginated list of attachments (documents) for a specific contact. Each attachment includes a public document URL that can be used directly for download or rendering.",
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          },
          {
            "$ref": "#/components/parameters/pathParam_id"
          },
          {
            "$ref": "#/components/parameters/queryParam_limit_100"
          },
          {
            "$ref": "#/components/parameters/queryParam_page"
          }
        ],
        "responses": {
          "200": {
            "description": "A paginated list of contact attachments",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [
                    {
                      "$ref": "#/components/schemas/Paginated"
                    },
                    {
                      "type": "object",
                      "properties": {
                        "data": {
                          "type": "array",
                          "items": {
                            "$ref": "#/components/schemas/ContactAttachment"
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
            "description": "Bad Request",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string",
                      "example": "Param contactId must be a valid UUID"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "Contact not found",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string",
                      "example": "Contact not found"
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
      "queryParam_limit_100": {
        "description": "Max number of rows returned",
        "in": "query",
        "name": "limit",
        "schema": {
          "default": 100,
          "maximum": 100,
          "minimum": 1,
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
      "ContactAttachment": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "contact_id": {
            "$ref": "#/components/schemas/ID"
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "updated_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "uploaded_by": {
            "type": "object",
            "properties": {
              "id": {
                "$ref": "#/components/schemas/ID"
              },
              "first_name": {
                "type": "string",
                "example": "Maria"
              },
              "last_name": {
                "type": "string",
                "example": "Silva"
              }
            }
          },
          "document": {
            "type": "object",
            "properties": {
              "id": {
                "$ref": "#/components/schemas/ID"
              },
              "name": {
                "type": "string",
                "example": "contract-signed"
              },
              "file_name": {
                "type": "string",
                "example": "contract-signed.pdf"
              },
              "url": {
                "type": "string",
                "format": "uri",
                "example": "https://file.clint.digital/.../contract-signed.pdf"
              },
              "extension": {
                "type": "string",
                "example": "pdf"
              },
              "file_size": {
                "type": "integer",
                "example": 204800,
                "description": "File size in bytes"
              }
            }
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
      },
      "Paginated": {
        "type": "object",
        "properties": {
          "status": {
            "type": "integer",
            "example": "200",
            "description": "Response status"
          },
          "totalCount": {
            "type": "integer",
            "example": "50",
            "description": "Total items based on current filters"
          },
          "page": {
            "type": "integer",
            "example": "1",
            "description": "Current page"
          },
          "totalPages": {
            "type": "integer",
            "example": "10",
            "description": "Total pages based on current filters"
          },
          "hasNext": {
            "type": "boolean",
            "example": "true",
            "description": "Indicates that has next page"
          },
          "hasPrevious": {
            "type": "boolean",
            "example": "true",
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