# List groups

Retrieve a paginated list of groups

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
      "name": "Groups",
      "description": "Operations related to managing deals"
    }
  ],
  "paths": {
    "/v1/groups": {
      "get": {
        "summary": "List groups",
        "tags": [
          "Groups"
        ],
        "description": "Retrieve a paginated list of groups",
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
          }
        ],
        "responses": {
          "200": {
            "description": "A list of groups",
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
                            "$ref": "#/components/schemas/Group"
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
      "DateTime": {
        "type": "string",
        "format": "date-time",
        "example": "2020-01-01T14:15:00.000000+00:00"
      },
      "Group": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "name": {
            "type": "string",
            "example": "Group name"
          },
          "archived_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "archived_by": {
            "$ref": "#/components/schemas/ID"
          }
        }
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