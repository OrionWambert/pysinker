import logging
import os
import subprocess
from abc import ABC
from datetime import datetime
from pysinker.core.job_scheduler import schedule, ScheduleConfig, start_job_daemon
from pysinker.source.db_config import DbConfig
from pysinker.source.file_config import FileConfig
from pysinker.source.sinker_source import SinkerSource
from pysinker.target.s3_bucket import S3BucketConfig, upload_file_to_s3_bucket, upload_directory_to_s3_bucket


class PostgresSinkerSource(SinkerSource, ABC):
    def __init__(self, config: DbConfig):
        super().__init__(config)

    def dump_database(self, file_config: FileConfig, s3_config: S3BucketConfig):
        logging.info("Dumping database...")
        if self.check_db_dump_tool_installed():
            config = self.config
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            custom_path = file_config.path
            file_name = file_config.name
            file_full_name = f"{file_name}_{timestamp}.{file_config.extension}"
            file_path = os.path.join(custom_path, file_full_name)
            cmd = ["pg_dump", f"--format={file_config.format}", "-v", f"--host={config.host}", f"--port={config.port}",
                   f"--username={config.user}", f"--dbname={config.database}", "-f", f"{file_path}"]
            env = dict(os.environ)

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=False)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                logging.info(f"Error during dump: {stderr.decode()}")
                return False
            else:
                logging.info(f"Database dump completed successfully: {stdout.decode()}")
                if s3_config is not None:
                    if file_config.format == "directory":
                        upload_directory_to_s3_bucket(bucket_name=s3_config.bucket_name,
                                                      aws_access_key_id=s3_config.aws_access_key_id,
                                                      aws_secret_access_key=s3_config.aws_secret_access_key,
                                                      s3_directory=file_name, local_directory=file_path, )
                        pass
                    else:
                        upload_file_to_s3_bucket(file_path=file_path, bucket_name=s3_config.bucket_name,
                                                 object_name=file_full_name,
                                                 aws_access_key_id=s3_config.aws_access_key_id,
                                                 aws_secret_access_key=s3_config.aws_secret_access_key, )
                return True

        else:
            return "pg-dump tool not installed"


def check_db_dump_tool_installed(self) -> bool:
    try:
        result = subprocess.run(["pg_dump", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        logging.info(f"Error checking pg-dump tool: {e}")
        return False


def check_db_dump_tool_version(self) -> str:
    if self.check_db_dump_tool_installed():
        result = subprocess.run(["pg_dump", "--version"], capture_output=True, text=True)
        return result.stdout
    else:
        return "pg-dump tool not installed"


def check_pg_connection(self) -> bool:
    if self.check_db_connection():
        pass
    return True


def dump_postgres_all_data(config: DbConfig, file_config: FileConfig, s3_config: S3BucketConfig,
                           schedule_config: ScheduleConfig):
    sinker = PostgresSinkerSource(config)
    scheduler = lambda: schedule(lambda: sinker.dump_database(file_config, s3_config), schedule_config)
    start_job_daemon(scheduler)
