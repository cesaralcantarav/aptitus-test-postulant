from datetime import datetime
from cli.utils.render import render_template
from cli.utils.render import templates_dir

def get_output_dir(storage):
    output_dir = './'
    if storage == 's3':
        output_dir = '/tmp'
    return output_dir

def generate_report(name, data):
    context = {'data': data }
    return render_template(templates_dir, name, **context)

def get_report_name(name):
    return '{}_{}.html'.format(name,
                                 datetime.now().strftime('%Y%m%d_%H%M%S'))

def save_report_to_file(filename, data):
    with open(filename, 'w', encoding='utf8', errors='ignore') as f:
        f.write(data)
