import datetime
import os
import subprocess
import sys
import atexit
import threading
import re
import locale
import platform


message_collapses = []
import_failed_extensions = set()


def register_message_collapse(f):
    global message_collapses
    message_collapses.append(f)


def is_import_failed_extension(x):
    global import_failed_extensions
    return x in import_failed_extensions


sys.__comfyui_manager_register_message_collapse = register_message_collapse
sys.__comfyui_manager_is_import_failed_extension = is_import_failed_extension

comfyui_manager_path = os.path.dirname(__file__)
custom_nodes_path = os.path.abspath(os.path.join(comfyui_manager_path, ".."))
startup_script_path = os.path.join(comfyui_manager_path, "startup-scripts")
restore_snapshot_path = os.path.join(startup_script_path, "restore-snapshot.json")
git_script_path = os.path.join(comfyui_manager_path, "git_helper.py")

std_log_lock = threading.Lock()


class TerminalHook:
    def __init__(self):
        self.hooks = {}

    def add_hook(self, k, v):
        self.hooks[k] = v

    def remove_hook(self, k):
        if k in self.hooks:
            del self.hooks[k]

    def write_stderr(self, msg):
        for v in self.hooks.values():
            try:
                v.write_stderr(msg)
            except Exception:
                pass

    def write_stdout(self, msg):
        for v in self.hooks.values():
            try:
                v.write_stdout(msg)
            except Exception:
                pass


terminal_hook = TerminalHook()
sys.__comfyui_manager_terminal_hook = terminal_hook


def handle_stream(stream, prefix):
    stream.reconfigure(encoding=locale.getpreferredencoding(), errors='replace')
    for msg in stream:
        if prefix == '[!]' and ('it/s]' in msg or 's/it]' in msg) and ('%|' in msg or 'it [' in msg):
            if msg.startswith('100%'):
                print('\r' + msg, end="", file=sys.stderr),
            else:
                print('\r' + msg[:-1], end="", file=sys.stderr),
        else:
            if prefix == '[!]':
                print(prefix, msg, end="", file=sys.stderr)
            else:
                print(prefix, msg, end="")


def process_wrap(cmd_str, cwd_path, handler=None):
    process = subprocess.Popen(cmd_str, cwd=cwd_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    if handler is None:
        handler = handle_stream

    stdout_thread = threading.Thread(target=handler, args=(process.stdout, ""))
    stderr_thread = threading.Thread(target=handler, args=(process.stderr, "[!]"))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    return process.wait()


try:
    if '--port' in sys.argv:
        port_index = sys.argv.index('--port')
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
            postfix = f"_{port}"
    else:
        postfix = ""

    # Logger setup
    if os.path.exists(f"comfyui{postfix}.log"):
        if os.path.exists(f"comfyui{postfix}.prev.log"):
            if os.path.exists(f"comfyui{postfix}.prev2.log"):
                os.remove(f"comfyui{postfix}.prev2.log")
            os.rename(f"comfyui{postfix}.prev.log", f"comfyui{postfix}.prev2.log")
        os.rename(f"comfyui{postfix}.log", f"comfyui{postfix}.prev.log")

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    pat_tqdm = r'\d+%.*\[(.*?)\]'
    pat_import_fail = r'seconds \(IMPORT FAILED\):'
    pat_custom_node = r'[/\\]custom_nodes[/\\](.*)$'

    is_start_mode = True
    is_import_fail_mode = False

    log_file = open(f"comfyui{postfix}.log", "w", encoding="utf-8")
    log_lock = threading.Lock()

    class ComfyUIManagerLogger:
        def __init__(self, is_stdout):
            self.is_stdout = is_stdout
            self.encoding = "utf-8"

        def fileno(self):
            try:
                if self.is_stdout:
                    return original_stdout.fileno()
                else:
                    return original_stderr.fileno()
            except AttributeError:
                # Handle error
                raise ValueError("The object does not have a fileno method")

        def write(self, message):
            global is_start_mode
            global is_import_fail_mode

            if any(f(message) for f in message_collapses):
                return

            if is_start_mode:
                if is_import_fail_mode:
                    match = re.search(pat_custom_node, message)
                    if match:
                        import_failed_extensions.add(match.group(1))
                        is_import_fail_mode = False
                else:
                    match = re.search(pat_import_fail, message)
                    if match:
                        is_import_fail_mode = True
                    else:
                        is_import_fail_mode = False

                    if 'Starting server' in message:
                        is_start_mode = False

            if not self.is_stdout:
                match = re.search(pat_tqdm, message)
                if match:
                    message = re.sub(r'([#|])\d', r'\1▌', message)
                    message = re.sub('#', '█', message)
                    if '100%' in message:
                        self.sync_write(message)
                    else:
                        original_stderr.write(message)
                        original_stderr.flush()
                else:
                    self.sync_write(message)
            else:
                self.sync_write(message)

        def sync_write(self, message):
            with log_lock:
                log_file.write(message)
                log_file.flush()

            with std_log_lock:
                if self.is_stdout:
                    original_stdout.write(message)
                    original_stdout.flush()
                    terminal_hook.write_stderr(message)
                else:
                    original_stderr.write(message)
                    original_stderr.flush()
                    terminal_hook.write_stdout(message)

        def flush(self):
            log_file.flush()

            with std_log_lock:
                if self.is_stdout:
                    original_stdout.flush()
                else:
                    original_stderr.flush()

        def close(self):
            self.flush()

        def reconfigure(self, *args, **kwargs):
            pass

        # You can close through sys.stderr.close_log()
        def close_log(self):
            sys.stderr = original_stderr
            sys.stdout = original_stdout
            log_file.close()
            
    def close_log():
        sys.stderr = original_stderr
        sys.stdout = original_stdout
        log_file.close()
        
    sys.stdout = ComfyUIManagerLogger(True)
    sys.stderr = ComfyUIManagerLogger(False)

    atexit.register(close_log)
except Exception as e:
    print(f"[ComfyUI-Manager] Logging failed: {e}")


print("** ComfyUI startup time:", datetime.datetime.now())
print("** Platform:", platform.system())
print("** Python version:", sys.version)
print("** Python executable:", sys.executable)
print("** Log path:", os.path.abspath('comfyui.log'))


def check_bypass_ssl():
    try:
        import configparser
        import ssl
        config_path = os.path.join(os.path.dirname(__file__), "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)
        default_conf = config['default']

        if 'bypass_ssl' in default_conf and default_conf['bypass_ssl'].lower() == 'true':
            print(f"[ComfyUI-Manager] WARN: Unsafe - SSL verification bypass option is Enabled. (see ComfyUI-Manager/config.ini)")
            ssl._create_default_https_context = ssl._create_unverified_context  # SSL certificate error fix.
    except Exception:
        pass


check_bypass_ssl()


# Perform install
processed_install = set()
script_list_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "startup-scripts", "install-scripts.txt")
pip_list = None


def get_installed_packages():
    global pip_list

    if pip_list is None:
        try:
            result = subprocess.check_output([sys.executable, '-m', 'pip', 'list'], universal_newlines=True)
            pip_list = set([line.split()[0].lower() for line in result.split('\n') if line.strip()])
        except subprocess.CalledProcessError as e:
            print(f"[ComfyUI-Manager] Failed to retrieve the information of installed pip packages.")
            return set()
    
    return pip_list


def is_installed(name):
    name = name.strip()

    if name.startswith('#'):
        return True

    pattern = r'([^<>!=]+)([<>!=]=?)'
    match = re.search(pattern, name)
    
    if match:
        name = match.group(1)
        
    return name.lower() in get_installed_packages()


if os.path.exists(restore_snapshot_path):
    try:
        import json

        cloned_repos = []

        def msg_capture(stream, prefix):
            stream.reconfigure(encoding=locale.getpreferredencoding(), errors='replace')
            for msg in stream:
                if msg.startswith("CLONE: "):
                    cloned_repos.append(msg[7:])
                    if prefix == '[!]':
                        print(prefix, msg, end="", file=sys.stderr)
                    else:
                        print(prefix, msg, end="")

                elif prefix == '[!]' and ('it/s]' in msg or 's/it]' in msg) and ('%|' in msg or 'it [' in msg):
                    if msg.startswith('100%'):
                        print('\r' + msg, end="", file=sys.stderr),
                    else:
                        print('\r'+msg[:-1], end="", file=sys.stderr),
                else:
                    if prefix == '[!]':
                        print(prefix, msg, end="", file=sys.stderr)
                    else:
                        print(prefix, msg, end="")

        print(f"[ComfyUI-Manager] Restore snapshot.")
        cmd_str = [sys.executable, git_script_path, '--apply-snapshot', restore_snapshot_path]
        exit_code = process_wrap(cmd_str, custom_nodes_path, handler=msg_capture)

        with open(restore_snapshot_path, 'r', encoding="UTF-8") as json_file:
            info = json.load(json_file)
            for url in cloned_repos:
                try:
                    repository_name = url.split("/")[-1].strip()
                    repo_path = os.path.join(custom_nodes_path, repository_name)
                    repo_path = os.path.abspath(repo_path)

                    requirements_path = os.path.join(repo_path, 'requirements.txt')
                    install_script_path = os.path.join(repo_path, 'install.py')

                    this_exit_code = 0

                    if os.path.exists(requirements_path):
                        with open(requirements_path, 'r', encoding="UTF-8") as file:
                            for line in file:
                                package_name = line.strip()
                                if package_name and not is_installed(package_name):
                                    install_cmd = [sys.executable, "-m", "pip", "install", package_name]
                                    this_exit_code += process_wrap(install_cmd, repo_path)

                    if os.path.exists(install_script_path) and f'{repo_path}/install.py' not in processed_install:
                        processed_install.add(f'{repo_path}/install.py')
                        install_cmd = [sys.executable, install_script_path]
                        print(f">>> {install_cmd} / {repo_path}")
                        this_exit_code += process_wrap(install_cmd, repo_path)

                    if this_exit_code != 0:
                        print(f"[ComfyUI-Manager] Restoring '{repository_name}' is failed.")

                except Exception as e:
                    print(e)
                    print(f"[ComfyUI-Manager] Restoring '{repository_name}' is failed.")

        if exit_code != 0:
            print(f"[ComfyUI-Manager] Restore snapshot failed.")
        else:
            print(f"[ComfyUI-Manager] Restore snapshot done.")

    except Exception as e:
        print(e)
        print(f"[ComfyUI-Manager] Restore snapshot failed.")

    os.remove(restore_snapshot_path)


def execute_lazy_install_script(repo_path, executable):
    global processed_install

    install_script_path = os.path.join(repo_path, "install.py")
    requirements_path = os.path.join(repo_path, "requirements.txt")

    if os.path.exists(requirements_path):
        print(f"Install: pip packages for '{repo_path}'")
        with open(requirements_path, "r") as requirements_file:
            for line in requirements_file:
                package_name = line.strip()
                if package_name and not is_installed(package_name):
                    install_cmd = [executable, "-m", "pip", "install", package_name]
                    process_wrap(install_cmd, repo_path)

    if os.path.exists(install_script_path) and f'{repo_path}/install.py' not in processed_install:
        processed_install.add(f'{repo_path}/install.py')
        print(f"Install: install script for '{repo_path}'")
        install_cmd = [executable, "install.py"]
        process_wrap(install_cmd, repo_path)


# Check if script_list_path exists
if os.path.exists(script_list_path):
    print("\n#######################################################################")
    print("[ComfyUI-Manager] Starting dependency installation/(de)activation for the extension\n")

    executed = set()
    # Read each line from the file and convert it to a list using eval
    with open(script_list_path, 'r', encoding="UTF-8") as file:
        for line in file:
            if line in executed:
                continue

            executed.add(line)

            try:
                script = eval(line)

                if script[1].startswith('#'):
                    if script[1] == "#LAZY-INSTALL-SCRIPT":
                        execute_lazy_install_script(script[0], script[2])

                elif os.path.exists(script[0]):
                    if 'pip' in script[1:] and 'install' in script[1:] and is_installed(script[-1]):
                        continue

                    print(f"\n## ComfyUI-Manager: EXECUTE => {script[1:]}")
                    print(f"\n## Execute install/(de)activation script for '{script[0]}'")

                    exit_code = process_wrap(script[1:], script[0])

                    if exit_code != 0:
                        print(f"install/(de)activation script failed: {script[0]}")
                else:
                    print(f"\n## ComfyUI-Manager: CANCELED => {script[1:]}")

            except Exception as e:
                print(f"[ERROR] Failed to execute install/(de)activation script: {line} / {e}")

    # Remove the script_list_path file
    if os.path.exists(script_list_path):
        os.remove(script_list_path)
        
    print("\n[ComfyUI-Manager] Startup script completed.")
    print("#######################################################################\n")

del processed_install
del pip_list