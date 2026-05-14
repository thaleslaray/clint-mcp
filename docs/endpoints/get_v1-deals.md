# List deals

Retrieve a paginated list of deals

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
      "get": {
        "summary": "List deals",
        "tags": [
          "Deals"
        ],
        "description": "Retrieve a paginated list of deals",
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
            "description": "Filter by created_at using GTE operator",
            "in": "query",
            "name": "created_at_start",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by created_at using LTE operator",
            "in": "query",
            "name": "created_at_end",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by updated_at using GTE operator",
            "in": "query",
            "name": "updated_at_start",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by updated_at using LTE operator",
            "in": "query",
            "name": "updated_at_end",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by user ID",
            "in": "query",
            "name": "user_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
            }
          },
          {
            "description": "Filter by user e-mail",
            "in": "query",
            "name": "user_email",
            "schema": {
              "type": "string",
              "example": "user@email.com"
            }
          },
          {
            "description": "Filter by contact ID",
            "in": "query",
            "name": "contact_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
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
            "description": "Filter by tag IDs using OR operator. Separated by ','",
            "in": "query",
            "name": "tag_ids",
            "schema": {
              "type": "string",
              "example": "8feade82-d77b-4e8b-9d35-fd43e972b5c8,99999999-d77b-4e8b-9d35-fd43e972b999"
            }
          },
          {
            "description": "Filter by tag names using OR operator. Separated by ','",
            "in": "query",
            "name": "tag_names",
            "schema": {
              "type": "string",
              "example": "tag1,tag2,tag3"
            }
          },
          {
            "description": "Filter by status",
            "in": "query",
            "name": "status",
            "schema": {
              "$ref": "#/components/schemas/DealStatus"
            }
          },
          {
            "description": "Filter by stage ID",
            "in": "query",
            "name": "stage_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
            }
          },
          {
            "description": "Filter by updated_stage_at using GTE operator",
            "in": "query",
            "name": "updated_stage_at_start",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by updated_stage_at using LTE operator",
            "in": "query",
            "name": "updated_stage_at_end",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by deal fields. Can be used multiple times for each field",
            "in": "query",
            "name": "fields",
            "style": "deepObject",
            "schema": {
              "type": "object"
            }
          },
          {
            "description": "Filter by won_at using GTE operator",
            "in": "query",
            "name": "won_at_start",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by won_at using LTE operator",
            "in": "query",
            "name": "won_at_end",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by lost_at using GTE operator",
            "in": "query",
            "name": "lost_at_start",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          },
          {
            "description": "Filter by lost_at_at using LTE operator",
            "in": "query",
            "name": "lost_at_end",
            "schema": {
              "$ref": "#/components/schemas/DateTime"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "A list of deals",
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
                            "$ref": "#/components/schemas/Deal"
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