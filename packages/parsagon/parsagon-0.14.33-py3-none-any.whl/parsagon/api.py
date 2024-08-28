from json import JSONDecodeError
import time
from urllib.parse import quote

import httpx

from parsagon import settings
from parsagon.exceptions import APIException, ProgramNotFoundException
from parsagon.settings import get_save_api_key_interactive

environment = "PANDAS_1.x"


class RaiseProgramNotFound:
    def __init__(self, program_name):
        self.program_name = program_name

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and issubclass(exc_type, APIException):
            if exc_value.status_code == 404:
                raise ProgramNotFoundException(self.program_name)
        return False


def _request_to_exception(response):
    status_code = response.status_code
    if status_code == 500:
        raise APIException("A server error occurred. Please notify Parsagon.", status_code)
    if status_code in (502, 503, 504):
        raise APIException("Lost connection to server.", status_code)
    try:
        errors = response.json()
        if "detail" in errors and errors["detail"] == "Invalid token.":
            raise APIException("Invalid API key.", status_code)
        if "non_field_errors" in errors:
            raise APIException(errors["non_field_errors"], status_code)
        else:
            raise APIException(errors, status_code)
    except JSONDecodeError:
        raise APIException("Could not parse response.", status_code)


def _api_call(httpx_func, endpoint, output="json", **kwargs):
    """
    Calls `httpx_func` using the given endpoint. kwargs are passed to `httpx_func`

    Output mode can be "json" or "none".
    "json" returns the response as a deserialized JSON object.
    "none" returns None.

    If the request is not successful, an exception is thrown.
    """
    api_key = settings.get_api_key()
    api_endpoint = f"{settings.get_api_base()}/api{endpoint}"
    headers = {"Authorization": f"Token {api_key}"}
    r = httpx_func(api_endpoint, headers=headers, timeout=None, **kwargs)
    if not r.is_success:
        _request_to_exception(r)
    if output == "json":
        return r.json()
    elif output == "none":
        return
    else:
        raise Exception("Invalid output mode")


def get_program_sketches(description):
    """
    Gets a program sketches (full and abridged) from a description.
    :param description: Description in natural language that will be used to generate the scraping program.
    :return: A dict with keys "full", "abridged", and "pseudocode" for the respective program ASTs and pseudocode.
    """
    return _api_call(httpx.post, "/transformers/get-program-sketch/", json={"description": description})


def edit_program_sketch(sketch, description):
    return _api_call(
        httpx.post, "/transformers/edit-program-sketch/", json={"sketch": sketch, "description": description}
    )


def get_interaction_element_id(marked_html, description, task):
    """
    Gets a program sketches (full and abridged) from a description.
    :param marked_html: HTML with data-psgn-id attributes.
    :param description: A natural language description of the element.
    :return: The integer ID (data-psgn-id) of the element in the marked HTML.
    """
    result = _api_call(
        httpx.post,
        "/transformers/get-nav-elem/",
        json={"html": marked_html, "description": description, "task": task},
    )["id"]
    return result


def get_schema_fields(schema):
    """
    Gets fields and their types from a given schema
    :param schema:
    :return: A dict mapping fields to their types
    """
    return _api_call(httpx.post, "/transformers/get-schema-fields/", json={"schema": schema})


def get_cleaned_data(html, schema, nodes):
    """
    Gets cleaned data from the nodes to be scraped.
    :param html: HTML of the page to scrape
    :param schema: Schema of the data to scrape
    :param nodes: Nodes to scrape
    :return: Cleaned data
    """
    return _api_call(
        httpx.post, "/transformers/get-cleaned-data/", json={"html": html, "schema": schema, "nodes": nodes}
    )


def scrape_page(html, schema, task, full_html=None):
    """
    Scrapes data from the provided page HTML - data will be returned in the schema provided.
    :param html: HTML of the page to scrape.
    :param schema: Schema of the data to scrape
    :param task: The user's task
    :return: Scraped data
    """
    return _api_call(
        httpx.post,
        "/transformers/get-custom-data/",
        json={"html": html, "schema": schema, "task": task, "full_html": full_html},
    )


def poll_about_data(url, json):
    for _ in range(20):
        result = _api_call(httpx.post, url, json=json)
        if result["done"]:
            return result["result"]
        time.sleep(5)
    raise APIException("Request timed out")


def get_str_about_data(data, question, model=None):
    """
    Asks GPT a question about the given data.
    :param data: the data to give GPT
    :param question: the question to ask about the data
    """
    return poll_about_data("/transformers/get-str-about-data/", {"data": data, "question": question, "model": model})


def get_bool_about_data(data, question, model=None):
    """
    Asks GPT a question about the given data.
    :param data: the data to give GPT
    :param question: the question to ask about the data
    """
    return poll_about_data("/transformers/get-bool-about-data/", {"data": data, "question": question, "model": model})


def get_json_about_data(data, question, model=None):
    """
    Asks GPT a question about the given data.
    :param data: the data to give GPT
    :param question: the question to ask about the data
    """
    return poll_about_data("/transformers/get-json-about-data/", {"data": data, "question": question, "model": model})


def get_serp_data(url):
    """
    Get Google results
    :param url: the search url
    """
    return _api_call(httpx.post, "/transformers/get-serp-data/", json={"url": url})


def create_pipeline(name, description, program_sketch, pseudocode, secrets):
    return _api_call(
        httpx.post,
        "/pipelines/",
        json={
            "name": name,
            "description": description,
            "program_sketch": program_sketch,
            "pseudocode": pseudocode,
            "secrets": secrets,
        },
    )


def update_pipeline(pipeline_id, data):
    return _api_call(httpx.patch, f"/pipelines/{pipeline_id}/", json=data)


def delete_pipeline(pipeline_id):
    _api_call(httpx.delete, f"/pipelines/{pipeline_id}/", output="none")


def create_custom_function(pipeline_id, call_id, custom_function):
    _api_call(
        httpx.post,
        "/transformers/custom-function/",
        json={"pipeline": pipeline_id, "call_id": call_id, **custom_function.to_json()},
    )


def add_examples_to_custom_function(pipeline_id, call_id, custom_function, remove_old_examples):
    _api_call(
        httpx.post,
        "/transformers/custom-function/add-examples/",
        json={
            "pipeline": pipeline_id,
            "call_id": call_id,
            "remove_old_examples": remove_old_examples,
            **custom_function.to_json(),
        },
    )


def double_quote(string):
    """
    A bug in Django disallows URLs even with quoted slashes as in:
    /api/pipelines/name/stripe%2Fstuff/code/ HTTP/1.1" 405
    Therefore we must double quote
    """
    return quote(quote(string, safe=""), safe="")


def get_pipeline(pipeline_name):
    escaped_pipeline_name = double_quote(pipeline_name)
    with RaiseProgramNotFound(pipeline_name):
        return _api_call(
            httpx.get,
            f"/pipelines/name/{escaped_pipeline_name}/?double_escaped=True",
        )


def get_pipelines():
    return _api_call(httpx.get, f"/pipelines/")


def get_pipeline_code(pipeline_name, variables, headless, use_uc, optimize, use_proxy, pipeline_id=None):
    if pipeline_id:
        return _api_call(
            httpx.post,
            f"/pipelines/{pipeline_id}/code/",
            json={
                "variables": variables,
                "headless": headless,
                "use_uc": use_uc,
                "optimize": optimize,
                "use_proxy": use_proxy,
            },
        )
    escaped_pipeline_name = double_quote(pipeline_name)
    with RaiseProgramNotFound(pipeline_name):
        return _api_call(
            httpx.post,
            f"/pipelines/name/{escaped_pipeline_name}/code/?double_escaped=True",
            json={
                "variables": variables,
                "headless": headless,
                "use_uc": use_uc,
                "optimize": optimize,
                "use_proxy": use_proxy,
            },
        )


def get_pipeline_code_parts(pipeline_id):
    return _api_call(httpx.get, f"/pipelines/{pipeline_id}/code-parts/")


def create_pipeline_run(pipeline_id, variables, is_local):
    return _api_call(
        httpx.post,
        f"/pipelines/{pipeline_id}/runs/",
        json={"variables": variables, "is_local": is_local},
    )


def update_pipeline_run(run_id, data):
    return _api_call(
        httpx.patch,
        f"/pipelines/runs/{run_id}/",
        json=data,
    )


def get_run(run_id):
    """
    Gets details about a run
    """
    return _api_call(
        httpx.get,
        f"/pipelines/runs/{run_id}/",
    )


def schedule(program_name, interval, runs=[{}]):
    pipeline_id = get_pipeline(program_name)["id"]
    return _api_call(
        httpx.post,
        f"/pipelines/schedules/",
        json={"pipeline": pipeline_id, "interval": interval, "variables_list": runs},
    )


def delete_schedule(program_name):
    pipeline_id = get_pipeline(program_name)["id"]
    return _api_call(
        httpx.delete,
        f"/pipelines/{pipeline_id}/schedules/",
    )


def send_assistant_message(message, thread_id=None):
    return _api_call(
        httpx.post, "/transformers/send-assistant-message/", json={"message": message, "thread_id": thread_id}
    )


def send_assistant_function_outputs(outputs, thread_id, run_id):
    return _api_call(
        httpx.post,
        "/transformers/send-assistant-function-outputs/",
        json={"outputs": outputs, "thread_id": thread_id, "run_id": run_id},
    )


def poll_extract(url, page_type):
    return _api_call(httpx.post, "/extract/", json={"url": url, "page_type": page_type})
