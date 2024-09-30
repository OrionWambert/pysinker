from multiprocessing import freeze_support
import typer
from typer import Typer
from typing_extensions import Annotated
from pysinker.core.job_scheduler import PID_FILE, kill_job_from_pid_file, ScheduleConfig
from pysinker.core.yaml_parser import parse_yaml_file
from pysinker.source.db_config import DbConfig
from pysinker.source.file_config import FileConfig
from pysinker.source.postgres_source import dump_postgres_all_data
from pysinker.target.s3_bucket import S3BucketConfig
app = Typer()

@app.command(name="dump")
def dump(config: Annotated[str, typer.Option(help="The path to the config file")] = "config.yaml"):
    config_value = parse_yaml_file(config)
    sources = config_value.get("source", [])
    target = config_value.get("target")
    for source in sources:
        source_type = source["type"]
        source_job = source["job"]
        schedule_type = source_job["schedule_type"]
        interval = source_job["interval"]
        year = source_job["year"]
        month = source_job["month"]
        day = source_job["day"]
        week = source_job["week"]
        day_of_week = source_job["day_of_week"]
        hour = source_job["hour"]
        minute = source_job["minute"]
        second = source_job["second"]

        schedule_config = ScheduleConfig(schedule_type=schedule_type, interval=interval,
                                         year=year, month=month, day=day, week=week,
                                         hour=hour, minute=minute, second=second,
                                         day_of_week=day_of_week, )

        if source_type == "postgres" or source_type == "postgressql":
            config = DbConfig(source["host"], source["port"], source["user"], source["password"], source["database"])
            file_config_value = source["file"]
            file_config = FileConfig(name=file_config_value["name"], extension=file_config_value["extension"],
                                     path=file_config_value["path"], format=file_config_value["format"])

            if target["s3"] is not None:
                s3_config_value = target["s3"]
                s3_bucket_config = S3BucketConfig(bucket_name=s3_config_value["bucket_name"],
                                                  aws_access_key_id=s3_config_value["aws_access_key_id"],
                                                  aws_secret_access_key=s3_config_value["aws_secret_access_key"],
                                                  aws_region=s3_config_value["aws_region"])
                dump_postgres_all_data(config, file_config, s3_bucket_config, schedule_config)
            else:
                s3_bucket_config = None
                dump_postgres_all_data(config, file_config, s3_bucket_config, schedule_config)


@app.command(name="stop")
def stop():
    kill_job_from_pid_file(PID_FILE)


if __name__ == "__main__":
    freeze_support()
    app()
