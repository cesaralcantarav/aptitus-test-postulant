import os
import click
import json
import uuid
from datetime import datetime

from cli.cli import pass_context
from cli.utils import xls
from cli.utils.config import get_endpoint_postulant
from cli.utils.file import get_file_from_storage
from cli.utils.file import put_file_to_storage
from cli.utils.file import validate_exist_file
from cli.utils import constants
from cli.utils.report import generate_report
from cli.utils.report import get_report_name
from cli.utils.report import save_report_to_file
from cli.utils.report import get_output_dir
from cli.schemas.postulant import PostulantRegRapRequestSchema
from cli.api.postulant import PostulantApi
from cli.api.postulant import validate_status_code

def prepare_headers():
    headers = { 
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin':'test-Qa'
    }
    return headers

def prepare_payload(data):
    schema = PostulantRegRapRequestSchema()
    payload = dict(
        txtName	= data[constants.REQUEST_COLUMN_TXT_NAME],
        txtFirstLastName = data[constants.REQUEST_COLUMN_TXT_FIRST_LAST_NAME],
        txtSecondLastName = data[constants.REQUEST_COLUMN_TXT_SECOND_LAST_NAME],
        txtEmail = data[constants.REQUEST_COLUMN_TXT_EMAIL],
        pswd = data[constants.REQUEST_COLUMN_PSWD],
        txtJob = data[constants.REQUEST_COLUMN_TXT_JOB],
        selLocation = data[constants.REQUEST_COLUMN_SEL_LOCATION]
    )
    return schema.dump(payload)

def validate_payload(payload):
    if len(payload.errors) != 0 :
        raise Exception(payload.errors)
           
def process(sheet, bank, endpoint):
    results = []
    api = PostulantApi(endpoint)
    headers = prepare_headers()
    api.set_headers(headers)
    for row in range(1, sheet.nrows):
        try:
            row_values = sheet.row_values(row)
            payload = prepare_payload(row_values)
            validate_payload(payload)
            
            response = api.registro_rapido(payload.data)

            click.echo("fila: {} - {} - {} - {} - {}".format(
                row - 1, 
                row_values[constants.REQUEST_COLUMN_TXT_NAME],
                row_values[constants.REQUEST_COLUMN_TXT_FIRST_LAST_NAME],
                row_values[constants.REQUEST_COLUMN_TXT_SECOND_LAST_NAME],
                row_values[constants.REQUEST_COLUMN_TXT_EMAIL]))
            validate_status_code(response)
            response_json = response.json()
            code = response_json['code']
            message = response_json['message']
            data = response_json['data']
            payload_request = json.dumps(payload.data, indent=4)
            payload_response = json.dumps(response_json, indent=4)
            results.append({
                "status_code": response.status_code, 
                "response_code": code,
                "response_message": message,
                "response":{
                    "id": str(uuid.uuid4()),
                    "payload": payload_response  
                },
                "request": {
                    "id": str(uuid.uuid4()),
                    "payload": payload_request
                }
            })

            click.echo("Payload Request:")
            click.echo(payload_request)
            
            click.echo("Payload Response:")
            click.echo(payload_response)

        except Exception as e:
            click.echo(e)

    return results

def prepare_data(operation, executed_at, endpoint, results):
    data = {
        'operation': operation,
        'executed_at': executed_at, 
        'endpoint': endpoint, 
        'results': results
    }
    return data

@click.command()
@click.option('--env', default='dev',  help='Ambiente de despliegue (dev/dev1a/pre/prod).')
@click.option('--input_file', default='data-stage.xlsx',  help='Archivo datos de entrada en formato Excel.')
@click.option('--storage', default='local',  help='Almacenamiento de los archivos inputs/outputs (local/s3).')
@pass_context
def command(ctx, **kwargs):
    """Test Registro Rapido de Postulantes."""
    click.echo("=== Iniciando Test Registro Rapido de Postulante  ===")
    try:
        click.echo("Storage Inputs/Outputs File: {}".format(kwargs['storage'])) 
        get_file_from_storage(
            ctx.config, 
            kwargs['env'], 
            kwargs['storage'], 
            kwargs['input_file']
        )

        endpoint = get_endpoint_postulant(ctx.config, kwargs['env'])
        click.echo("Endpoint: {}".format(endpoint))

        input_file = kwargs['input_file']
        click.echo("Input File: {}".format(input_file))

        validate_exist_file(input_file)
        wb = xls.get_workbook(input_file)

        sh = xls.get_sheet_by_name(wb, constants.SHEET_REGISTRO)
        results = process(sh, bank, endpoint)
        
        click.echo("Generate html report with results of Registro Rapido Ajax")
        data = prepare_data(
            constants.TEST_OPERATION_REGISTRO_RAPIDO, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            endpoint, 
            results
        )
        report_html = generate_report("report.html", data)
        
        report_name = get_report_name(f"rpt_registro_rapido_ajax")
        click.echo("Storing report {} into {}".format(report_name, kwargs['storage']))
        
        output_dir = get_output_dir(kwargs['storage'])
        output_file = '{}/{}'.format(output_dir, report_name)
        save_report_to_file(output_file, report_html)

        put_file_to_storage(
            ctx.config, 
            kwargs['env'], 
            kwargs['storage'], 
            output_file
        )

    except Exception as e:
        click.echo(str(e))

    click.echo("=== Finalizando Test Registro Rapido de Postulante ===")
