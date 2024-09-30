import logging
import os
import signal
import sys
from enum import StrEnum
import daemon
from apscheduler.schedulers.blocking import BlockingScheduler

PID_FILE = "pysinker.pid"


class ScheduleType(StrEnum):
    INTERVAL = "interval",
    CRON = "cron",


class ScheduleConfig:
    def __init__(self, interval: int, year: str = None,
                 month: str = None, day: str = None,
                 week: str = None,
                 day_of_week: str = None,
                 hour: str = "1",
                 minute: str = "0",
                 second: str = None,
                 schedule_type: ScheduleType = ScheduleType.CRON
                 ):
        self.schedule_type = schedule_type
        self.interval = interval
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second


def schedule(job, schedule_config: ScheduleConfig) -> BlockingScheduler:
    scheduler = BlockingScheduler()
    if schedule_config.schedule_type == ScheduleType.INTERVAL:
        scheduler.add_job(job, ScheduleType.INTERVAL, seconds=schedule_config.interval, max_instances=3)
    elif schedule_config.schedule_type == ScheduleType.CRON:
        scheduler.add_job(
            job,
            ScheduleType.CRON,
            year=schedule_config.year,
            month=schedule_config.month,
            day=schedule_config.day,
            week=schedule_config.week,
            day_of_week=schedule_config.day_of_week,
            hour=schedule_config.hour,
            minute=schedule_config.minute,
            second=schedule_config.second,
            max_instances=3
        )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit) as e:
        logging.info(f"Error when we trying to launch schedule {e}")
    return scheduler


def kill_job_from_pid_file(pid_file: str, next_pid: bool = False):
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        logging.info(f"Current pid {pid}")
        if next_pid:
            pid = pid + 2
        os.kill(pid, signal.SIGTERM)
        logging.info(f"Process {pid} terminated.")
        remove_file(pid_file)
    except FileNotFoundError:
        logging.error(f"Error: PID file '{pid_file}' not found.")
    except ValueError:
        logging.error("Error: PID file contains invalid data.")
    except OSError as e:
        if not next_pid:
            kill_job_from_pid_file(pid_file, next_pid=True)
        logging.error(f"Error: {e}")
    pass


def start_job_daemon(job):
    if os.path.exists(PID_FILE):
        logging.info("Daemon is already running. trying to remove file")
        kill_job_from_pid_file(PID_FILE)
        remove_file(PID_FILE)
    else:
        logging.info("Starting python daemon")
    pid = os.fork()
    if pid > 0:
        logging.info(f"Current pid {pid}")
        sys.exit(0)
    elif pid == 0:
        with open(PID_FILE, 'w') as f:
            process_id = str(os.getpid())
            logging.info(process_id, os.getgid(), os.getsid(int(process_id)))
            f.write(process_id)
        with daemon.DaemonContext():
            job()


def remove_file(file):
    try:
        logging.info(f"Remove python file {file}")
        os.remove(file)
    except FileNotFoundError:
        logging.error("Error: File not found.")
    except PermissionError:
        logging.error("Error: Permission denied.")
    except OSError:
        logging.error(f"Error: {file} not found.")
    except Exception as e:
        logging.error(f"Error: {e}")
