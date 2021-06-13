# Flask API

## Dependencies
- [flask](https://palletsprojects.com/p/flask/): Python server of choise
- [flasgger](https://github.com/flasgger/flasgger): Used to generate the swagger documentation
- [flask-expects-json](https://github.com/Fischerfredl/flask-expects-json): Used to validate JSON request data
- [jsonschema](https://github.com/Julian/jsonschema): Used to create the schema that the validator object
- [numpy](https://pypi.org/project/numpy/): Used to unit test function calculating quantile

## Set Up

1. Project setup
```sh
# clone the repo
$ git clone https://github.com/trang510/flask-api.git
# move to the project folder
$ cd flask-api
```

2. Creating virtual environment
- Install `pipenv` a global python project `pip install pipenv`
- Create a `virtual environment` for this project
    ```
    pipenv install
    ```
3. Start the server with:
    ```
   pipenv run python -m flask run
    ```

4. Visit http://localhost:5000/apidocs for the swagger documentation
   
## Tests

The code is covered by some tests, to run the tests please execute

```
pipenv run python -m unittest
```