#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import yaml
from pathlib import Path

BUILD_STEP_SCRIPT_TEMPLATE = """\
#!/bin/bash

{environment}

set -e
set -x

{command}
"""

yaml_path = Path(sys.argv[1])
with yaml_path.open() as yaml_file:
    delivery_yaml = yaml_file.read()

delivery = yaml.safe_load(delivery_yaml)
build_steps = delivery['build_steps']

environment = {}

with tempfile.TemporaryDirectory(prefix='local-builder') as tempdir:

    for i, build_step in enumerate(build_steps):
        export_commands = ["export {key}={value}".format(key=key, value=value)
                        for key, value in environment.items()]

        export_lines = "\n".join(export_commands)

        script = BUILD_STEP_SCRIPT_TEMPLATE.format(environment=export_lines,
                                                   command=build_step['cmd'])
        step_sh = Path(tempdir) / 'build-step-{}.sh'.format(i)
        with open(str(step_sh), 'w') as fd:
             fd.write(script)
        step_sh.chmod(0o755)

    run_sh = Path(tempdir) / 'run.sh'
    with open(str(run_sh), 'w') as fd:
        fd.write('''#!/bin/bash
set -e
set -x
cp -va /workspace-src /workspace
cd /workspace/
''')
        for i, _ in enumerate(build_steps):
            fd.write('/build-steps/build-step-{}.sh\n'.format(i))
    run_sh.chmod(0o755)

    with subprocess.Popen(['/usr/bin/docker', 'run', '-it', '-v', '{}:/build-steps'.format(tempdir), '-v', '{}:/workspace-src'.format(yaml_path.parent.absolute()), 'ubuntu-buildbox', '/build-steps/run.sh'], stdout=subprocess.PIPE) as proc:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.decode('utf-8'), end='')


