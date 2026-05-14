# List contacts

Retrieve a paginated list of contacts

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
    "/v1/contacts": {
      "get": {
        "summary": "List contacts",
        "tags": [
          "Contacts"
        ],
        "description": "Retrieve a paginated list of contacts",
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          },
          {
            "$ref": "#/components/parameters/queryParam_limit"
          },
          {
            "$ref": "#/components/parameters/queryParam_offset"
          },
          {
            "$ref": "#/components/parameters/queryParam_page"
          },
          {
            "description": "Filter by origin ID",
            "in": "query",
            "name": "origin_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
            }
          },
          {
            "description": "Filter by contact name",
            "in": "query",
            "name": "name",
            "schema": {
              "type": "string",
              "example": "Contact name"
            }
          },
          {
            "description": "Filter by contact ddi",
            "in": "query",
            "name": "ddi",
            "schema": {
              "type": "string",
              "example": "55"
            }
          },
          {
            "description": "Filter by contact phone",
            "in": "query",
            "name": "phone",
            "schema": {
              "type": "string",
              "example": "999999999"
            }
          },
          {
            "description": "Filter by contact e-mail",
            "in": "query",
            "name": "email",
            "schema": {
              "type": "string",
              "example": "contact@email.com"
            }
          },
          {
            "description": "Filter by contact tag IDs using OR operator. Separated by ','",
            "in": "query",
            "name": "tag_ids",
            "schema": {
              "type": "string",
              "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8,99999999-d77b-4e8b-9d35-fd43e972b999"
            }
          },
          {
            "description": "Filter by contact tag names using OR operator. Separated by ','",
            "in": "query",
            "name": "tag_names",
            "schema": {
              "type": "string",
              "example": "tag1,tag2,tag3"
            }
          },
          {
            "description": "Filter by contact fields. Can be used multiple times for each field",
            "in": "query",
            "name": "fields",
            "style": "deepObject",
            "schema": {
              "type": "object"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "A list of contacts",
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
                            "$ref": "#/components/schemas/Contact"
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
      },
      "queryParam_limit": {
        "description": "Max number of rows returned",
        "in": "query",
        "name": "limit",
        "schema": {
          "default": 200,
          "maximum": 1000,
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
      "Contact": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "updated_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "name": {
            "type": "string",
            "example": "Contact name"
          },
          "email": {
            "type": "string",
            "example": "contact@email.com"
          },
          "organization": {
            "type": "string",
            "example": "Organization name"
          },
          "instagram": {
            "type": "string",
            "example": "Instagram ID"
          },
          "tags": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Tag"
            }
          },
          "fields": {
            "$ref": "#/components/schemas/Fields"
          },
          "fullPhone": {
            "$ref": "#/components/schemas/FullPhone"
          }
        }
      },
      "DateTime": {
        "type": "string",
        "format": "date-time",
        "example": "2020-01-01T14:15:00.000000+00:00"
      },
      "Fields": {
        "type": "object"
      },
      "FullPhone": {
        "type": "string",
        "example": "+5548999999999"
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
      },
      "Tag": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "name": {
            "type": "string",
            "example": "Tag name"
          },
          "color": {
            "$ref": "#/components/schemas/TagColor"
          }
        }
      },
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