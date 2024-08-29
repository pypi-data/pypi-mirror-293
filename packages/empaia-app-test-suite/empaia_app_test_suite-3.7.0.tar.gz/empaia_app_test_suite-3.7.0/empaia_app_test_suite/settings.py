import os
import pathlib
import shutil

import toml
import yaml
from dotenv import dotenv_values
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from empaia_app_test_suite import __version__
from empaia_app_test_suite.constants import STATIC_ALT_USER_ID, STATIC_ORGANIZATION_ID, STATIC_USER_ID

EATS_NET = "eats"
CDS_BASE_PLUGINS = "cds-plugin-tiffslide|cds-plugin-wsidicom|cds-plugin-pil;1|cds-plugin-tifffile|cds-plugin-openslide"


def get_docker_compose_dict():
    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_docker_compose_file = os.path.join(path_to_this_file, "services", "docker-compose.yml")
    with open(path_to_docker_compose_file, encoding="utf-8") as stream:
        return yaml.safe_load(stream)


class JobEnv:
    class JobEnvSettings(BaseModel):
        empaia_job_id: str
        empaia_token: str
        empaia_app_api: str

    def __init__(self, env_file, encoding="utf-8"):
        values = dotenv_values(env_file, encoding=encoding)
        values = {key.lower(): val for key, val in values.items()}
        self.settings = self.JobEnvSettings(**values)


class EatsSettings(BaseSettings):
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="eats_", env_file=".env")


def get_databases():
    docker_compose_dict = get_docker_compose_dict()
    return [
        {
            "name": "eats-postgres-db",
            "image": docker_compose_dict["services"]["eats-postgres-db"]["image"],
            "command": "postgres -c config_file=/etc/postgresql/postgresql.conf",
            "environment": {
                "POSTGRES_DB": "eats",
                "POSTGRES_USER": "empaia",
                "POSTGRES_PASSWORD": "empaia",
            },
            "volume": {
                "name": "eats-postgres-db-vol",
                "mount": "/var/lib/postgresql/data",
            },
        },
        {
            "name": "eats-mongo-db",
            "image": docker_compose_dict["services"]["eats-mongo-db"]["image"],
            "environment": {},
            "volume": {
                "name": "eats-mongo-db-vol",
                "mount": "/data/db",
            },
        },
    ]


def get_services(
    nginx_port=None,
    wbs_url=None,
    isyntax_sdk=None,
    mirax_plugin=None,
    gpu_driver=None,
    frontend_token_exp=None,
    scope_token_exp=None,
    app_ui_frame_ancestors=None,
    app_ui_connect_src=None,
    app_ui_disable_csp=False,
):
    nginx_port = nginx_port or 8888
    frontend_token_exp = frontend_token_exp or 86400
    scope_token_exp = scope_token_exp or 86400

    jes_gpu_worker = ";" if gpu_driver else ""
    jes_cpu_worker = ";x1" if not gpu_driver else ""

    wbs_url = wbs_url.rstrip("/") if wbs_url else f"http://localhost:{nginx_port}/wbs-api"

    cds_plugins = CDS_BASE_PLUGINS
    if isyntax_sdk:
        cds_plugins = "cds-plugin-isyntax|" + cds_plugins
    if mirax_plugin:
        cds_plugins = "cds-plugin-mirax|" + cds_plugins

    if app_ui_frame_ancestors is None:
        app_ui_frame_ancestors = ""

    if app_ui_connect_src is None:
        app_ui_connect_src = ""

    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_services = os.path.join(path_to_this_file, "services")
    default_version = f"eats-{__version__}"

    docker_compose_dict = get_docker_compose_dict()

    services = []

    # check for isyntax sdk
    isyntax_sdk_path = os.path.join(
        path_to_services,
        "clinical_data_service/wsi_format_plugins/isyntax",
        "philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip",
    )
    if isyntax_sdk:
        shutil.copy(isyntax_sdk, isyntax_sdk_path)
        services.append(
            {
                "name": "cds-plugin-isyntax",
                "dockerfile_path": str(
                    pathlib.Path(path_to_services, "clinical_data_service/wsi_format_plugins/isyntax/Dockerfile")
                ),
                "environment": {"PLUGIN_ISYNTAX_DATA_DIR": "/data"},
                "ports": {},
                "command": [],
                "path": str(pathlib.Path(path_to_services, "clinical_data_service/wsi_format_plugins")),
            }
        )

    # check for mirax
    mirax_plugin_path = os.path.join(
        path_to_services,
        "clinical_data_service/wsi_format_plugins/mirax",
        "mirax_backend.zip",
    )
    if mirax_plugin:
        shutil.copy(mirax_plugin, mirax_plugin_path)
        services.append(
            {
                "name": "cds-plugin-mirax",
                "dockerfile_path": str(
                    pathlib.Path(path_to_services, "clinical_data_service/wsi_format_plugins/mirax/Dockerfile")
                ),
                "environment": {"CPM_DATA_DIR": "/data"},
                "ports": {},
                "command": [],
                "path": str(pathlib.Path(path_to_services, "clinical_data_service/wsi_format_plugins/mirax")),
            }
        )

    services.extend(
        [
            {
                "name": "app-service",
                "image": docker_compose_dict["services"]["app-service"]["image"],
                "environment": {
                    "AS_MPS_URL": "http://marketplace-service-mock:8000",
                    "AS_MPS_USE_V1_ROUTES": "True",
                    "AS_CLIENT_ID": "mustnotbeempty",
                    "AS_CLIENT_SECRET": "mustnotbeempty",
                    "AS_MDS_URL": "http://medical-data-service:8000",
                    "AS_ROOT_PATH": "/app-api",
                    "NO_PROXY": "marketplace-service-mock,medical-data-service,mustnotbeempty",
                    "AS_ORGANIZATION_ID": STATIC_ORGANIZATION_ID,
                    "AS_ENABLE_TOKEN_VERIFICATION": True,
                },
                "command": ["--port=8000", "--host=0.0.0.0", "--root-path=/app-api"],
                "ports": {},
            },
            {
                "name": "pixelmapd",
                "image": docker_compose_dict["services"]["pixelmapd"]["image"],
                "environment": {
                    "PMD_PORT": 5556,
                    "PMD_DATA_PATH": "/app/data/pixelmaps/",
                },
                "command": ["annotctl", "pixelmapd"],
                "ports": {},
                "volume": {
                    "name": "annot-data-vol",
                    "mount": "/app/data/pixelmaps",
                },
            },
            {
                "name": "annotation-service",
                "image": docker_compose_dict["services"]["annotation-service"]["image"],
                "environment": {
                    "ANNOT_DB_HOST": "eats-postgres-db",
                    "ANNOT_DB_PORT": 5432,
                    "ANNOT_DB": "eats",
                    "ANNOT_DB_USERNAME": "empaia",
                    "ANNOT_DB_PASSWORD": "empaia",
                    "ANNOT_API_V1_INTEGRATION": "annotation_service.api.v1.integrations.disable_auth:DisableAuth",
                    "ANNOT_API_V3_INTEGRATION": "annotation_service.api.v3.integrations.disable_auth:DisableAuth",
                    "ANNOT_ALLOW_EXTERNAL_IDS": "True",
                    "ANNOT_V1_ITEM_LIMIT": 10000,
                    "ANNOT_V1_POST_LIMIT": 10000,
                    "ANNOT_V3_ITEM_LIMIT": 10000,
                    "ANNOT_V3_POST_LIMIT": 10000,
                    "ANNOT_ENABLE_PROFILER": False,
                    "ANNOT_ENABLE_FILE_PROFILER": False,
                    "ANNOT_PIXELMAPS_DATA_PATH": "/app/data/pixelmaps/",
                    "ANNOT_CDS_URL": "http://clinical-data-service:8000",
                    "NO_PROXY": "eats-postgres-db, clinical-data-service",
                },
                "command": ["run.sh", "--host=0.0.0.0", "--workers=4", "--port=8000"],
                "ports": {},
                "volume": {
                    "name": "annot-data-vol",
                    "mount": "/app/data/pixelmaps",
                },
            },
            {
                "name": "job-service",
                "image": docker_compose_dict["services"]["job-service"]["image"],
                "environment": {
                    "JS_DB_HOST": "eats-postgres-db",
                    "JS_DB_PORT": 5432,
                    "JS_DB": "eats",
                    "JS_DB_USERNAME": "empaia",
                    "JS_DB_PASSWORD": "empaia",
                    "JS_RSA_KEYS_DIRECTORY": "/app/rsa",
                    "NO_PROXY": "eats-postgres-db, annotation-service",
                    "JS_ANNOT_URL": "http://annotation-service:8000",
                },
                "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
                "ports": {},
                "volume": {
                    "name": "js-rsa-vol",
                    "mount": "/opt/app/rsa",
                },
            },
            {
                "name": "examination-service",
                "image": docker_compose_dict["services"]["examination-service"]["image"],
                "environment": {
                    "ES_DB_HOST": "eats-postgres-db",
                    "ES_DB_PORT": 5432,
                    "ES_DB": "eats",
                    "ES_DB_USERNAME": "empaia",
                    "ES_DB_PASSWORD": "empaia",
                    "ES_SCOPE_TOKEN_EXP": scope_token_exp,
                    "ES_API_V1_INTEGRATION": "examination_service.api.v1.integrations.disable_auth:DisableAuth",
                    "NO_PROXY": "eats-postgres-db",
                },
                "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
                "ports": {},
                "volume": {
                    "name": "es-rsa-vol",
                    "mount": "/opt/app/rsa",
                },
            },
            {
                "name": "cds-plugin-openslide",
                "image": docker_compose_dict["services"]["cds-plugin-openslide"]["image"],
                "environment": {"PLUGIN_OPENSLIDE_DATA_DIR": "/data"},
            },
            {
                "name": "cds-plugin-tiffslide",
                "image": docker_compose_dict["services"]["cds-plugin-tiffslide"]["image"],
                "environment": {"PLUGIN_TIFFSLIDE_DATA_DIR": "/data"},
            },
            {
                "name": "cds-plugin-tifffile",
                "image": docker_compose_dict["services"]["cds-plugin-tifffile"]["image"],
                "environment": {"PLUGIN_TIFFFILE_DATA_DIR": "/data"},
            },
            {
                "name": "cds-plugin-pil",
                "image": docker_compose_dict["services"]["cds-plugin-pil"]["image"],
                "environment": {"PLUGIN_PIL_DATA_DIR": "/data"},
            },
            {
                "name": "cds-plugin-wsidicom",
                "image": docker_compose_dict["services"]["cds-plugin-wsidicom"]["image"],
                "environment": {"PLUGIN_WSIDICOM_DATA_DIR": "/data"},
            },
            {
                "name": "clinical-data-service",
                "image": docker_compose_dict["services"]["clinical-data-service"]["image"],
                "environment": {
                    "CDS_DB_HOST": "eats-postgres-db",
                    "CDS_DB_PORT": 5432,
                    "CDS_DB": "eats",
                    "CDS_DB_USERNAME": "empaia",
                    "CDS_DB_PASSWORD": "empaia",
                    "CDS_DATA_DIR": "/data",
                    "CDS_MAX_RETURNED_REGION_SIZE": 25000000,
                    "CDS_PLUGIN_ADDRESSES": cds_plugins,
                    "CDS_MIGRATION_STORAGE_ADDRESS_LEGACY_DATA_DIR": "/data",
                    "CDS_ALLOW_EXTERNAL_IDS": "True",
                    "NO_PROXY": "eats-postgres-db",
                },
                "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
                "ports": {},
            },
            {
                "name": "medical-data-service",
                "image": docker_compose_dict["services"]["medical-data-service"]["image"],
                "environment": {
                    "MDS_API_INTEGRATION": "medical_data_service.api.integrations.disable_auth:DisableAuth",
                    "MDS_JS_URL": "http://job-service:8000",
                    "MDS_AS_URL": "http://annotation-service:8000",
                    "MDS_CDS_URL": "http://clinical-data-service:8000",
                    "MDS_ES_URL": "http://examination-service:8000",
                    "MDS_ROOT_PATH": "/mds-api",
                    "MDS_ENABLE_STORAGE_ROUTES": True,
                    "NO_PROXY": "job-service,annotation-service,clinical-data-service,examination-service",
                },
                "command": [
                    "uvicorn",
                    "--host=0.0.0.0",
                    "--port=8000",
                    "--workers=2",
                    "--root-path=/mds-api",
                    "medical_data_service.app:app",
                ],
                "ports": {},
            },
            {
                "name": "marketplace-service-mock",
                "image": docker_compose_dict["services"]["marketplace-service-mock"]["image"],
                "environment": {
                    "MPSM_API_INTEGRATION": "marketplace_service_mock.api.integrations.disable_auth:DisableAuth",
                    "MPSM_ROOT_PATH": "/mps-api",
                    "MPSM_DISABLE_API_V0": "True",
                    "MPSM_ENABLE_API_V1": "True",
                },
                "command": [
                    "uvicorn",
                    "--host=0.0.0.0",
                    "--port=8000",
                    "--root-path=/mps-api",
                    "marketplace_service_mock.app:app",
                ],
                "ports": {},
                "volume": {
                    "name": "marketplace-service-mock-vol",
                    "mount": "/data",
                },
            },
            {
                "name": "aaa-service-mock",
                "image": docker_compose_dict["services"]["aaa-service-mock"]["image"],
                "environment": {
                    "AAAM_API_INTEGRATION": "aaa_service_mock.api.integrations.disable_auth:DisableAuth",
                    "AAAM_ROOT_PATH": "/aaa-api",
                },
                "command": [
                    "uvicorn",
                    "--host=0.0.0.0",
                    "--port=8000",
                    "--root-path=/aaa-api",
                    "aaa_service_mock.app:app",
                ],
                "ports": {},
                "volume": {
                    "name": "aaa-service-mock-vol",
                    "mount": "/data",
                },
            },
            {
                "name": "job-execution-service",
                "image": docker_compose_dict["services"]["job-execution-service"]["image"],
                "environment": {
                    "JES_DATABASE_URL": "mongodb://eats-mongo-db:27017",
                    "JES_DOCKER_NETWORK": EATS_NET,
                    "JES_DOCKER_GPU_DRIVER": gpu_driver,
                    "JES_WORKER_STANDALONE_GPU": jes_gpu_worker,
                    "JES_WORKER_STANDALONE_CPU": jes_cpu_worker,
                    "JES_WORKER_STANDALONE_PROXY": "",
                    "JES_WORKER_PREPROCESSING_GPU": "",
                    "JES_WORKER_PREPROCESSING_CPU": "",
                    "JES_WORKER_PREPROCESSING_PROXY": "",
                    "JES_DOCKER_HOST": "",
                    "JES_DOCKER_GPU_COUNT": 1,
                    "JES_JOB_RUNNER": "EVENTED",
                    "JES_ENABLE_RECEIVER_AUTH": "False",
                    "JES_DOCKER_ALWAYS_PULL": "False",
                    "JES_MPS_URL": "http://marketplace-service-mock:8000",
                    "JES_MPS_USE_V1_ROUTES": "True",
                    "JES_ROOT_PATH": "/jes-api",
                    "JES_IDP_URL": "",
                    "JES_AUDIENCE": "org.empaia.auth.jes",
                    "JES_CLIENT_ID": "",
                    "JES_CLIENT_SECRET": "",
                    "JES_OPENAPI_TOKEN_URL": "",
                    "NO_PROXY": "eats-mongo-db,marketplace-service-mock",
                },
                "command": [],
                "ports": {},
                "volume": {
                    "name": "/var/run/docker.sock",
                    "mount": "/var/run/docker.sock",
                },
            },
            {
                "name": "workbench-daemon",
                "image": docker_compose_dict["services"]["workbench-daemon"]["image"],
                "environment": {
                    "WBS_MEDICAL_DATA_SERVICE_URL": "http://medical-data-service:8000",
                    "WBS_JOB_EXECUTION_SERVICE_URL": "http://job-execution-service:8000",
                    "WBS_APP_SERVICE_URL": "http://app-service:8000",
                    "WBS_MARKETPLACE_SERVICE_URL": "http://marketplace-service-mock:8000",
                    "WBS_ORGANIZATION_ID": STATIC_ORGANIZATION_ID,
                    "NO_PROXY": "medical-data-service,job-execution-service,marketplace-service-mock",
                    "WBS_CLIENT_ID": "wbs",
                    "WBS_DEBUG": "True",
                    "WBS_ENABLE_EATS_MODE": "True",
                },
                "command": ["wbd"],
                "ports": {},
            },
            {
                "name": "workbench-service",
                "image": docker_compose_dict["services"]["workbench-service"]["image"],
                "environment": {
                    "WBS_ENABLE_EATS_MODE": "True",
                    "WBS_AAA_SERVICE_URL": "http://aaa-service-mock:8000",
                    "WBS_MEDICAL_DATA_SERVICE_URL": "http://medical-data-service:8000",
                    "WBS_APP_SERVICE_URL": "http://app-service:8000",
                    "WBS_JOB_EXECUTION_SERVICE_URL": "http://job-execution-service:8000",
                    "WBS_MARKETPLACE_SERVICE_URL": "http://marketplace-service-mock:8000",
                    "WBS_CORS_ALLOW_ORIGINS": '["*"]',
                    "WBS_API_V1_INTEGRATION": "workbench_service.api.v1.integrations.disable_auth:DisableAuth",
                    "WBS_API_V2_INTEGRATION": "workbench_service.api.v2.integrations.disable_auth:DisableAuth",
                    "WBS_API_V3_INTEGRATION": "workbench_service.api.v3.integrations.disable_auth:DisableAuth",
                    "WBS_ORGANIZATION_ID": STATIC_ORGANIZATION_ID,
                    "WBS_CLIENT_ID": "wbs",
                    "WBS_FRONTEND_TOKEN_EXP": frontend_token_exp,
                    # "WBS_ROOT_PATH": "/wbs-api",
                    "WBS_APP_UI_FRAME_ANCESTORS": app_ui_frame_ancestors,
                    "WBS_APP_UI_CONNECT_SRC": app_ui_connect_src,
                    "NO_PROXY": (
                        "aaa-service-mock,medical-data-service,app-service,job-execution-service,"
                        "marketplace-service-mock,workbench-client-v3-generic-ui"
                    ),
                    "WBS_GENERIC_APP_UI_V3_URL": "http://workbench-client-v3-generic-ui",
                    "WBS_FRONTEND_CSP_URL": f"http://localhost:{nginx_port}",
                    "WBS_DISABLE_CSP_SETTINGS": app_ui_disable_csp,
                    "WBS_DISABLE_MULTI_USER": False,
                },
                "command": [
                    "run.sh",
                    "--host=0.0.0.0",
                    "--port=8000",
                    "--root-path=/wbs-api",
                ],
                "ports": {},
                "extra_hosts": {"host.docker.internal": "host-gateway"},
                "volume": {
                    "name": "wbs-rsa-vol",
                    "mount": "/opt/app/rsa",
                },
            },
            {
                "name": "workbench-client-v3",
                "image": docker_compose_dict["services"]["workbench-client-v3"]["image"],
                "environment": {
                    "WBC_WBS_SERVER_API_URL": wbs_url,
                    "WBC_WBS_USER_ID": STATIC_USER_ID,
                    "NO_PROXY": "localhost,127.0.0.1",
                },
                "ports": {},
                "command": [],
            },
            {
                "name": "workbench-client-v3-alt-user",
                "image": docker_compose_dict["services"]["workbench-client-v3"]["image"],
                "environment": {
                    "WBC_WBS_SERVER_API_URL": wbs_url,
                    "WBC_WBS_USER_ID": STATIC_ALT_USER_ID,
                    "NO_PROXY": "localhost,127.0.0.1",
                },
                "ports": {},
                "command": [],
            },
            {
                "name": "workbench-client-v3-sample-ui",
                "image": docker_compose_dict["services"]["workbench-client-v3-sample-ui"]["image"],
                "environment": {
                    "NO_PROXY": "localhost,127.0.0.1",
                },
                "command": [],
            },
            {
                "name": "workbench-client-v3-generic-ui",
                "image": docker_compose_dict["services"]["workbench-client-v3-generic-ui"]["image"],
                "environment": {
                    "NO_PROXY": "localhost,127.0.0.1",
                },
                "command": [],
            },
            {
                "name": "nginx",
                "environment": {},
                "path": str(pathlib.Path(path_to_services, "nginx")),
                "dockerfile_path": "Dockerfile",
                "ports": {"80": nginx_port},
                "command": [],
            },
        ]
    )

    for service in services:
        if "path" not in service:
            service["path"] = str(pathlib.Path(path_to_services, service["name"]))

        if "image" not in service:
            pyproject_file = pathlib.Path(service["path"], "pyproject.toml")
            version = default_version
            if pyproject_file.exists():
                version = toml.load(pyproject_file)["tool"]["poetry"]["version"]
            service["image"] = "eats-" + service["name"] + ":" + version

    return services
