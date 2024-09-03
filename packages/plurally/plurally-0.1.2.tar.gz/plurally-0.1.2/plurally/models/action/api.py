
openapi_json_schema = {
    "openapi": "3.1.0",
    "info": {"title": "Plurally", "version": "0.1.0"},
    "paths": {
        "/time": {
            "get": {
                "summary": "Read Time",
                "operationId": "read_time_time_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TimeRead"}
                            }
                        },
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "TimeRead": {
                "properties": {"val": {"type": "string", "title": "Val"}},
                "type": "object",
                "required": ["val"],
                "title": "TimeRead",
            }
        }
    },
}


# parse response scheema into a pydantic model


