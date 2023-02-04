# PrintRAPI

PrintRAPI is an API for printing receipts on receipt printing devices. It is built on top of the FastAPI and slowapi libraries. It allows users to print text, markdown documents, images, and cut the paper.

## Setup

To get started, you will need to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

You will also need to set the environment variable `API_SECRET` to a secret of your choosing.

## Usage

PrintRAPI provides the following endpoints:

- `/print` for printing text
- `/pmarkdown` for printing markdown documents
- `/part` for printing images
- `/cut` for cutting the paper

The API is rate limited to 3 requests per minute.

To use the API, you will need to provide an `x-PrintRAPI-key` header with a value matching the `API_SECRET` environment variable.

### Examples

Printing text:

```bash
curl -X GET \
  'http://localhost:8899/print?text=Hello%20World' \
  -H 'x-PrintRAPI-key: <your secret>'
```

Printing markdown:

```bash
curl -X GET \
  'http://localhost:8899/pmarkdown?doc=%2A%20Hello%20World%2A' \
  -H 'x-PrintRAPI-key: <your secret>'
```

Printing an image:

```bash
curl -X GET \
  'http://localhost:8899/image' \
  -H 'x-PrintRAPI-key: <your secret>'
```

Cutting the paper:

```bash
curl -X GET \
  'http://localhost:8899/cut' \
  -H 'x-PrintRAPI-key: <your secret>'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
