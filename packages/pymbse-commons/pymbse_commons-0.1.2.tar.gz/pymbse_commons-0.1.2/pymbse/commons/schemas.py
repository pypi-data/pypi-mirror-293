# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

from enum import Enum
from typing import Any, ClassVar, Dict, List

from pydantic import BaseModel, ConfigDict, SerializeAsAny, model_validator
from typing_extensions import Self


class ExecEnvironment(BaseModel):
    name: str
    version: str

    model_config = ConfigDict(from_attributes=True)

    subclass_registry: ClassVar[Dict[str, type]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        ExecEnvironment.subclass_registry[cls.__name__] = cls

    class Settings:
        is_root = True


class DockerEnvironment(ExecEnvironment):
    image: str


class PythonEnvironment(ExecEnvironment):
    requirements: str


class ResourceType(str, Enum):
    unknown = "unknown"
    file = "file"
    dictionary = "dictionary"

    @staticmethod
    def infer_type(suffix: str) -> "ResourceType":
        if suffix in [".yml", ".yaml", ".json"]:
            return ResourceType.dictionary
        else:
            return ResourceType.file


class Resource(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

    subclass_registry: ClassVar[Dict[str, type]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        Resource.subclass_registry[cls.__name__] = cls

    class Settings:
        is_root = True


class ArtefactResource(Resource):
    resource_type: ResourceType
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class ArtefactResourceRef(Resource):
    ref_system: str
    ref_model: str
    ref_name: str

    ref_file_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ModelReference(BaseModel):
    """Reference to a model."""

    system: str
    model: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ModelExecutionReference(ModelReference):
    """Reference to a model execution."""

    execution: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class Model(BaseModel):
    name: str
    system: str
    env: SerializeAsAny[ExecEnvironment]
    inputs: List[SerializeAsAny[Resource]] = []
    outputs: List[ArtefactResource] = []

    model_config = ConfigDict(from_attributes=True)

    def get_reference(self) -> ModelReference:
        return ModelReference(system=self.system, model=self.name)

    def get_alternative_filenames(self) -> dict[str, str]:
        alt_fn = {}

        for inp in self.inputs:
            if isinstance(inp, ArtefactResourceRef) and inp.ref_file_name:
                alt_fn[inp.name] = inp.ref_file_name

        return alt_fn

    @model_validator(mode="after")
    def check_references_unique(self) -> Self:
        inp_names = {ref.name for ref in self.inputs}
        if len(inp_names) != len(self.inputs):
            raise ValueError("Input names must be unique")
        outp_names = {outp.name for outp in self.outputs}
        if len(outp_names) != len(self.outputs):
            raise ValueError("Output names must be unique")
        return self

    def __init__(self, **kwargs):
        if "inputs" in kwargs:
            for index in range(len(kwargs["inputs"])):
                current_input = kwargs["inputs"][index]
                if isinstance(current_input, dict):
                    input_keys = sorted(current_input.keys())
                    for _, subclass in Resource.subclass_registry.items():
                        registry_keys = sorted(subclass.model_fields.keys())
                        if input_keys == registry_keys:
                            current_input = subclass(**current_input)
                            break
                    kwargs["inputs"][index] = current_input
        if "env" in kwargs:
            if isinstance(kwargs["env"], dict):
                env_keys = sorted(kwargs["env"].keys())
                for _, subclass in ExecEnvironment.subclass_registry.items():
                    registry_keys = sorted(subclass.model_fields.keys())
                    if env_keys == registry_keys:
                        kwargs["env"] = subclass(**kwargs["env"])
                        break
        super().__init__(**kwargs)


class ModelExecution(BaseModel):
    model: Model
    exec_id: str
    execution_hash: str

    inputs: List[str]
    outputs: List[str]

    model_config = ConfigDict(from_attributes=True)

    def get_reference(self) -> ModelExecutionReference:
        return ModelExecutionReference(
            system=self.model.system, model=self.model.name, execution=self.exec_id
        )


class System(BaseModel):
    name: str
    models: List[Model] = []


class ModelSource(BaseModel):
    """Reference to a model source. Used in roxie-exec api."""

    name: str
    uri: str


class ExecutionSource(BaseModel):
    """Reference to an execution source. Used in roxie-exec api."""

    name: str
    uri: str


class ExecutionJob(BaseModel):
    """Reference to a running job. Used in roxie-exec api."""

    id: str
    status: str
