# List channel accounts

Retrieve a paginated list of WhatsApp Official channel accounts. Only returns channels with type WHATSAPP_OFFICIAL that are not deleted.

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
      "name": "Channel Accounts",
      "description": "Operations related to WhatsApp Official channel accounts (v2)"
    }
  ],
  "paths": {
    "/v2/channel-accounts": {
      "get": {
        "summary": "List channel accounts",
        "tags": [
          "Channel Accounts"
        ],
        "description": "Retrieve a paginated list of WhatsApp Official channel accounts. Only returns channels with type WHATSAPP_OFFICIAL that are not deleted.",
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
            "$ref": "#/components/parameters/queryParam_limit_100"
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
            "description": "A paginated list of channel accounts",
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
                            "$ref": "#/components/schemas/ChannelAccount"
                          }
                        }
                      }
                    }
                  ]
                }
              }
            }
          },
          "401": {
            "description": "Authentication error - invalid or missing api-token"
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
      "ChannelAccount": {
        "type": "object",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "name": {
            "type": "string",
            "example": "WhatsApp Business"
          },
          "status": {
            "type": "string",
            "enum": [
              "CONNECTED",
              "DISCONNECTED",
              "CANCELLED"
            ],
            "example": "CONNECTED"
          },
          "avatar": {
            "type": "string",
            "nullable": true,
            "example": "https://example.com/avatar.jpg"
          },
          "identifier": {
            "type": "string",
            "nullable": true,
            "example": "5548999999999"
          },
          "team_id": {
            "$ref": "#/components/schemas/ID",
            "nullable": true
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