import yaml
cf = None


def read_yaml():
    with open("application.yml", 'rb') as f:
        cf = f.read()
    cf = yaml.load(cf)
    return cf