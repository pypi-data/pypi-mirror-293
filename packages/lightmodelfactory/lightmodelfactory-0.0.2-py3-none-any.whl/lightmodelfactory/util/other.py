import subprocess

def get_port(start_port):
    def is_port_open(port):
            try:
                cmd = f'apt install net-tools'
                subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                cmd = f"netstat -anlp | grep :{port}"
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                if result.stdout:
                    return True
            except subprocess.CalledProcessError:
                return False
            return False
    while is_port_open(start_port):
        start_port = start_port + 1
    return start_port

def dataclass_to_cli_args(data_class_instance):
    from dataclasses import fields
    fieldss = fields(data_class_instance)
    cli_args = []
    for field in fieldss:
        arg_name = f"--{field.name}"
        key = getattr(data_class_instance, field.name)
        if key is not None:
            cli_args.append(f"{arg_name} {getattr(data_class_instance, field.name)}")
    return " ".join(cli_args)