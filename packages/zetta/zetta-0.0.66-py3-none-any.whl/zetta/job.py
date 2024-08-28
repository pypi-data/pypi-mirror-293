# Copyright ZettaBlock Labs 2024
import configparser
import json
import os
import requests
from typing import Any
import yaml
from zetta._utils.connections import ai_network_endpoints

from zetta.config_templates import lf_template
from zetta.cli.model import SERVICE_CREATE_MODEL_URL, SERVICE_GITEA_URL

WORKER_HOST = "http://44.222.138.39:8000"


def create_model_if_not_exist(
    model_name: str,
    description: str = None,
    license_type: str = "MIT",
    modality_type: str = "Text-to-Text",
    private: bool = False,
):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)

        profile_path = os.path.join(zetta_root, ".zetta/profile")
        config = configparser.ConfigParser()
        config.read(profile_path)
        user = config.get('default', 'user_name', fallback=None)
    except FileNotFoundError:
        raise Exception(f"Zetta secrets not found at {secrets_path}")
    except IOError:
        raise Exception(f"An error occurred while reading Zetta secrets {secrets_path}")

    # check if model already exists
    url = f"{SERVICE_GITEA_URL}/api/v1/repos/{user}/{model_name}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f'Found existing model repository {SERVICE_GITEA_URL}/{user}/{model_name}')
        return

    # create model repository
    headers = {
        "Authorization": token
    }

    json_data = {
        "type": "Model",
        "name": model_name,
        "license": license_type,
        "description": description,
        "private": private,
        "modality": modality_type
    }

    response = requests.post(SERVICE_CREATE_MODEL_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        print(f'Successfully created model repository {SERVICE_GITEA_URL}/{user}/{model_name}')
    else:
        response.raise_for_status()


def worker_health():
    url = f"{WORKER_HOST}/healthz"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get health: [{response.status_code}] {response.text}")


def worker_get_jobs(env: str, json_output=False):
    url = f"{ai_network_endpoints.get(env)}/task"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if json_output:
            return json.dumps(data, indent=2)
        else:
            return yaml.dump(data, default_flow_style=False)
    else:
        raise Exception(f"Failed to get jobs: [{response.status_code}] {response.text}")


def worker_get_job(uuid, env, json_output=False):
    url = f"{ai_network_endpoints.get(env)}/task/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if json_output:
            return json.dumps(data, indent=2)
        else:
            return yaml.dump(data, default_flow_style=False)
    else:
        raise Exception(f"Failed to get job: [{response.status_code}] {response.text}")


def worker_log_job(uuid):
    url = f"{WORKER_HOST}/logs/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["logs"]
    else:
        raise Exception(f"Failed to log job: [{response.status_code}] {response.text}")


def worker_run_job(
    config: dict[str, Any],
    user_name: str = None,
    user_email: str = None,
    gitea_reponame: str = None,
):
    if user_name is None or user_email is None:
        try:
            zetta_root = os.path.expanduser("~")
            profile_path = os.path.join(zetta_root, ".zetta/profile")
            profile = configparser.ConfigParser()
            profile.read(profile_path)
            user_name = profile.get('default', 'user_name', fallback=None)
            user_email = profile.get('default', 'email', fallback=None)
        except Exception as e:
            raise Exception(f"Failed to get user name or email: {e}")

    url = f"{WORKER_HOST}/lf/jobs"
    gitea_info = {
        "gitea_username": user_name,
        "gitea_email": user_email,
        # "gitea_password": None,
        # "private": True,
        "repo_name": gitea_reponame,
    }
    data = {
        "framework": "llama-factory",
        "config": config,
        "config_file_type": "json",
        "gitea_info": gitea_info,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to submit job: [{response.status_code}] {response.text}")


def safe_load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def safe_load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def process_zetta_job_config(config_path):
    raw_cfg = safe_load_yaml(config_path)
    output_model_name = raw_cfg["output_model_name"]
    output_model_fee = raw_cfg["output_model_fee"]
    print(f"Output model name: {output_model_name}, fee: {output_model_fee}")

    base_datasets = raw_cfg["base_datasets"]

    # dump llama-factory config.yml
    lf_config = dict(
        model_name_or_path=raw_cfg["base_model"]["name"],
        ### method
        stage=raw_cfg["stage"],
        do_train=raw_cfg["do_train"],
        finetuning_type=raw_cfg["finetuning_type"],
        lora_target=raw_cfg["lora_target"],
        # datasets
        dataset=','.join([i["name"] for i in base_datasets]),
        template=raw_cfg["template"],
        cutoff_len=raw_cfg["cutoff_len"],
        max_samples=raw_cfg["max_samples"],
        overwrite_cache=raw_cfg["overwrite_cache"],
        preprocessing_num_workers=raw_cfg["preprocessing_num_workers"],
        ### output
        output_dir=raw_cfg["output_dir"],
        logging_steps=raw_cfg["logging_steps"],
        save_steps=raw_cfg["save_steps"],
        plot_loss=raw_cfg["plot_loss"],
        overwrite_output_dir=raw_cfg["overwrite_output_dir"],
        ### train
        per_device_train_batch_size=raw_cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=raw_cfg["gradient_accumulation_steps"],
        learning_rate=raw_cfg["learning_rate"],
        num_train_epochs=raw_cfg["num_train_epochs"],
        lr_scheduler_type=raw_cfg["lr_scheduler_type"],
        warmup_ratio=raw_cfg["warmup_ratio"],
        bf16=raw_cfg["bf16"],
        ddp_timeout=raw_cfg["ddp_timeout"],
        ### eval
        val_size=raw_cfg["val_size"],
        per_device_eval_batch_size=raw_cfg["per_device_eval_batch_size"],
        eval_strategy=raw_cfg["eval_strategy"],
        eval_steps=raw_cfg["eval_steps"],
    )
    return lf_config, output_model_name


def init_zetta_job_config(project_name, location):
    if not os.path.exists(location):
        os.makedirs(location, exist_ok=True)
    path = f"{location}/config.yaml"
    with open(path, 'w') as file:
        file.write(lf_template.format(project_name))
    return path


""" Gitea interactions"""

def run_command(c):
    """
    Run command and return all its output at a time
    :param c: command in string
    :return: command output or err
    """
    import subprocess
    try:
        p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        rc = p.returncode
        return {'out': out, 'err': err, 'returncode': rc}
    except Exception as e:
        return {'err': e}


GITEA_REPO = "https://c2dfc8357c7461343b83e8af68bd96222aa8cc99@gitea.stag-vxzy.zettablock.com/ruimins/test_repo.git"
GITEA_REPO_PUBLIC = "https://gitea.stag-vxzy.zettablock.com/ruimins/test_repo"
commands_template = """
git clone {} {} &&
cd {} &&
git checkout -b {} &&
cp {} . &&
git add . &&
git commit -m "Add files for job {}" &&
git push origin {} &&
cd - &&
rm -rf {}
"""

def gitea_upload(config_path: str, job_id: str):
    config_path = os.path.abspath(config_path)
    tmp_path = os.path.abspath(f"{job_id}")
    os.makedirs(tmp_path, exist_ok=True)
    cmd = commands_template.format(GITEA_REPO, tmp_path, tmp_path, job_id, config_path, job_id, job_id, tmp_path)
    # return cmd
    try:
        res = run_command(cmd)
        if 'returncode' not in res or res['returncode'] != 0:
            raise Exception(res.get("err", "Unknown error"))
        # extract commit link
        out = res["out"].decode("utf-8")
        # example out: "[branch_name 33a1896] commit message"
        commit_hash = out.split("]")[0].split(" ")[-1]
        link = f"{GITEA_REPO_PUBLIC}/src/commit/{commit_hash}"
        return link
    except Exception:
        return None
