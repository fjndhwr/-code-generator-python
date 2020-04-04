import yaml
cf = None


def read_yaml():
    with open("build/application.yml", 'rb') as f:
        cf = f.read()
    cf = yaml.load(cf)
    return cf