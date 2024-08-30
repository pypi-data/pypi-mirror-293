import dataclasses
import logging
import pathlib
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Reads a file and returns its contents as string."""
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        path: pathlib.Path | str

    @dataclasses.dataclass
    class Outputs:
        data: str

    def execute(self, inputs):
        if not self.config.path.exists():
            raise ValueError(f"File not found: {self.config.path}")

        data = pathlib.Path(self.config.path).read_text()
        logger.info(f"Read str from {self.config.path}")
        return self.Outputs(data)

    def dry_run(self, inputs):
        return self.execute(inputs)
