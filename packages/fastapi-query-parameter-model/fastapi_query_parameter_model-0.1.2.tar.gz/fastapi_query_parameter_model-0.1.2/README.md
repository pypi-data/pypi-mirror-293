# QueryParameterModel

**QueryParameterModel** is a Python library designed to simplify the parsing of query parameters in FastAPI applications. Utilizing Pydantic for validation, this package offers a streamlined approach to handling query parameters, including automatic conversion of camelCase query parameters from the URL to Python's snake_case convention.

## Features

- **CamelCase to SnakeCase Conversion**: Automatically convert camelCase query parameters from the URL to Python's snake_case convention.
- **Flexible Parsing**: Parse query parameters into a full Pydantic model, which is particularly useful when handling multiple parameters in FastAPI routes.
- **List Support**: Easily handle query parameters that are lists.
- **FastAPI Integration**: Seamlessly integrate with FastAPI’s dependency injection system.

## Installation

You can install **QueryParameterModel** via pip:

```bash
pip install fastapi-query-parameter-model
```

## Usage

### Define Your Model

Create a model by inheriting from `QueryParameterModel` and define your query parameters. CamelCase query parameters from the URL will be converted to snake_case in your model.

```python
from fastapi_query_parameter_model import QueryParameterModel
from fastapi import Query

class SmallTestQueryParamsModels(QueryParameterModel):
    title: str
    age: int = 0
    is_major: bool = Query(alias="isMajor", default=False)
    array: list[str] = []
```

### Integrate with FastAPI

Use FastAPI’s dependency injection to parse query parameters into the model:

```python
from fastapi import FastAPI, Depends
from fastapi_query_parameter_model import QueryParameterModel

app = FastAPI()

@app.get("/small-test")
async def small_test(
    query_params: SmallTestQueryParamsModels = Depends(SmallTestQueryParamsModels.parser)
):
    return query_params.model_dump()
```

### Example Usage

Here are two example endpoints demonstrating how to use the models with FastAPI:

```python
from fastapi import FastAPI, Depends, Query
from fastapi_query_parameter_model import QueryParameterModel

app = FastAPI()

class SmallTestQueryParamsModels(QueryParameterModel):
    title: str
    age: int = 0
    is_major: bool = Query(alias="isMajor", default=False)
    array: list[str] = []

class FullTestQueryParamsModels(QueryParameterModel):
    title: str
    age: int = 0
    is_major: bool = Query(alias="isMajor", default=False)
    str_array: list[str] = Query(alias="strArray", default=[])
    int_array: list[int] = Query(alias="intArray", default=[])

@app.get("/small-test")
async def small_test(
    query_params: SmallTestQueryParamsModels = Depends(SmallTestQueryParamsModels.parser)
):
    return query_params.model_dump()

@app.get("/full-test")
async def full_test(
    query_params: FullTestQueryParamsModels = Depends(FullTestQueryParamsModels.parser)
):
    return query_params.model_dump()
```

### Example Response

Using the following query : `small-test?title=thisATitle&isMajor=true&array[]=a&array[]=b&array[]=c`

For the `/small-test` route, a sample response might look like this:

```json
{
  "title": "thisATitle",
  "age": 0,
  "is_major": true,
  "array": ["a", "b", "c"]
}
```

This response shows how the query parameters are parsed and returned as a Pydantic model instance with snake_case attributes.


### Methods

- **`parser(request: Request)`**: Parses the query parameters from a FastAPI `Request` object and returns an instance of the model with converted snake_case attributes.
- **`model_dump()`**: This is a native pydantic function, only used in this example, to show the result of the parsed query parameters model

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push your branch and open a pull request.

Please ensure that your code adheres to the existing style and includes tests where applicable.

## License

**QueryParameterModel** is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, feel free to open an issue on the [GitHub repository](https://github.com/PierroD/fastapi-query-parameter-model).

---

This revised README should more accurately reflect the functionality of your `QueryParameterModel` and help users understand its features and usage. Let me know if there are any other adjustments or additional details you’d like to include!