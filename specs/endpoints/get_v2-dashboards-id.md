# Retrieve a dashboard

Retrieve a single dashboard with its list of charts.

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
      "name": "Dashboards",
      "description": "Operations related to analytics dashboards and chart data (v2)."
    }
  ],
  "paths": {
    "/v2/dashboards/{id}": {
      "get": {
        "summary": "Retrieve a dashboard",
        "tags": [
          "Dashboards"
        ],
        "description": "Retrieve a single dashboard with its list of charts.",
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
            "description": "Dashboard details with charts",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "status": {
                      "type": "integer",
                      "example": 200
                    },
                    "data": {
                      "$ref": "#/components/schemas/Dashboard"
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Authentication error - invalid or missing api-token"
          },
          "404": {
            "description": "Dashboard not found"
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
      "Dashboard": {
        "type": "object",
        "description": "Dashboard with full chart details",
        "properties": {
          "id": {
            "$ref": "#/components/schemas/ID"
          },
          "name": {
            "type": "string",
            "example": "Sales Dashboard"
          },
          "created_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "updated_at": {
            "$ref": "#/components/schemas/DateTime"
          },
          "charts": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "$ref": "#/components/schemas/ID"
                },
                "name": {
                  "type": "string",
                  "example": "Monthly Revenue"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "line",
                    "area",
                    "bar",
                    "stackedBar",
                    "table",
                    "number",
                    "kpiPanel",
                    "pie",
                    "donut",
                    "funnel"
                  ],
                  "example": "bar"
                },
                "layout": {
                  "type": "object",
                  "description": "Chart position in the dashboard grid",
                  "properties": {
                    "x": {
                      "type": "integer"
                    },
                    "y": {
                      "type": "integer"
                    },
                    "w": {
                      "type": "integer"
                    },
                    "h": {
                      "type": "integer"
                    }
                  }
                }
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