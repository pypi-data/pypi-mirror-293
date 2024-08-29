from typing import List

import requests

from empaia_app_test_suite.constants import JOB_MODES, STATIC_ALT_USER_ID, STATIC_CASE_ID, STATIC_USER_ID
from empaia_app_test_suite.custom_models import WsiInput


def get_or_create_static_case(mds_url, alt_user):
    user_id = STATIC_ALT_USER_ID if alt_user else STATIC_USER_ID
    r = requests.get(f"{mds_url}/v3/cases/{STATIC_CASE_ID}")
    if r.status_code == 400:
        data = {
            "description": "A very interesting example case",
            "id": STATIC_CASE_ID,
            "creator_id": user_id,
            "creator_type": "USER",
        }
        r = requests.post(f"{mds_url}/private/v3/cases", json=data, params={"external_ids": True})
        r.raise_for_status()


def get_or_create_examination(mds_url, app_id, alt_user):
    user_id = STATIC_ALT_USER_ID if alt_user else STATIC_USER_ID
    examination = {"case_id": STATIC_CASE_ID, "app_id": app_id, "creator_id": user_id, "creator_type": "USER"}
    r = requests.put(f"{mds_url}/v3/examinations", json=examination)
    r.raise_for_status()
    ex = r.json()
    return ex


def get_or_create_scope(mds_url, ex_id, alt_user):
    # create or get scope
    user_id = STATIC_ALT_USER_ID if alt_user else STATIC_USER_ID
    data = {"examination_id": ex_id, "user_id": user_id}
    r = requests.put(f"{mds_url}/v3/scopes", json=data)
    r.raise_for_status()
    return r.json()["id"]


def add_job_to_examination(mds_url, job_id, ex_id):
    # add job to examination
    r = requests.put(f"{mds_url}/v3/examinations/{ex_id}/jobs/{job_id}/add")
    r.raise_for_status()


def register_wsis(wsis_to_register: List[WsiInput], mds_url: str):
    url_cds = f"{mds_url}/private/v3/slides"
    for wsi_info in wsis_to_register:
        # CDS
        post_data_cds = {
            "tissue": wsi_info.tissue,
            "stain": wsi_info.stain,
            "block": wsi_info.block,
            "id": wsi_info.id,
            "case_id": STATIC_CASE_ID,
            "main_path": wsi_info.path,
        }
        r = requests.post(url_cds, json=post_data_cds, params={"external_ids": True})
        r.raise_for_status()
    wsi_ids = [wsi.id for wsi in wsis_to_register]
    return wsi_ids


def create_job(app_id: str, mds_url: str, job_mode: str, creator_id: str, creator_type: str = "SCOPE"):
    job = {
        "app_id": app_id,
        "creator_id": creator_id,
        "creator_type": creator_type,
        "mode": JOB_MODES[job_mode],
        "containerized": True,
    }
    r = requests.post(f"{mds_url}/v3/jobs", json=job)
    r.raise_for_status()
    data = r.json()
    job_id = data["id"]
    r = requests.get(f"{mds_url}/v3/jobs/{job_id}/token")
    r.raise_for_status()
    data = r.json()
    return job_id, data["access_token"]


def post_job_inputs(job_id: str, job_inputs: dict, mds_url: str):
    for input_key, input_id in job_inputs.items():
        r = requests.put(f"{mds_url}/v3/jobs/{job_id}/inputs/{input_key}", json={"id": input_id})
        r.raise_for_status()


def set_job_statuses(job_id: str, mds_url: str, statuses: List[str]):
    for s in statuses:
        try:
            r = requests.put(f"{mds_url}/v3/jobs/{job_id}/status", json={"status": s})
            r.raise_for_status()
        except requests.HTTPError as e:
            msg = r.text
            if s in ["READY", "RUNNING"]:
                error_msg = f"Could not change job status to '{s}'. Job was started already. Error: {msg}"
                raise Exception(error_msg) from e
            else:
                raise e


def post_collection(data: str, mds_url: str, params: dict):
    empty_collection = {}
    for key in data:
        if key == "items":
            empty_collection[key] = []
        else:
            empty_collection[key] = data[key]
    r = requests.post(f"{mds_url}/v3/collections", json=empty_collection, params=params)
    r.raise_for_status()
    empty_collection = r.json()
    collection = extend_collection(empty_collection, data["items"], mds_url, params)
    return collection


def extend_collection(empty_collection: dict, items: dict, mds_url: str, params: dict, batch_size: int = 1000):
    inner_type = empty_collection["item_type"]
    skip = 0
    while skip < len(items):
        batch = {"items": []}
        if inner_type == "collection":
            for item in items[skip : skip + batch_size]:
                inner_collection = {}
                for key in item:
                    if key == "items":
                        inner_collection[key] = []
                    else:
                        inner_collection[key] = item[key]
                batch["items"].append(inner_collection)
            r = requests.post(f"{mds_url}/v3/collections/{empty_collection['id']}/items", json=batch, params=params)
            r.raise_for_status()
            posted_collections = r.json()
            for collection in posted_collections["items"]:
                for orig_collection in items:
                    if orig_collection["id"] == collection["id"]:
                        collection = extend_collection(collection, orig_collection["items"], mds_url, params)
            if "items" not in empty_collection:
                empty_collection["items"] = []
            empty_collection["items"] += posted_collections["items"]
        else:
            batch["items"] += items[skip : skip + batch_size]
            r = requests.post(f"{mds_url}/v3/collections/{empty_collection['id']}/items", json=batch, params=params)
            r.raise_for_status()
            posted_items = r.json()
            if "items" not in empty_collection:
                empty_collection["items"] = []
            empty_collection["items"] += posted_items["items"]
        skip += batch_size
    return empty_collection


def get_collections_items(collection: dict, mds_url, batch_size: int = 1000):
    if collection["item_type"] == "collection":
        for inner in collection["items"]:
            inner = get_collections_items(inner, mds_url, batch_size)
    else:
        skip = 0
        limit = batch_size
        if "items" not in collection:
            collection["items"] = []
        while skip < collection["item_count"]:
            params = {"skip": skip, "limit": limit}
            r = requests.put(f"{mds_url}/v3/collections/{collection['id']}/items/query", json={}, params=params)
            r.raise_for_status()
            batch = r.json()["items"]
            collection["items"] += batch
            skip += batch_size
    return collection


def get_collection(collection_id: str, mds_url: str, batch_size: int = 1000, shallow: bool = False):
    try:
        r = requests.get(f"{mds_url}/v3/collections/{collection_id}", params={"shallow": shallow})
        r.raise_for_status()
        collection = r.json()
        if shallow:
            return collection
    except requests.exceptions.HTTPError as error:
        if "Request Entity Too Large" not in str(error):
            raise error
        r = requests.get(f"{mds_url}/v3/collections/{collection_id}?shallow=true")
        r.raise_for_status()
        collection = r.json()
        collection = get_collections_items(collection, mds_url, batch_size)
    return collection


def get_annotation(annotation_id: str, mds_url: str):
    url = f"{mds_url}/v3/annotations/{annotation_id}"
    params = {"with_classes": True}
    raw_annotation = requests.get(url, params=params)
    return raw_annotation.json()


def get_job(job_id: str, mds_url: str):
    url = f"{mds_url}/v3/jobs/{job_id}"
    r = requests.get(url)
    r.raise_for_status()
    job = r.json()
    return job
