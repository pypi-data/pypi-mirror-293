# Pdxpy

Converter for Python data structures to pdxscript.

For example, 
```
"test_effect": {
    "if": [
        {
            "limit": {
                "NOT": {
                    "has_variable": "some_variable"
                }
            }
        },
        {
            "set_variable": "some_variable"
        }
    ]
}
```

gets converted to 

```
test_effect = {
    if = {
        limit = {
            NOT = { 
                has_variable = some_variable
            }
        }
        set_variable = some_variable
    }
}
```