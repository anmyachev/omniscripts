import os
import re
import subprocess
from conda.cli.python_api import run_command, Commands
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import execute_process


class CondaEnvironment:
    "Manage conda environments(create, remove, etc.)"

    def __init__(self, name):
        self.name = name

    def is_env_exist(self, name=None):
        env_name = name if name else self.name
        envs_list_cmdline = ['conda',
                             'env',
                             'list']
        _, output = execute_process(envs_list_cmdline)
        envs = re.findall(r'[^\s]+', output)
        if env_name in envs:
            return True
        return False

    def remove(self, name=None):
        env_name = name if name else self.name
        print("REMOVING CONDA ENVIRONMENT")
        remove_env_cmdline = ['conda',
                              'env',
                              'remove',
                              '--name', env_name]
        execute_process(remove_env_cmdline)
        # TODO: replace with run_command
        # run_command(Commands.REMOVE, self._add_conda_execution([], env_name),
        #             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        #             use_exception_handler=True)

    def create(self, existence_check=False, name=None, requirements_file=None):
        env_name = name if name else self.name
        if self.is_env_exist(env_name):
            if existence_check:
                return
            else:
                self.remove(env_name)
        cmdline = ['conda',
                   'env',
                   'create',
                   '--name', env_name,
                   f'--file={requirements_file}' if requirements_file else '']
        print("CREATING CONDA ENVIRONMENT")
        execute_process(cmdline, print_output=False)
        # TODO: replace with run_command
        # run_command(Commands.CREATE, self._add_conda_execution(cmdline, env_name),
        #             stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
        #             use_exception_handler=True)

    def _add_full_conda_execution(self, cmdline, name=None):
        env_name = name if name else self.name
        cmd_res = ['conda', 'run', '-n', env_name]
        cmd_res.extend(cmdline)
        return cmd_res

    def _add_conda_execution(self, cmdline, name=None):
        env_name = name if name else self.name
        cmd_res = ['-n', env_name]
        cmd_res.extend(cmdline)
        return cmd_res

    def run(self, cmdline, name=None, cwd=None, print_output=True):
        env_name = name if name else self.name
        if cwd:
            # run_command doesn't have cwd
            execute_process(self._add_full_conda_execution(cmdline, env_name), cwd=cwd,
                            print_output=print_output)
        else:
            print("CMD: ", " ".join(cmdline))
            _, _, return_code = run_command(Commands.RUN,
                                            self._add_conda_execution(cmdline, env_name),
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            use_exception_handler=True)
            if return_code != 0:
                raise Exception(f"Conda run returned {return_code}.")
