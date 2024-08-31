from typing import Optional
import requests
from prettytable import PrettyTable

from e2enetworks.cloud.tir.finetuning.constants import (
    HUGGING_FACE, EOS_BUCKET, TEXT_MODELS_LIST,
    CLIENT_NOT_READY_MESSAGE, PIPELINE,
    ALLOWED_DATATYPES_ERROR, INVALID_DATASET,
    PLAN_NAME_ERROR, DEFAULT_TEXT_TRAINING_ARGS,
    DEFAULT_IMAGE_TRAINING_ARGS, IMAGE_MODELS_LIST,
    INVALID_MODEL_NAME, DATASET_TYPES_LIST,
    )
from e2enetworks.cloud.tir.helpers import get_argument_from_kwargs
from e2enetworks.cloud.tir.skus import Plans, client
from e2enetworks.cloud.tir.utils import prepare_object


class FinetuningClient:
    def __init__(self, project: Optional[str] = None):
        if not client.Default.ready():
            raise ValueError(CLIENT_NOT_READY_MESSAGE)
        if project:
            client.Default.set_project(project)

    def create_finetuning(
        self,
        name,
        model_name,
        plan_name,
        huggingface_integration_id,
        wandb_integration_id=None,
        wandb_integration_run_name="",
        description=None,
        training_type="Peft",
        **kwargs
    ):
        if not isinstance(plan_name, str):
            return ValueError(PLAN_NAME_ERROR)

        if model_name in TEXT_MODELS_LIST:
            training_inputs = self._get_text_model_inputs(**kwargs)
        elif model_name in IMAGE_MODELS_LIST:
            training_inputs = self._get_image_model_inputs(**kwargs)
        else:
            raise Exception(INVALID_MODEL_NAME)

        payload = {
            "name": name,
            "model_name": model_name,
            "huggingface_integration_id": huggingface_integration_id,
            "sku_item_price_id": self._get_sku_item_price_from_plan_name(plan_name),
            "training_inputs": training_inputs,
            "training_type": training_type,
            "wandb_integration_id": wandb_integration_id if wandb_integration_id else None,
            "wandb_integration_run_name": wandb_integration_run_name,
            "description": description,
        }
        url = f"{client.Default.gpu_projects_path()}/finetuning/?"
        req = requests.Request('POST', url, json=payload)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def _get_text_model_inputs(self, **kwargs):
        return {
            **self._get_dataset_config(**kwargs),
            **{key: get_argument_from_kwargs(key, kwargs, type_, default, is_required)
                for key, (type_, default, is_required) in DEFAULT_TEXT_TRAINING_ARGS.items()}
        }

    def _get_image_model_inputs(self, **kwargs):
        return {
            **self._get_dataset_config(**kwargs),
            **{key: get_argument_from_kwargs(key, kwargs, type_, default, is_required)
                for key, (type_, default, is_required) in DEFAULT_IMAGE_TRAINING_ARGS.items()}
        }

    def _get_dataset_config(self, **kwargs):
        dataset_type = kwargs.get("dataset_type")
        dataset_info = kwargs.get("dataset")

        if dataset_type not in DATASET_TYPES_LIST:
            raise Exception(ALLOWED_DATATYPES_ERROR)

        if dataset_type == HUGGING_FACE:
            return {"dataset_type": HUGGING_FACE,
                    "dataset": dataset_info}

        dataset_sub_str = dataset_info.split('/')
        if len(dataset_sub_str) <= 1:
            raise Exception(INVALID_DATASET)
        object_name = dataset_info.replace(f"{dataset_sub_str[0]}/", '', 1)
        if not object_name:
            raise Exception("dataset invalid")
        return {"dataset_type": dataset_type,
                "dataset": f'{dataset_sub_str[0]}/{object_name}'}

    def list_finetunings(self):
        url = f"{client.Default.gpu_projects_path()}/finetuning/?"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list_supported_models(self):
        url = f"{client.Default.gpu_projects_path()}/finetuning/model_types/?"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def show_plan_names(self):
        plans = Plans()
        plans_list = plans.list(PIPELINE)
        gpu_skus = plans_list["GPU"]
        plans_table = PrettyTable()
        plans_table.field_names = ['name', 'series', 'cpu', 'gpu', 'memory',
                                   'sku_item_price_id', 'sku_type', 'committed_days', 'unit_price']
        plans.insert_plans_in_table(gpu_skus, plans_table)
        print(plans_table)

    def _get_sku_item_price_from_plan_name(self, plan_name, committed_days=0):
        plans = Plans().list(PIPELINE)
        plan_name_to_sku = {}
        gpu_skus = plans["GPU"]
        for sku in gpu_skus:
            for sku_item_price in sku["plans"]:
                if not sku["is_free"]:
                    name = sku.get('name')
                    committed_days = sku_item_price.get('committed_days')
                    key = f'{name}_c{committed_days}'
                    plan_name_to_sku[key] = sku_item_price['sku_item_price_id']
        if plan_name_to_sku.get(f'{plan_name}_c{committed_days}'):
            return plan_name_to_sku.get(f'{plan_name}_c{committed_days}')
        raise Exception(f'Plan_name invalid : {plan_name}')

    def get_finetuning(self,
                       finetuning_id: str | int
                       ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete_finetuning(self,
                          finetuning_id: str | int
                          ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def stop_finetuning(self,
                        finetuning_id: str | int
                        ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?&action=terminate&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def retry_finetuning(self,
                         finetuning_id: str | int
                         ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?&action=retry&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def show_text_model_training_inputs(self):
        """
        Prints the training inputs for text models with their default values.
        """
        print("Text Model Training Inputs:")
        for key, (type_, default, _) in DEFAULT_TEXT_TRAINING_ARGS.items():
            print(f"- {key}: {type_.__name__} (default: {default})")

    def show_image_model_training_inputs(self):
        """
        Prints the training inputs for image models with their default values.
        """
        print("Image Model Training Inputs:")
        for key, (type_, default, _) in DEFAULT_IMAGE_TRAINING_ARGS.items():
            print(f"- {key}: {type_.__name__} (default: {default})")

    @staticmethod
    def help():
        help_text = """
        FinetuningClient Class Help:

        This class provides methods for interacting with finetuning-related operations.
        Before using these methods, make sure to initialize the client using:
        - Using e2enetworks.cloud.tir.init(...)

        Available Methods:
        1. create_finetuning(
            self,
            name,
            model_name,
            plan_name,
            huggingface_integration_id,
            wandb_integration_id=None,
            wandb_integration_run_name="",
            description="",
            training_type="Peft",
            **kwargs
        )
            - Create a new finetuning.
            Note: Training inputs should be passed in **kwargs as a dictionary.

        2. list_finetunings()
            - List existing finetunings.

        3. get_finetuning(finetuning_id)
            - Get details of a specific finetuning.

        4. delete_finetuning(finetuning_id)
            - Delete a specific finetuning.

        5. stop_finetuning(finetuning_id)
            - Stop a specific finetuning.

        6. retry_finetuning(finetuning_id)
            - Retry a failed/terminated finetuning.

        7. show_plan_names()
            - List currently supported SKUs for finetuning.

        8. list_supported_models()
            - List currently supported models for finetuning.

        9. show_text_model_training_inputs()
            - Print text model training inputs and defaults.

        10. show_image_model_training_inputs()
            - Print image model training inputs and defaults.

        Note: Certain methods require specific arguments. Refer to the method signatures for details.
        """
        print(help_text)
