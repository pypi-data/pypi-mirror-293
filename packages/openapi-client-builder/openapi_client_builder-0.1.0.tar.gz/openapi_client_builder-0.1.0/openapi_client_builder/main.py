import typer
from .tools import get_openapi_json, output_file, schemas2type, server2client

app = typer.Typer(no_args_is_help=True)

@app.command()
def type(host:str='127.0.0.1',port:str='8000',path='/api/openapi.json', url=None, output:str='./dist', name='api.types.d.ts'):
    data_dict = get_openapi_json(url if url else f'http://{host}:{port}{path}')
    data_schemas = data_dict['components']['schemas']
    schemas = schemas2type(data_schemas)
    output_file(name, schemas)

@app.command()
def api(host:str='127.0.0.1',port:str='8000',path='/api/openapi.json', url=None, output:str='./dist', name='db_api.d.ts'):
    data_dict = get_openapi_json(url if url else f'http://{host}:{port}{path}')
    data_paths = data_dict['paths']
    _api = server2client(data_paths)
    output_file('db_api.ts', _api)