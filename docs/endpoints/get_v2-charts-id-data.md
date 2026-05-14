# Get single chart data

Execute a single chart query and return its data.

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
    "/v2/charts/{id}/data": {
      "get": {
        "summary": "Get single chart data",
        "tags": [
          "Dashboards"
        ],
        "description": "Execute a single chart query and return its data.",
        "parameters": [
          {
            "$ref": "#/components/parameters/headerParamXAPIKey"
          },
          {
            "$ref": "#/components/parameters/pathParam_id"
          },
          {
            "description": "Start date filter (inclusive)",
            "in": "query",
            "name": "date_start",
            "schema": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
              "example": "2026-01-01"
            }
          },
          {
            "description": "End date filter (inclusive)",
            "in": "query",
            "name": "date_end",
            "schema": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
              "example": "2026-12-31"
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
            "description": "Filter by origin ID",
            "in": "query",
            "name": "origin_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
            }
          },
          {
            "description": "Filter by origin group ID",
            "in": "query",
            "name": "origin_group_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
            }
          },
          {
            "description": "Filter by tag ID",
            "in": "query",
            "name": "tag_id",
            "schema": {
              "$ref": "#/components/schemas/ID"
            }
          },
          {
            "description": "Timezone for date calculations",
            "in": "query",
            "name": "timezone",
            "schema": {
              "type": "string",
              "maxLength": 50,
              "example": "America/Sao_Paulo"
            }
          },
          {
            "description": "Limit rows returned (applies to table/list chart types)",
            "in": "query",
            "name": "limit",
            "schema": {
              "type": "integer",
              "minimum": 1,
              "maximum": 15000
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Chart data",
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
                      "$ref": "#/components/schemas/ChartData"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Validation error (e.g. invalid date format)"
          },
          "401": {
            "description": "Authentication error - invalid or missing api-token"
          },
          "404": {
            "description": "Chart not found"
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
      "ChartData": {
        "type": "object",
        "description": "Chart data returned from a Cube.js query. The result format varies by chart type.",
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
            "example": "number"
          },
          "result": {
            "description": "Chart result data. Format depends on chart type: number types return {value}, table types return {columns, rows}, series types (line, bar, pie, etc.) return an array of series objects.",
            "oneOf": [
              {
                "type": "object",
                "description": "Number/KPI chart result",
                "properties": {
                  "value": {
                    "example": 42
                  }
                }
              },
              {
                "type": "object",
                "description": "Table chart result",
                "properties": {
                  "columns": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "key": {
                          "type": "string"
                        },
                        "title": {
                          "type": "string"
                        },
                        "type": {
                          "type": "string"
                        }
                      }
                    }
                  },
                  "rows": {
                    "type": "array",
                    "items": {
                      "type": "object"
                    }
                  }
                }
              },
              {
                "type": "array",
                "description": "Series chart result (line, bar, pie, etc.)",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "data": {
                      "type": "array",
                      "items": {
                        "type": "object"
                      }
                    }
                  }
                }
              }
            ]
          },
          "error": {
            "type": "string",
            "description": "Present instead of result when the chart query failed",
            "example": "Failed to fetch chart data"
          }
        }
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