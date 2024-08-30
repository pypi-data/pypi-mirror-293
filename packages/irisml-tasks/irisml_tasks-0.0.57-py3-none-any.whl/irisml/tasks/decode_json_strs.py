import dataclasses
import json
import logging
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Parse a list of json strings to dictionaries.

    If parsing fails, return dictionary {'failed_parse': raw_str}

    Inputs:
        json_strs (List[str]): JSON strings.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        json_strs: list[str]

    @dataclasses.dataclass
    class Outputs:
        dicts: list[dict]

    def execute(self, inputs):
        dicts = []
        for json_str in inputs.json_strs:
            try:
                dicts.append(json.loads(json_str))
            except Exception as e:
                logger.info(f"Could not decode JSON string: {e}")
                dicts.append({'failed_parse': json_str})
        return self.Outputs(dicts=dicts)

    def dry_run(self, inputs):
        return self.execute(inputs)
