import json
from abc import ABC, abstractmethod
from json import JSONEncoder
import subprocess

from typing import Dict, Any

NADA_TESTS_COLLECTED = []


class NadaTestCase:
    def __init__(self, fn, program, test_name):
        self.fn = fn
        self.program = program
        self.test_name = test_name
        self.file = fn.__module__

    def run(self):
        return self.fn()

    def name(self):
        return f"{self.file}:{self.test_name}"


class NadaTestJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.to_json()


def nada_test(program: str):
    if not program or not isinstance(program, str):
        raise Exception("Program must be provided to @nada_test(program='...')")

    def decorator(fn_or_class):
        # if it is a class, instantiate it
        if isinstance(fn_or_class, type):
            if not issubclass(fn_or_class, NadaTest):
                raise Exception(f"Class {fn_or_class.__name__} must be a subclass of NadaTest")
            name = fn_or_class.__name__
            fn = fn_or_class()
        else:
            fn = fn_or_class
            name = fn.__name__
        NADA_TESTS_COLLECTED.append(NadaTestCase(fn, program, name))
        return fn

    return decorator


def nada_run(program: str, inputs: [Dict[str, Any]], debug, json_encoder=NadaTestJSONEncoder) -> Dict[str, Any]:
    """
    Run a Nada program with the given inputs and return the outputs.
    :param program: program name
    :param inputs: inputs to the program
    :param debug: if True, run the program in debug mode
    :param json_encoder: encoder for serializing the inputs to json
    :return: the outputs of the program as a dictionary
    """
    inputs_json = json.dumps(inputs, cls=json_encoder)
    command = ["nada", "run-json", program]
    if debug:
        command.append("--debug")
    output = subprocess.run(
        command,
        input=inputs_json,
        capture_output=True,
        text=True,
        check=True
    )
    output = json.loads(output.stdout)
    return output


class NadaTest(ABC):
    """
    Base class for Nada tests. Subclass this class and implement the `inputs` and `check_outputs` methods.
    """

    @abstractmethod
    def inputs(self):
        raise NotImplementedError

    @abstractmethod
    def check(self, outputs):
        raise NotImplementedError

    def __call__(self):
        outs = yield self.inputs()
        self.check(outs)
