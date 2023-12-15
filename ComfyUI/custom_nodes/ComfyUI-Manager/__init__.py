import configparser
import mimetypes
import shutil
import folder_paths
import os
import sys
import threading
import datetime
import re
import locale
import subprocess  # don't remove this
from tqdm.auto import tqdm
import concurrent
import ssl
from urllib.parse import urlparse
import http.client
import re
import signal
import nodes
import torch


version = [1, 13, 7]
version_str = f"V{version[0]}.{version[1]}" + (f'.{version[2]}' if len(version) > 2 else '')
print(f"### Loading: ComfyUI-Manager ({version_str})")


required_comfyui_revision = 1793
comfy_ui_hash = "-"


cache_lock = threading.Lock()

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


def run_script(cmd, cwd='.'):
    if len(cmd) > 0 and cmd[0].startswith("#"):
        print(f"[ComfyUI-Manager] Unexpected behavior: `{cmd}`")
        return 0

    process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    stdout_thread = threading.Thread(target=handle_stream, args=(process.stdout, ""))
    stderr_thread = threading.Thread(target=handle_stream, args=(process.stderr, "[!]"))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    return process.wait()


try:
    import git
except:
    my_path = os.path.dirname(__file__)
    requirements_path = os.path.join(my_path, "requirements.txt")

    print(f"## ComfyUI-Manager: installing dependencies")

    run_script([sys.executable, '-s', '-m', 'pip', 'install', '-r', requirements_path])

    try:
        import git
    except:
        print(f"## [ERROR] ComfyUI-Manager: Attempting to reinstall dependencies using an alternative method.")
        run_script([sys.executable, '-s', '-m', 'pip', 'install', '--user', '-r', requirements_path])

        try:
            import git
        except:
            print(f"## [ERROR] ComfyUI-Manager: Failed to install the GitPython package in the correct Python environment. Please install it manually in the appropriate environment. (You can seek help at https://app.element.io/#/room/%23comfyui_space%3Amatrix.org)")

    print(f"## ComfyUI-Manager: installing dependencies done.")


from git.remote import RemoteProgress

sys.path.append('../..')

from torchvision.datasets.utils import download_url

comfy_ui_required_revision = 1240
comfy_ui_revision = "Unknown"
comfy_ui_commit_date = ""

comfy_path = os.path.dirname(folder_paths.__file__)
custom_nodes_path = os.path.join(comfy_path, 'custom_nodes')
js_path = os.path.join(comfy_path, "web", "extensions")

comfyui_manager_path = os.path.dirname(__file__)
cache_dir = os.path.join(comfyui_manager_path, '.cache')
local_db_model = os.path.join(comfyui_manager_path, "model-list.json")
local_db_alter = os.path.join(comfyui_manager_path, "alter-list.json")
local_db_custom_node_list = os.path.join(comfyui_manager_path, "custom-node-list.json")
local_db_extension_node_mappings = os.path.join(comfyui_manager_path, "extension-node-map.json")
git_script_path = os.path.join(os.path.dirname(__file__), "git_helper.py")

startup_script_path = os.path.join(comfyui_manager_path, "startup-scripts")
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
cached_config = None


default_channels = 'default::https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main,recent::https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/node_db/new,'
with open(os.path.join(comfyui_manager_path, 'channels.list'), 'r') as file:
    channels = file.read()
    default_channels = channels.replace('\n', ',')


from comfy.cli_args import args
import latent_preview


def write_config():
    config = configparser.ConfigParser()
    config['default'] = {
        'preview_method': get_current_preview_method(),
        'badge_mode': get_config()['badge_mode'],
        'git_exe':  get_config()['git_exe'],
        'channel_url': get_config()['channel_url'],
        'channel_url_list': get_config()['channel_url_list'],
        'share_option': get_config()['share_option'],
        'bypass_ssl': get_config()['bypass_ssl']
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def read_config():
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        default_conf = config['default']

        channel_url_list_is_valid = True
        if 'channel_url_list' in default_conf and default_conf['channel_url_list'] != '':
            for item in default_conf['channel_url_list'].split(","):
                if len(item.split("::")) != 2:
                    channel_url_list_is_valid = False
                    break

        if channel_url_list_is_valid:
            ch_url_list = default_conf['channel_url_list']
        else:
            print(f"[WARN] ComfyUI-Manager: channel_url_list is invalid format")
            ch_url_list = ''

        return {
                    'preview_method': default_conf['preview_method'] if 'preview_method' in default_conf else get_current_preview_method(),
                    'badge_mode': default_conf['badge_mode'] if 'badge_mode' in default_conf else 'none',
                    'git_exe': default_conf['git_exe'] if 'git_exe' in default_conf else '',
                    'channel_url': default_conf['channel_url'] if 'channel_url' in default_conf else 'https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main',
                    'channel_url_list': ch_url_list,
                    'share_option': default_conf['share_option'] if 'share_option' in default_conf else 'all',
                    'bypass_ssl': default_conf['bypass_ssl'] if 'bypass_ssl' in default_conf else False,
               }

    except Exception:
        return {
            'preview_method': get_current_preview_method(),
            'badge_mode': 'none',
            'git_exe': '',
            'channel_url': 'https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main',
            'channel_url_list': '',
            'share_option': 'all',
            'bypass_ssl': False
        }


def get_config():
    global cached_config

    if cached_config is None:
        cached_config = read_config()

    return cached_config


def get_current_preview_method():
    if args.preview_method == latent_preview.LatentPreviewMethod.Auto:
        return "auto"
    elif args.preview_method == latent_preview.LatentPreviewMethod.Latent2RGB:
        return "latent2rgb"
    elif args.preview_method == latent_preview.LatentPreviewMethod.TAESD:
        return "taesd"
    else:
        return "none"


def set_preview_method(method):
    if method == 'auto':
        args.preview_method = latent_preview.LatentPreviewMethod.Auto
    elif method == 'latent2rgb':
        args.preview_method = latent_preview.LatentPreviewMethod.Latent2RGB
    elif method == 'taesd':
        args.preview_method = latent_preview.LatentPreviewMethod.TAESD
    else:
        args.preview_method = latent_preview.LatentPreviewMethod.NoPreviews

    get_config()['preview_method'] = args.preview_method


def set_badge_mode(mode):
    get_config()['badge_mode'] = mode


set_preview_method(get_config()['preview_method'])


def try_install_script(url, repo_path, install_cmd):
    int_comfyui_revision = 0

    if type(comfy_ui_revision) == int:
        int_comfyui_revision = comfy_ui_revision
    elif comfy_ui_revision.isdigit():
        int_comfyui_revision = int(comfy_ui_revision)

    if platform.system() == "Windows" and int_comfyui_revision >= comfy_ui_required_revision:
        if not os.path.exists(startup_script_path):
            os.makedirs(startup_script_path)

        script_path = os.path.join(startup_script_path, "install-scripts.txt")
        with open(script_path, "a") as file:
            obj = [repo_path] + install_cmd
            file.write(f"{obj}\n")

        return True
    else:
        print(f"\n## ComfyUI-Manager: EXECUTE => {install_cmd}")
        code = run_script(install_cmd, cwd=repo_path)

        if platform.system() == "Windows":
            try:
                if int(comfy_ui_revision) < comfy_ui_required_revision:
                    print("\n\n###################################################################")
                    print(f"[WARN] ComfyUI-Manager: Your ComfyUI version ({comfy_ui_revision}) is too old. Please update to the latest version.")
                    print(f"[WARN] The extension installation feature may not work properly in the current installed ComfyUI version on Windows environment.")
                    print("###################################################################\n\n")
            except:
                pass

        if code != 0:
            if url is None:
                url = os.path.dirname(repo_path)
            print(f"install script failed: {url}")
            return False

def print_comfyui_version():
    global comfy_ui_revision
    global comfy_ui_commit_date
    global comfy_ui_hash

    try:
        repo = git.Repo(os.path.dirname(folder_paths.__file__))

        comfy_ui_revision = len(list(repo.iter_commits('HEAD')))
        current_branch = repo.active_branch.name
        comfy_ui_hash = repo.head.commit.hexsha

        try:
            if int(comfy_ui_revision) < comfy_ui_required_revision:
                print(f"\n\n## [WARN] ComfyUI-Manager: Your ComfyUI version ({comfy_ui_revision}) is too old. Please update to the latest version. ##\n\n")
        except:
            pass

        comfy_ui_commit_date = repo.head.commit.committed_datetime.date()
        if current_branch == "master":
            print(f"### ComfyUI Revision: {comfy_ui_revision} [{comfy_ui_hash[:8]}] | Released on '{comfy_ui_commit_date}'")
        else:
            print(f"### ComfyUI Revision: {comfy_ui_revision} on '{current_branch}' [{comfy_ui_hash[:8]}] | Released on '{comfy_ui_commit_date}'")
    except:
        print("### ComfyUI Revision: UNKNOWN (The currently installed ComfyUI is not a Git repository)")


print_comfyui_version()


# use subprocess to avoid file system lock by git (Windows)
def __win_check_git_update(path, do_fetch=False, do_update=False):
    if do_fetch:
        command = [sys.executable, git_script_path, "--fetch", path]
    elif do_update:
        command = [sys.executable, git_script_path, "--pull", path]
    else:
        command = [sys.executable, git_script_path, "--check", path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()

    if 'detected dubious' in output:
        try:
            # fix and try again
            print(f"[ComfyUI-Manager] Try fixing 'dubious repository' error on '{path}' repo")
            process = subprocess.Popen(['git', 'config', '--global', '--add', 'safe.directory', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            output = output.decode('utf-8').strip()
        except Exception as e:
            print(f'[ComfyUI-Manager] failed to fixing')

        if 'detected dubious' in output:
            print(f'\n[ComfyUI-Manager] Failed to fixing repository setup. Please execute this command on cmd: \n'
                  f'-----------------------------------------------------------------------------------------\n'
                  f'git config --global --add safe.directory "{path}"\n'
                  f'-----------------------------------------------------------------------------------------\n')

    if do_update:
        if "CUSTOM NODE PULL: True" in output:
            process.wait()
            print(f"\rUpdated: {path}")
            return True
        elif "CUSTOM NODE PULL: None" in output:
            process.wait()
            return True
        else:
            print(f"\rUpdate error: {path}")
            process.wait()
            return False
    else:
        if "CUSTOM NODE CHECK: True" in output:
            process.wait()
            return True
        elif "CUSTOM NODE CHECK: False" in output:
            process.wait()
            return False
        else:
            print(f"\rFetch error: {path}")
            process.wait()
            return False


def __win_check_git_pull(path):
    command = [sys.executable, git_script_path, "--pull", path]
    process = subprocess.Popen(command)
    process.wait()


def switch_to_default_branch(repo):
    show_result = repo.git.remote("show", "origin")
    matches = re.search(r"\s*HEAD branch:\s*(.*)", show_result)
    if matches:
        default_branch = matches.group(1)
        repo.git.checkout(default_branch)


def git_repo_has_updates(path, do_fetch=False, do_update=False):
    if do_fetch:
        print(f"\x1b[2K\rFetching: {path}", end='')
    elif do_update:
        print(f"\x1b[2K\rUpdating: {path}", end='')

    # Check if the path is a git repository
    if not os.path.exists(os.path.join(path, '.git')):
        raise ValueError('Not a git repository')

    if platform.system() == "Windows":
        res = __win_check_git_update(path, do_fetch, do_update)
        execute_install_script(None, path, lazy_mode=True)
        return res
    else:
        # Fetch the latest commits from the remote repository
        repo = git.Repo(path)

        remote_name = 'origin'
        remote = repo.remote(name=remote_name)

        # Get the current commit hash
        commit_hash = repo.head.commit.hexsha

        if do_fetch or do_update:
            remote.fetch()

        if do_update:
            if repo.head.is_detached:
                switch_to_default_branch(repo)

            try:
                remote.pull()
                repo.git.submodule('update', '--init', '--recursive')
                new_commit_hash = repo.head.commit.hexsha

                if commit_hash != new_commit_hash:
                    execute_install_script(None, path)
                    print(f"\x1b[2K\rUpdated: {path}")
                    return True
                else:
                    return False

            except Exception as e:
                print(f"\nUpdating failed: {path}\n{e}", file=sys.stderr)

        if repo.head.is_detached:
            return True

        # Get commit hash of the remote branch
        current_branch = repo.active_branch
        branch_name = current_branch.name

        remote_commit_hash = repo.refs[f'{remote_name}/{branch_name}'].object.hexsha

        # Compare the commit hashes to determine if the local repository is behind the remote repository
        if commit_hash != remote_commit_hash:
            # Get the commit dates
            commit_date = repo.head.commit.committed_datetime
            remote_commit_date = repo.refs[f'{remote_name}/{branch_name}'].object.committed_datetime

            # Compare the commit dates to determine if the local repository is behind the remote repository
            if commit_date < remote_commit_date:
                return True

    return False


def git_pull(path):
    # Check if the path is a git repository
    if not os.path.exists(os.path.join(path, '.git')):
        raise ValueError('Not a git repository')

    # Pull the latest changes from the remote repository
    if platform.system() == "Windows":
        return __win_check_git_pull(path)
    else:
        repo = git.Repo(path)

        print(f"path={path} / repo.is_dirty: {repo.is_dirty()}")

        if repo.is_dirty():
            repo.git.stash()

        if repo.head.is_detached:
            switch_to_default_branch(repo)

        origin = repo.remote(name='origin')
        origin.pull()
        repo.git.submodule('update', '--init', '--recursive')
        
        repo.close()

    return True


async def get_data(uri):
    print(f"FETCH DATA from: {uri}")
    if uri.startswith("http"):
        async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(uri) as resp:
                json_text = await resp.text()
    else:
        with cache_lock:
            with open(uri, "r", encoding="utf-8") as f:
                json_text = f.read()

    json_obj = json.loads(json_text)
    return json_obj


def setup_js():
    import nodes
    js_dest_path = os.path.join(js_path, "comfyui-manager")

    if hasattr(nodes, "EXTENSION_WEB_DIRS"):
        if os.path.exists(js_dest_path):
            shutil.rmtree(js_dest_path)
    else:
        print(f"[WARN] ComfyUI-Manager: Your ComfyUI version is outdated. Please update to the latest version.")
        # setup js
        if not os.path.exists(js_dest_path):
            os.makedirs(js_dest_path)
        js_src_path = os.path.join(comfyui_manager_path, "js", "comfyui-manager.js")

        print(f"### ComfyUI-Manager: Copy .js from '{js_src_path}' to '{js_dest_path}'")
        shutil.copy(js_src_path, js_dest_path)


setup_js()


def setup_environment():
    git_exe = get_config()['git_exe']

    if git_exe != '':
        git.Git().update_environment(GIT_PYTHON_GIT_EXECUTABLE=git_exe)


setup_environment()


# Expand Server api

import server
from aiohttp import web
import aiohttp
import json
import zipfile
import urllib.request


def simple_hash(input_string):
    hash_value = 0
    for char in input_string:
        hash_value = (hash_value * 31 + ord(char)) % (2**32)

    return hash_value


def is_file_created_within_one_day(file_path):
    if not os.path.exists(file_path):
        return False

    file_creation_time = os.path.getctime(file_path)
    current_time = datetime.datetime.now().timestamp()
    time_difference = current_time - file_creation_time

    return time_difference <= 86400


async def get_data_by_mode(mode, filename):
    try:
        if mode == "local":
            uri = os.path.join(comfyui_manager_path, filename)
            json_obj = await get_data(uri)
        else:
            uri = get_config()['channel_url'] + '/' + filename
            cache_uri = str(simple_hash(uri))+'_'+filename
            cache_uri = os.path.join(cache_dir, cache_uri)

            if mode == "cache":
                if is_file_created_within_one_day(cache_uri):
                    json_obj = await get_data(cache_uri)
                else:
                    json_obj = await get_data(uri)
                    with cache_lock:
                        with open(cache_uri, "w", encoding='utf-8') as file:
                            json.dump(json_obj, file, indent=4, sort_keys=True)
            else:
                uri = get_config()['channel_url'] + '/' + filename
                json_obj = await get_data(uri)
                with cache_lock:
                    with open(cache_uri, "w", encoding='utf-8') as file:
                        json.dump(json_obj, file, indent=4, sort_keys=True)
    except Exception as e:
        print(f"[ComfyUI-Manager] Due to a network error, switching to local mode.\n=> {filename}\n=> {e}")
        uri = os.path.join(comfyui_manager_path, filename)
        json_obj = await get_data(uri)

    return json_obj


def get_model_dir(data):
    if data['save_path'] != 'default':
        if '..' in data['save_path'] or data['save_path'].startswith('/'):
            print(f"[WARN] '{data['save_path']}' is not allowed path. So it will be saved into 'models/etc'.")
            base_model = "etc"
        else:
            if data['save_path'].startswith("custom_nodes"):
                base_model = os.path.join(comfy_path, data['save_path'])
            else:
                base_model = os.path.join(folder_paths.models_dir, data['save_path'])
    else:
        model_type = data['type']
        if model_type == "checkpoints":
            base_model = folder_paths.folder_names_and_paths["checkpoints"][0][0]
        elif model_type == "unclip":
            base_model = folder_paths.folder_names_and_paths["checkpoints"][0][0]
        elif model_type == "VAE":
            base_model = folder_paths.folder_names_and_paths["vae"][0][0]
        elif model_type == "lora":
            base_model = folder_paths.folder_names_and_paths["loras"][0][0]
        elif model_type == "T2I-Adapter":
            base_model = folder_paths.folder_names_and_paths["controlnet"][0][0]
        elif model_type == "T2I-Style":
            base_model = folder_paths.folder_names_and_paths["controlnet"][0][0]
        elif model_type == "controlnet":
            base_model = folder_paths.folder_names_and_paths["controlnet"][0][0]
        elif model_type == "clip_vision":
            base_model = folder_paths.folder_names_and_paths["clip_vision"][0][0]
        elif model_type == "gligen":
            base_model = folder_paths.folder_names_and_paths["gligen"][0][0]
        elif model_type == "upscale":
            base_model = folder_paths.folder_names_and_paths["upscale_models"][0][0]
        elif model_type == "embeddings":
            base_model = folder_paths.folder_names_and_paths["embeddings"][0][0]
        else:
            base_model = "etc"

    return base_model


def get_model_path(data):
    base_model = get_model_dir(data)
    return os.path.join(base_model, data['filename'])


def check_a_custom_node_installed(item, do_fetch=False, do_update_check=True, do_update=False):
    item['installed'] = 'None'

    if item['install_type'] == 'git-clone' and len(item['files']) == 1:
        url = item['files'][0]

        if url.endswith("/"):
            url = url[:-1]

        dir_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
        dir_path = os.path.join(custom_nodes_path, dir_name)
        if os.path.exists(dir_path):
            try:
                if do_update_check and git_repo_has_updates(dir_path, do_fetch, do_update):
                    item['installed'] = 'Update'
                elif sys.__comfyui_manager_is_import_failed_extension(dir_name):
                    item['installed'] = 'Fail'
                else:
                    item['installed'] = 'True'
            except:
                if sys.__comfyui_manager_is_import_failed_extension(dir_name):
                    item['installed'] = 'Fail'
                else:
                    item['installed'] = 'True'

        elif os.path.exists(dir_path + ".disabled"):
            item['installed'] = 'Disabled'

        else:
            item['installed'] = 'False'

    elif item['install_type'] == 'copy' and len(item['files']) == 1:
        dir_name = os.path.basename(item['files'][0])

        if item['files'][0].endswith('.py'):
            base_path = custom_nodes_path
        elif 'js_path' in item:
            base_path = os.path.join(js_path, item['js_path'])
        else:
            base_path = js_path

        file_path = os.path.join(base_path, dir_name)
        if os.path.exists(file_path):
            if sys.__comfyui_manager_is_import_failed_extension(dir_name):
                item['installed'] = 'Fail'
            else:
                item['installed'] = 'True'
        elif os.path.exists(file_path + ".disabled"):
            item['installed'] = 'Disabled'
        else:
            item['installed'] = 'False'


def check_custom_nodes_installed(json_obj, do_fetch=False, do_update_check=True, do_update=False):
    if do_fetch:
        print("Start fetching...", end="")
    elif do_update:
        print("Start updating...", end="")
    elif do_update_check:
        print("Start update check...", end="")

    def process_custom_node(item):
        check_a_custom_node_installed(item, do_fetch, do_update_check, do_update)

    with concurrent.futures.ThreadPoolExecutor(4) as executor:
        for item in json_obj['custom_nodes']:
            executor.submit(process_custom_node, item)

    if do_fetch:
        print(f"\x1b[2K\rFetching done.")
    elif do_update:
        update_exists = any(item['installed'] == 'Update' for item in json_obj['custom_nodes'])
        if update_exists:
            print(f"\x1b[2K\rUpdate done.")
        else:
            print(f"\x1b[2K\rAll extensions are already up-to-date.")
    elif do_update_check:
        print(f"\x1b[2K\rUpdate check done.")


@server.PromptServer.instance.routes.get("/customnode/getmappings")
async def fetch_customnode_mappings(request):
    json_obj = await get_data_by_mode(request.rel_url.query["mode"], 'extension-node-map.json')
    
    all_nodes = set()
    patterns = []
    for k, x in json_obj.items():
        all_nodes.update(set(x[0]))

        if 'nodename_pattern' in x[1]:
            patterns.append((x[1]['nodename_pattern'], x[0]))

    missing_nodes = set(nodes.NODE_CLASS_MAPPINGS.keys()) - all_nodes

    for x in missing_nodes:
        for pat, item in patterns:
            if re.match(pat, x):
                item.append(x)

    return web.json_response(json_obj, content_type='application/json')


@server.PromptServer.instance.routes.get("/customnode/fetch_updates")
async def fetch_updates(request):
    try:
        json_obj = await get_data_by_mode(request.rel_url.query["mode"], 'custom-node-list.json')

        check_custom_nodes_installed(json_obj, True)

        update_exists = any('custom_nodes' in json_obj and 'installed' in node and node['installed'] == 'Update' for node in
                            json_obj['custom_nodes'])

        if update_exists:
            return web.Response(status=201)

        return web.Response(status=200)
    except:
        return web.Response(status=400)


@server.PromptServer.instance.routes.get("/customnode/update_all")
async def update_all(request):
    try:
        save_snapshot_with_postfix('autosave')

        json_obj = await get_data_by_mode(request.rel_url.query["mode"], 'custom-node-list.json')

        check_custom_nodes_installed(json_obj, do_update=True)

        update_exists = any(item['installed'] == 'Update' for item in json_obj['custom_nodes'])

        if update_exists:
            return web.Response(status=201)

        return web.Response(status=200)
    except:
        return web.Response(status=400)


def convert_markdown_to_html(input_text):
    pattern_a = re.compile(r'\[a/([^]]+)\]\(([^)]+)\)')
    pattern_w = re.compile(r'\[w/([^]]+)\]')
    pattern_i = re.compile(r'\[i/([^]]+)\]')
    pattern_bold = re.compile(r'\*\*([^*]+)\*\*')
    pattern_white = re.compile(r'%%([^*]+)%%')

    def replace_a(match):
        return f"<a href='{match.group(2)}' target='blank'>{match.group(1)}</a>"

    def replace_w(match):
        return f"<p class='cm-warn-note'>{match.group(1)}</p>"

    def replace_i(match):
        return f"<p class='cm-info-note'>{match.group(1)}</p>"

    def replace_bold(match):
        return f"<B>{match.group(1)}</B>"

    def replace_white(match):
        return f"<font color='white'>{match.group(1)}</font>"

    input_text = input_text.replace('\\[', '&#91;').replace('\\]', '&#93;').replace('<', '&lt;').replace('>', '&gt;')

    result_text = re.sub(pattern_a, replace_a, input_text)
    result_text = re.sub(pattern_w, replace_w, result_text)
    result_text = re.sub(pattern_i, replace_i, result_text)
    result_text = re.sub(pattern_bold, replace_bold, result_text)
    result_text = re.sub(pattern_white, replace_white, result_text)

    return result_text.replace("\n", "<BR>")


def populate_markdown(x):
    if 'description' in x:
        x['description'] = convert_markdown_to_html(x['description'])

    if 'name' in x:
        x['name'] = x['name'].replace('<', '&lt;').replace('>', '&gt;')

    if 'title' in x:
        x['title'] = x['title'].replace('<', '&lt;').replace('>', '&gt;')


@server.PromptServer.instance.routes.get("/customnode/getlist")
async def fetch_customnode_list(request):
    if "skip_update" in request.rel_url.query and request.rel_url.query["skip_update"] == "true":
        skip_update = True
    else:
        skip_update = False

    if request.rel_url.query["mode"] == "local":
        channel = 'local'
    else:
        channel = get_config()['channel_url']

    json_obj = await get_data_by_mode(request.rel_url.query["mode"], 'custom-node-list.json')

    def is_ignored_notice(code):
        global version

        if code is not None and code.startswith('#NOTICE_'):
            try:
                notice_version = [int(x) for x in code[8:].split('.')]
                return notice_version[0] < version[0] or (notice_version[0] == version[0] and notice_version[1] <= version[1])
            except Exception:
                return False
        else:
            False


    json_obj['custom_nodes'] = [record for record in json_obj['custom_nodes'] if not is_ignored_notice(record.get('author'))]

    check_custom_nodes_installed(json_obj, False, not skip_update)

    for x in json_obj['custom_nodes']:
        populate_markdown(x)

    if channel != 'local':
        channels = default_channels+","+get_config()['channel_url_list']
        channels = channels.split(',')

        found = 'custom'
        for item in channels:
            item_info = item.split('::')
            if len(item_info) == 2 and item_info[1] == channel:
                found = item_info[0]

        channel = found

    json_obj['channel'] = channel

    return web.json_response(json_obj, content_type='application/json')


@server.PromptServer.instance.routes.get("/alternatives/getlist")
async def fetch_alternatives_list(request):
    if "skip_update" in request.rel_url.query and request.rel_url.query["skip_update"] == "true":
        skip_update = True
    else:
        skip_update = False

    alter_json = await get_data_by_mode(request.rel_url.query["mode"], 'alter-list.json')
    custom_node_json = await get_data_by_mode(request.rel_url.query["mode"], 'custom-node-list.json')

    fileurl_to_custom_node = {}

    for item in custom_node_json['custom_nodes']:
        for fileurl in item['files']:
            fileurl_to_custom_node[fileurl] = item

    for item in alter_json['items']:
        fileurl = item['id']
        if fileurl in fileurl_to_custom_node:
            custom_node = fileurl_to_custom_node[fileurl]
            check_a_custom_node_installed(custom_node, not skip_update)

            populate_markdown(item)
            populate_markdown(custom_node)
            item['custom_node'] = custom_node

    return web.json_response(alter_json, content_type='application/json')


def check_model_installed(json_obj):
    def process_model(item):
        model_path = get_model_path(item)
        item['installed'] = 'None'

        if model_path is not None:
            if os.path.exists(model_path):
                item['installed'] = 'True'
            else:
                item['installed'] = 'False'

    with concurrent.futures.ThreadPoolExecutor(8) as executor:
        for item in json_obj['models']:
            executor.submit(process_model, item)


@server.PromptServer.instance.routes.get("/externalmodel/getlist")
async def fetch_externalmodel_list(request):
    json_obj = await get_data_by_mode(request.rel_url.query["mode"], 'model-list.json')

    check_model_installed(json_obj)

    for x in json_obj['models']:
        populate_markdown(x)

    return web.json_response(json_obj, content_type='application/json')


@server.PromptServer.instance.routes.get("/snapshot/getlist")
async def get_snapshot_list(request):
    snapshots_directory = os.path.join(os.path.dirname(__file__), 'snapshots')
    items = [f[:-5] for f in os.listdir(snapshots_directory) if f.endswith('.json')]
    items.sort(reverse=True)
    return web.json_response({'items': items}, content_type='application/json')


@server.PromptServer.instance.routes.get("/snapshot/remove")
async def remove_snapshot(request):
    try:
        target = request.rel_url.query["target"]

        path = os.path.join(os.path.dirname(__file__), 'snapshots', f"{target}.json")
        if os.path.exists(path):
            os.remove(path)

        return web.Response(status=200)
    except:
        return web.Response(status=400)


@server.PromptServer.instance.routes.get("/snapshot/restore")
async def remove_snapshot(request):
    try:
        target = request.rel_url.query["target"]

        path = os.path.join(os.path.dirname(__file__), 'snapshots', f"{target}.json")
        if os.path.exists(path):
            if not os.path.exists(startup_script_path):
                os.makedirs(startup_script_path)

            target_path = os.path.join(startup_script_path, "restore-snapshot.json")
            shutil.copy(path, target_path)

            print(f"Snapshot restore scheduled: `{target}`")
            return web.Response(status=200)

        print(f"Snapshot file not found: `{path}`")
        return web.Response(status=400)
    except:
        return web.Response(status=400)


def get_current_snapshot():
    # Get ComfyUI hash
    repo_path = os.path.dirname(folder_paths.__file__)

    if not os.path.exists(os.path.join(repo_path, '.git')):
        print(f"ComfyUI update fail: The installed ComfyUI does not have a Git repository.")
        return web.Response(status=400)

    repo = git.Repo(repo_path)
    comfyui_commit_hash = repo.head.commit.hexsha

    git_custom_nodes = {}
    file_custom_nodes = []

    # Get custom nodes hash
    for path in os.listdir(custom_nodes_path):
        fullpath = os.path.join(custom_nodes_path, path)

        if os.path.isdir(fullpath):
            is_disabled = path.endswith(".disabled")

            try:
                git_dir = os.path.join(fullpath, '.git')

                if not os.path.exists(git_dir):
                    continue

                repo = git.Repo(fullpath)
                commit_hash = repo.head.commit.hexsha
                url = repo.remotes.origin.url
                git_custom_nodes[url] = {
                    'hash': commit_hash,
                    'disabled': is_disabled
                }

            except:
                print(f"Failed to extract snapshots for the custom node '{path}'.")

        elif path.endswith('.py'):
            is_disabled = path.endswith(".py.disabled")
            filename = os.path.basename(path)
            item = {
                'filename': filename,
                'disabled': is_disabled
            }

            file_custom_nodes.append(item)

    return {
        'comfyui': comfyui_commit_hash,
        'git_custom_nodes': git_custom_nodes,
        'file_custom_nodes': file_custom_nodes,
    }


def save_snapshot_with_postfix(postfix):
        now = datetime.datetime.now()

        date_time_format = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{date_time_format}_{postfix}"

        path = os.path.join(os.path.dirname(__file__), 'snapshots', f"{file_name}.json")
        with open(path, "w") as json_file:
            json.dump(get_current_snapshot(), json_file, indent=4)


@server.PromptServer.instance.routes.get("/snapshot/get_current")
async def get_current_snapshot_api(request):
    try:
        return web.json_response(get_current_snapshot(), content_type='application/json')
    except:
        return web.Response(status=400)


@server.PromptServer.instance.routes.get("/snapshot/save")
async def save_snapshot(request):
    try:
        save_snapshot_with_postfix('snapshot')
        return web.Response(status=200)
    except:
        return web.Response(status=400)


def unzip_install(files):
    temp_filename = 'manager-temp.zip'
    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            data = response.read()

            with open(temp_filename, 'wb') as f:
                f.write(data)

            with zipfile.ZipFile(temp_filename, 'r') as zip_ref:
                zip_ref.extractall(custom_nodes_path)

            os.remove(temp_filename)
        except Exception as e:
            print(f"Install(unzip) error: {url} / {e}", file=sys.stderr)
            return False

    print("Installation was successful.")
    return True


def download_url_with_agent(url, save_path):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read()

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        with open(save_path, 'wb') as f:
            f.write(data)

    except Exception as e:
        print(f"Download error: {url} / {e}", file=sys.stderr)
        return False

    print("Installation was successful.")
    return True


def copy_install(files, js_path_name=None):
    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        try:
            if url.endswith(".py"):
                download_url(url, custom_nodes_path)
            else:
                path = os.path.join(js_path, js_path_name) if js_path_name is not None else js_path
                if not os.path.exists(path):
                    os.makedirs(path)
                download_url(url, path)

        except Exception as e:
            print(f"Install(copy) error: {url} / {e}", file=sys.stderr)
            return False

    print("Installation was successful.")
    return True


def copy_uninstall(files, js_path_name='.'):
    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        dir_name = os.path.basename(url)
        base_path = custom_nodes_path if url.endswith('.py') else os.path.join(js_path, js_path_name)
        file_path = os.path.join(base_path, dir_name)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            elif os.path.exists(file_path + ".disabled"):
                os.remove(file_path + ".disabled")
        except Exception as e:
            print(f"Uninstall(copy) error: {url} / {e}", file=sys.stderr)
            return False

    print("Uninstallation was successful.")
    return True


def copy_set_active(files, is_disable, js_path_name='.'):
    if is_disable:
        action_name = "Disable"
    else:
        action_name = "Enable"

    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        dir_name = os.path.basename(url)
        base_path = custom_nodes_path if url.endswith('.py') else os.path.join(js_path, js_path_name)
        file_path = os.path.join(base_path, dir_name)

        try:
            if is_disable:
                current_name = file_path
                new_name = file_path + ".disabled"
            else:
                current_name = file_path + ".disabled"
                new_name = file_path

            os.rename(current_name, new_name)

        except Exception as e:
            print(f"{action_name}(copy) error: {url} / {e}", file=sys.stderr)

            return False

    print(f"{action_name} was successful.")
    return True


def execute_install_script(url, repo_path, lazy_mode=False):
    install_script_path = os.path.join(repo_path, "install.py")
    requirements_path = os.path.join(repo_path, "requirements.txt")

    if lazy_mode:
        install_cmd = ["#LAZY-INSTALL-SCRIPT",  sys.executable]
        try_install_script(url, repo_path, install_cmd)
    else:
        if os.path.exists(requirements_path):
            print("Install: pip packages")
            with open(requirements_path, "r") as requirements_file:
                for line in requirements_file:
                    package_name = line.strip()
                    if package_name:
                        install_cmd = [sys.executable, "-m", "pip", "install", package_name]
                        if package_name.strip() != "":
                            try_install_script(url, repo_path, install_cmd)

        if os.path.exists(install_script_path):
            print(f"Install: install script")
            install_cmd = [sys.executable, "install.py"]
            try_install_script(url, repo_path, install_cmd)

    return True


class GitProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.pos = 0
        self.pbar.refresh()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def gitclone_install(files):
    print(f"install: {files}")
    for url in files:
        if not is_valid_url(url):
            print(f"Invalid git url: '{url}'")
            return False

        if url.endswith("/"):
            url = url[:-1]
        try:
            print(f"Download: git clone '{url}'")
            repo_name = os.path.splitext(os.path.basename(url))[0]
            repo_path = os.path.join(custom_nodes_path, repo_name)

            # Clone the repository from the remote URL
            if platform.system() == 'Windows':
                res = run_script([sys.executable, git_script_path, "--clone", custom_nodes_path, url])
                if res != 0:
                    return False
            else:
                repo = git.Repo.clone_from(url, repo_path, recursive=True, progress=GitProgress())
                repo.git.clear_cache()
                repo.close()

            if not execute_install_script(url, repo_path):
                return False

        except Exception as e:
            print(f"Install(git-clone) error: {url} / {e}", file=sys.stderr)
            return False

    print("Installation was successful.")
    return True


import platform
import subprocess
import time


def rmtree(path):
    retry_count = 3

    while True:
        try:
            retry_count -= 1

            if platform.system() == "Windows":
                run_script(['attrib', '-R', path + '\\*', '/S'])
            shutil.rmtree(path)

            return True

        except Exception as ex:
            print(f"ex: {ex}")
            time.sleep(3)

            if retry_count < 0:
                raise ex

            print(f"Uninstall retry({retry_count})")


def gitclone_uninstall(files):
    import shutil
    import os

    print(f"uninstall: {files}")
    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        try:
            dir_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
            dir_path = os.path.join(custom_nodes_path, dir_name)

            # safety check
            if dir_path == '/' or dir_path[1:] == ":/" or dir_path == '':
                print(f"Uninstall(git-clone) error: invalid path '{dir_path}' for '{url}'")
                return False

            install_script_path = os.path.join(dir_path, "uninstall.py")
            disable_script_path = os.path.join(dir_path, "disable.py")
            if os.path.exists(install_script_path):
                uninstall_cmd = [sys.executable, "uninstall.py"]
                code = run_script(uninstall_cmd, cwd=dir_path)

                if code != 0:
                    print(f"An error occurred during the execution of the uninstall.py script. Only the '{dir_path}' will be deleted.")
            elif os.path.exists(disable_script_path):
                disable_script = [sys.executable, "disable.py"]
                code = run_script(disable_script, cwd=dir_path)
                if code != 0:
                    print(f"An error occurred during the execution of the disable.py script. Only the '{dir_path}' will be deleted.")

            if os.path.exists(dir_path):
                rmtree(dir_path)
            elif os.path.exists(dir_path + ".disabled"):
                rmtree(dir_path + ".disabled")
        except Exception as e:
            print(f"Uninstall(git-clone) error: {url} / {e}", file=sys.stderr)
            return False

    print("Uninstallation was successful.")
    return True


def gitclone_set_active(files, is_disable):
    import os

    if is_disable:
        action_name = "Disable"
    else:
        action_name = "Enable"

    print(f"{action_name}: {files}")
    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        try:
            dir_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
            dir_path = os.path.join(custom_nodes_path, dir_name)

            # safey check
            if dir_path == '/' or dir_path[1:] == ":/" or dir_path == '':
                print(f"{action_name}(git-clone) error: invalid path '{dir_path}' for '{url}'")
                return False

            if is_disable:
                current_path = dir_path
                new_path = dir_path + ".disabled"
            else:
                current_path = dir_path + ".disabled"
                new_path = dir_path

            os.rename(current_path, new_path)

            if is_disable:
                if os.path.exists(os.path.join(new_path, "disable.py")):
                    disable_script = [sys.executable, "disable.py"]
                    try_install_script(url, new_path, disable_script)
            else:
                if os.path.exists(os.path.join(new_path, "enable.py")):
                    enable_script = [sys.executable, "enable.py"]
                    try_install_script(url, new_path, enable_script)

        except Exception as e:
            print(f"{action_name}(git-clone) error: {url} / {e}", file=sys.stderr)
            return False

    print(f"{action_name} was successful.")
    return True


def gitclone_update(files):
    import os

    print(f"Update: {files}")
    for url in files:
        if url.endswith("/"):
            url = url[:-1]
        try:
            repo_name = os.path.splitext(os.path.basename(url))[0].replace(".git", "")
            repo_path = os.path.join(custom_nodes_path, repo_name)
            git_pull(repo_path)

            if not execute_install_script(url, repo_path, lazy_mode=True):
                return False

        except Exception as e:
            print(f"Update(git-clone) error: {url} / {e}", file=sys.stderr)
            return False

    print("Update was successful.")
    return True


@server.PromptServer.instance.routes.post("/customnode/install")
async def install_custom_node(request):
    json_data = await request.json()

    install_type = json_data['install_type']

    print(f"Install custom node '{json_data['title']}'")

    res = False

    if len(json_data['files']) == 0:
        return web.Response(status=400)

    if install_type == "unzip":
        res = unzip_install(json_data['files'])

    if install_type == "copy":
        js_path_name = json_data['js_path'] if 'js_path' in json_data else '.'
        res = copy_install(json_data['files'], js_path_name)

    elif install_type == "git-clone":
        res = gitclone_install(json_data['files'])

    if 'pip' in json_data:
        for pname in json_data['pip']:
            install_cmd = [sys.executable, "-m", "pip", "install", pname]
            try_install_script(json_data['files'][0], ".", install_cmd)

    if res:
        print(f"After restarting ComfyUI, please refresh the browser.")
        return web.json_response({}, content_type='application/json')

    return web.Response(status=400)


@server.PromptServer.instance.routes.get("/customnode/install/git_url")
async def install_custom_node_git_url(request):
    res = False
    if "url" in request.rel_url.query:
        url = request.rel_url.query['url']
        res = gitclone_install([url])

    if res:
        print(f"After restarting ComfyUI, please refresh the browser.")
        return web.Response(status=200)

    return web.Response(status=400)


@server.PromptServer.instance.routes.post("/customnode/uninstall")
async def uninstall_custom_node(request):
    json_data = await request.json()

    install_type = json_data['install_type']

    print(f"Uninstall custom node '{json_data['title']}'")

    res = False

    if install_type == "copy":
        js_path_name = json_data['js_path'] if 'js_path' in json_data else '.'
        res = copy_uninstall(json_data['files'], js_path_name)

    elif install_type == "git-clone":
        res = gitclone_uninstall(json_data['files'])

    if res:
        print(f"After restarting ComfyUI, please refresh the browser.")
        return web.json_response({}, content_type='application/json')

    return web.Response(status=400)


@server.PromptServer.instance.routes.post("/customnode/update")
async def update_custom_node(request):
    json_data = await request.json()

    install_type = json_data['install_type']

    print(f"Update custom node '{json_data['title']}'")

    res = False

    if install_type == "git-clone":
        res = gitclone_update(json_data['files'])

    if res:
        print(f"After restarting ComfyUI, please refresh the browser.")
        return web.json_response({}, content_type='application/json')

    return web.Response(status=400)


@server.PromptServer.instance.routes.get("/comfyui_manager/update_comfyui")
async def update_comfyui(request):
    print(f"Update ComfyUI")

    try:
        repo_path = os.path.dirname(folder_paths.__file__)

        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"ComfyUI update fail: The installed ComfyUI does not have a Git repository.")
            return web.Response(status=400)

        # version check
        repo = git.Repo(repo_path)

        if repo.head.is_detached:
            switch_to_default_branch(repo)

        current_branch = repo.active_branch
        branch_name = current_branch.name

        remote_name = 'origin'
        remote = repo.remote(name=remote_name)

        try:
            remote.fetch()
        except Exception as e:
            if 'detected dubious' in e:
                print(f"[ComfyUI-Manager] Try fixing 'dubious repository' error on 'ComfyUI' repository")
                subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', comfy_path])
                try:
                    remote.fetch()
                except Exception:
                    print(f"\n[ComfyUI-Manager] Failed to fixing repository setup. Please execute this command on cmd: \n"
                          f"-----------------------------------------------------------------------------------------\n"
                          f'git config --global --add safe.directory "{comfy_path}"\n'
                          f"-----------------------------------------------------------------------------------------\n")

        commit_hash = repo.head.commit.hexsha
        remote_commit_hash = repo.refs[f'{remote_name}/{branch_name}'].object.hexsha

        if commit_hash != remote_commit_hash:
            git_pull(repo_path)
            execute_install_script("ComfyUI", repo_path)
            return web.Response(status=201)
        else:
            return web.Response(status=200)
    except Exception as e:
        print(f"ComfyUI update fail: {e}", file=sys.stderr)
        pass

    return web.Response(status=400)


@server.PromptServer.instance.routes.post("/customnode/toggle_active")
async def toggle_active(request):
    json_data = await request.json()

    install_type = json_data['install_type']
    is_disabled = json_data['installed'] == "Disabled"

    print(f"Update custom node '{json_data['title']}'")

    res = False

    if install_type == "git-clone":
        res = gitclone_set_active(json_data['files'], not is_disabled)
    elif install_type == "copy":
        res = copy_set_active(json_data['files'], not is_disabled, json_data.get('js_path', None))

    if res:
        return web.json_response({}, content_type='application/json')

    return web.Response(status=400)


@server.PromptServer.instance.routes.post("/model/install")
async def install_model(request):
    json_data = await request.json()

    model_path = get_model_path(json_data)

    res = False

    try:
        if model_path is not None:
            print(f"Install model '{json_data['name']}' into '{model_path}'")

            if json_data['url'].startswith('https://github.com') or json_data['url'].startswith('https://huggingface.co'):
                model_dir = get_model_dir(json_data)
                download_url(json_data['url'], model_dir)
                
                return web.json_response({}, content_type='application/json')
            else:
                res = download_url_with_agent(json_data['url'], model_path)
        else:
            print(f"Model installation error: invalid model type - {json_data['type']}")

        if res:
            return web.json_response({}, content_type='application/json')
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        pass

    return web.Response(status=400)


class ManagerTerminalHook:
    def write_stderr(self, msg):
        server.PromptServer.instance.send_sync("manager-terminal-feedback", {"data": msg})

    def write_stdout(self, msg):
        server.PromptServer.instance.send_sync("manager-terminal-feedback", {"data": msg})


manager_terminal_hook = ManagerTerminalHook()


@server.PromptServer.instance.routes.get("/manager/terminal")
async def terminal_mode(request):
    if "mode" in request.rel_url.query:
        if request.rel_url.query['mode'] == 'true':
            sys.__comfyui_manager_terminal_hook.add_hook('cm', manager_terminal_hook)
        else:
            sys.__comfyui_manager_terminal_hook.remove_hook('cm')

    return web.Response(status=200)


@server.PromptServer.instance.routes.get("/manager/preview_method")
async def preview_method(request):
    if "value" in request.rel_url.query:
        set_preview_method(request.rel_url.query['value'])
        write_config()
    else:
        return web.Response(text=get_current_preview_method(), status=200)

    return web.Response(status=200)


@server.PromptServer.instance.routes.get("/manager/badge_mode")
async def badge_mode(request):
    if "value" in request.rel_url.query:
        set_badge_mode(request.rel_url.query['value'])
        write_config()
    else:
        return web.Response(text=get_config()['badge_mode'], status=200)

    return web.Response(status=200)


@server.PromptServer.instance.routes.get("/manager/channel_url_list")
async def channel_url_list(request):
    channels = default_channels+","+get_config()['channel_url_list']
    channels = channels.split(',')

    if "value" in request.rel_url.query:
        for item in channels:
            name_url = item.split("::")
            if len(name_url) == 2 and name_url[0] == request.rel_url.query['value']:
                get_config()['channel_url'] = name_url[1]
                write_config()
                break
    else:
        selected = 'custom'
        selected_url = get_config()['channel_url']
        for item in channels:
            item_info = item.split('::')
            if len(item_info) == 2 and item_info[1] == selected_url:
                selected = item_info[0]

        res = {'selected': selected,
               'list': channels}
        return web.json_response(res, status=200)

    return web.Response(status=200)


@server.PromptServer.instance.routes.get("/manager/notice")
async def get_notice(request):
    url = "github.com"
    path = "/ltdrdata/ltdrdata.github.io/wiki/News"

    conn = http.client.HTTPSConnection(url)
    conn.request("GET", path)

    response = conn.getresponse()

    try:
        if response.status == 200:
            html_content = response.read().decode('utf-8')

            pattern = re.compile(r'<div class="markdown-body">([\s\S]*?)</div>')
            match = pattern.search(html_content)

            if match:
                markdown_content = match.group(1)
                markdown_content += f"<HR>ComfyUI: {comfy_ui_revision}[{comfy_ui_hash[:6]}]({comfy_ui_commit_date})"
                # markdown_content += f"<BR>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;()"
                markdown_content += f"<BR>Manager: {version_str}"

                try:
                    if required_comfyui_revision > int(comfy_ui_revision):
                        markdown_content = f'<P style="text-align: center; color:red; background-color:white; font-weight:bold">Your ComfyUI is too OUTDATED!!!</P>' + markdown_content
                except:
                    pass

                return web.Response(text=markdown_content, status=200)
            else:
                return web.Response(text="Unable to retrieve Notice", status=200)
        else:
            return web.Response(text="Unable to retrieve Notice", status=200)
    finally:
        conn.close()


@server.PromptServer.instance.routes.get("/manager/reboot")
def restart(self):
    try:
        sys.stdout.close_log()
    except Exception as e:
        pass

    return os.execv(sys.executable, [sys.executable] + sys.argv)


@server.PromptServer.instance.routes.get("/manager/share_option")
async def share_option(request):
    if "value" in request.rel_url.query:
        get_config()['share_option'] = request.rel_url.query['value']
        write_config()
    else:
        return web.Response(text=get_config()['share_option'], status=200)

    return web.Response(status=200)


def get_openart_auth():
    if not os.path.exists(os.path.join(comfyui_manager_path, ".openart_key")):
        return None
    try:
        with open(os.path.join(comfyui_manager_path, ".openart_key"), "r") as f:
            openart_key = f.read().strip()
        return openart_key if openart_key else None
    except:
        return None


def get_matrix_auth():
    if not os.path.exists(os.path.join(comfyui_manager_path, "matrix_auth")):
        return None
    try:
        with open(os.path.join(comfyui_manager_path, "matrix_auth"), "r") as f:
            matrix_auth = f.read()
            homeserver, username, password = matrix_auth.strip().split("\n")
            if not homeserver or not username or not password:
                return None
        return {
            "homeserver": homeserver,
            "username": username,
            "password": password,
        }
    except:
        return None


def get_comfyworkflows_auth():
    if not os.path.exists(os.path.join(comfyui_manager_path, "comfyworkflows_sharekey")):
        return None
    try:
        with open(os.path.join(comfyui_manager_path, "comfyworkflows_sharekey"), "r") as f:
            share_key = f.read()
            if not share_key.strip():
                return None
        return share_key
    except:
        return None


@server.PromptServer.instance.routes.get("/manager/get_openart_auth")
async def api_get_openart_auth(request):
    # print("Getting stored Matrix credentials...")
    openart_key = get_openart_auth()
    if not openart_key:
        return web.Response(status=404)
    return web.json_response({"openart_key": openart_key})


@server.PromptServer.instance.routes.post("/manager/set_openart_auth")
async def api_set_openart_auth(request):
    json_data = await request.json()
    openart_key = json_data['openart_key']
    with open(os.path.join(comfyui_manager_path, ".openart_key"), "w") as f:
        f.write(openart_key)
    return web.Response(status=200)


@server.PromptServer.instance.routes.get("/manager/get_matrix_auth")
async def api_get_matrix_auth(request):
    # print("Getting stored Matrix credentials...")
    matrix_auth = get_matrix_auth()
    if not matrix_auth:
        return web.Response(status=404)
    return web.json_response(matrix_auth)


@server.PromptServer.instance.routes.get("/manager/get_comfyworkflows_auth")
async def api_get_comfyworkflows_auth(request):
    # Check if the user has provided Matrix credentials in a file called 'matrix_accesstoken'
    # in the same directory as the ComfyUI base folder
    # print("Getting stored Comfyworkflows.com auth...")
    comfyworkflows_auth = get_comfyworkflows_auth()
    if not comfyworkflows_auth:
        return web.Response(status=404)
    return web.json_response({"comfyworkflows_sharekey" : comfyworkflows_auth})


def set_matrix_auth(json_data):
    homeserver = json_data['homeserver']
    username = json_data['username']
    password = json_data['password']
    with open(os.path.join(comfyui_manager_path, "matrix_auth"), "w") as f:
        f.write("\n".join([homeserver, username, password]))


def set_comfyworkflows_auth(comfyworkflows_sharekey):
    with open(os.path.join(comfyui_manager_path, "comfyworkflows_sharekey"), "w") as f:
        f.write(comfyworkflows_sharekey)


def has_provided_matrix_auth(matrix_auth):
    return matrix_auth['homeserver'].strip() and matrix_auth['username'].strip() and matrix_auth['password'].strip()


def has_provided_comfyworkflows_auth(comfyworkflows_sharekey):
    return comfyworkflows_sharekey.strip()


@server.PromptServer.instance.routes.post("/manager/share")
async def share_art(request):
    # get json data
    json_data = await request.json()

    matrix_auth = json_data['matrix_auth']
    comfyworkflows_sharekey = json_data['cw_auth']['cw_sharekey']

    set_matrix_auth(matrix_auth)
    set_comfyworkflows_auth(comfyworkflows_sharekey)

    share_destinations = json_data['share_destinations']
    credits = json_data['credits']
    title = json_data['title']
    description = json_data['description']
    is_nsfw = json_data['is_nsfw']
    prompt = json_data['prompt']
    potential_outputs = json_data['potential_outputs']
    selected_output_index = json_data['selected_output_index']
    
    try:
        output_to_share = potential_outputs[int(selected_output_index)]
    except:
        # for now, pick the first output
        output_to_share = potential_outputs[0]
        
    assert output_to_share['type'] in ('image', 'output')
    output_dir = folder_paths.get_output_directory()

    if output_to_share['type'] == 'image':
        asset_filename = output_to_share['image']['filename']
        asset_subfolder = output_to_share['image']['subfolder']

        if output_to_share['image']['type'] == 'temp':
            output_dir = folder_paths.get_temp_directory()
    else:
        asset_filename = output_to_share['output']['filename']
        asset_subfolder = output_to_share['output']['subfolder']

    if asset_subfolder:
        asset_filepath = os.path.join(output_dir, asset_subfolder, asset_filename)
    else:
        asset_filepath = os.path.join(output_dir, asset_filename)

    # get the mime type of the asset
    assetFileType = mimetypes.guess_type(asset_filepath)[0]

    if "comfyworkflows" in share_destinations:
        share_website_host = "https://comfyworkflows.com"
        share_endpoint = f"{share_website_host}/api"
        
        # get presigned urls
        async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(
                f"{share_endpoint}/get_presigned_urls",
                json={
                    "assetFileName": asset_filename,
                    "assetFileType": assetFileType,
                    "workflowJsonFileName" : 'workflow.json',
                    "workflowJsonFileType" : 'application/json',

                },
            ) as resp:
                assert resp.status == 200
                presigned_urls_json = await resp.json()
                assetFilePresignedUrl = presigned_urls_json["assetFilePresignedUrl"]
                assetFileKey = presigned_urls_json["assetFileKey"]
                workflowJsonFilePresignedUrl = presigned_urls_json["workflowJsonFilePresignedUrl"]
                workflowJsonFileKey = presigned_urls_json["workflowJsonFileKey"]

        # upload asset
        async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.put(assetFilePresignedUrl, data=open(asset_filepath, "rb")) as resp:
                assert resp.status == 200

        # upload workflow json
        async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.put(workflowJsonFilePresignedUrl, data=json.dumps(prompt['workflow']).encode('utf-8')) as resp:
                assert resp.status == 200

        # make a POST request to /api/upload_workflow with form data key values
        async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            form = aiohttp.FormData()
            if comfyworkflows_sharekey:
                form.add_field("shareKey", comfyworkflows_sharekey)
            form.add_field("source", "comfyui_manager")
            form.add_field("assetFileKey", assetFileKey)
            form.add_field("assetFileType", assetFileType)
            form.add_field("workflowJsonFileKey", workflowJsonFileKey)
            form.add_field("sharedWorkflowWorkflowJsonString", json.dumps(prompt['workflow']))
            form.add_field("sharedWorkflowPromptJsonString", json.dumps(prompt['output']))
            form.add_field("shareWorkflowCredits", credits)
            form.add_field("shareWorkflowTitle", title)
            form.add_field("shareWorkflowDescription", description)
            form.add_field("shareWorkflowIsNSFW", str(is_nsfw).lower())

            async with session.post(
                f"{share_endpoint}/upload_workflow",
                data=form,
            ) as resp:
                assert resp.status == 200
                upload_workflow_json = await resp.json()
                workflowId = upload_workflow_json["workflowId"]

    # check if the user has provided Matrix credentials
    if "matrix" in share_destinations:
        comfyui_share_room_id = '!LGYSoacpJPhIfBqVfb:matrix.org'
        filename = os.path.basename(asset_filepath)
        content_type = assetFileType

        try:
            from matrix_client.api import MatrixHttpApi
            from matrix_client.client import MatrixClient

            homeserver = 'matrix.org'
            if matrix_auth:
                homeserver = matrix_auth.get('homeserver', 'matrix.org')
            homeserver = homeserver.replace("http://", "https://")
            if not homeserver.startswith("https://"):
                homeserver = "https://" + homeserver
            
            client = MatrixClient(homeserver)
            try:
                token = client.login(username=matrix_auth['username'], password=matrix_auth['password'])
                if not token:
                    return web.json_response({"error" : "Invalid Matrix credentials."}, content_type='application/json', status=400)
            except:
                return web.json_response({"error" : "Invalid Matrix credentials."}, content_type='application/json', status=400)

            matrix = MatrixHttpApi(homeserver, token=token)
            with open(asset_filepath, 'rb') as f:
                mxc_url = matrix.media_upload(f.read(), content_type, filename=filename)['content_uri']
                        
            workflow_json_mxc_url = matrix.media_upload(prompt['workflow'], 'application/json', filename='workflow.json')['content_uri']

            text_content = ""
            if title:
                text_content += f"{title}\n"
            if description:
                text_content += f"{description}\n"
            if credits:
                text_content += f"\ncredits: {credits}\n"
            response = matrix.send_message(comfyui_share_room_id, text_content)
            response = matrix.send_content(comfyui_share_room_id, mxc_url, filename, 'm.image')
            response = matrix.send_content(comfyui_share_room_id, workflow_json_mxc_url, 'workflow.json', 'm.file')
        except:
            import traceback
            traceback.print_exc()
            return web.json_response({"error" : "An error occurred when sharing your art to Matrix."}, content_type='application/json', status=500)
    
    return web.json_response({
        "comfyworkflows" : {
            "url" : None if "comfyworkflows" not in share_destinations else f"{share_website_host}/workflows/{workflowId}",
        },
        "matrix" : {
            "success" : None if "matrix" not in share_destinations else True
        }
    }, content_type='application/json', status=200)


import asyncio
async def default_cache_update():
    async def get_cache(filename):
        uri = 'https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/' + filename
        cache_uri = str(simple_hash(uri)) + '_' + filename
        cache_uri = os.path.join(cache_dir, cache_uri)

        json_obj = await get_data(uri)

        with cache_lock:
            with open(cache_uri, "w", encoding='utf-8') as file:
                json.dump(json_obj, file, indent=4, sort_keys=True)
                print(f"[ComfyUI-Manager] default cache updated: {uri}")

    a = get_cache("custom-node-list.json")
    b = get_cache("extension-node-map.json")
    c = get_cache("model-list.json")
    d = get_cache("alter-list.json")

    await asyncio.gather(a, b, c, d)

threading.Thread(target=lambda: asyncio.run(default_cache_update())).start()


WEB_DIRECTORY = "js"
NODE_CLASS_MAPPINGS = {}
__all__ = ['NODE_CLASS_MAPPINGS']

