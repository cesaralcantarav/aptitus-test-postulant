import yaml

def read_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

def get_endpoint_postulant(config, env):
    return config['endpoint']['postulant'][env]
