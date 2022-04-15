import json

def load_json(file_path: str) -> dict:
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)

        if type(data) != type({}):
            raise TypeError("TypeError")

        return data

    except FileNotFoundError as error:
        print(f"JSON ERROR: {error}")

    except TypeError as error:
        print(f"JSON ERROR: {error} (File: {file_path}) (Data: {data})")

    except Exception as error:
        print(f"JSON ERROR: {error} (File: {file_path})")

def dump_json(data: dict, file_path: str, pretty=False) -> None:

    indent = 0
    if pretty: indent = 4

    try: 
        if type(data) != type({}):
            raise TypeError("TypeError")

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=indent)

    except FileNotFoundError as error:
        print(f"JSON ERROR: {error}")

    except TypeError as error:
        print(f"JSON ERROR: {error} (File: {file_path}) (Data: {data})")

    except Exception as error:
        print(f"JSON ERROR: {error} (File: {file_path}) ")
