from typing import Union

class PdxObject:

    def __init__(self, o: Union[list, dict]):
        self.data = o

    def __str__(self):
        return json_to_pdx(self.data)

def json_to_pdx(data, indent=0):
    if isinstance(data, str): return " " * 4 * indent + data 
    elif isinstance(data, bool): return " " * 4 * indent + ("yes" if data else "no")
    elif isinstance(data, int): return " " * 4 * indent + str(data)
    elif isinstance(data, list): return '\n'.join([json_to_pdx(item, indent) for item in data])
    elif isinstance(data, dict): return '\n'.join([f"{' ' * 4 * indent}{k} = {{\n{json_to_pdx(v, indent + 1)}\n{' ' * 4 * indent}}}" if isinstance(v, (dict, list)) else f"{' ' * 4 * indent}{k} = {json_to_pdx(v, 0)}" for k, v in data.items()])
    elif isinstance(data, PdxObject): return json_to_pdx(data.data, indent)


def test():
    json_data = {
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
    }

    print(json_to_pdx(json_data))