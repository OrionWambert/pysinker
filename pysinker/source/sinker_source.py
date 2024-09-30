from abc import abstractmethod

from pysinker.source.db_config import DbConfig
from pysinker.source.file_config import FileConfig
from pysinker.target.s3_bucket import S3BucketConfig


class SinkerSource:
    def __init__(self, config: DbConfig):
        self.config = config

    @abstractmethod
    def check_db_dump_tool_installed(self) -> bool:
        pass

    @abstractmethod
    def check_db_connection(self) -> bool:
        pass

    @abstractmethod
    def dump_database(self, file_config: FileConfig, s3_config: S3BucketConfig):
        pass
