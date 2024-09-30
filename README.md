# Database Backup CLI

A CLI tool to automate database backups. Currently, it supports **PostgreSQL** as the only source and **S3** as the target storage, but it's designed to be extensible to support multiple databases and destinations in future versions.

The tool uses **Typer** to handle commands, **subprocesses** and **child processes** to execute the database operations. It also includes a scheduling mechanism based on YAML configuration files.

## Features

- **Automated backups** based on a provided schedule.
- Support for **PostgreSQL** as the source database.
- Backups stored in **AWS S3** as the destination.
- Configurable notification system (to be implemented).
- Extensible design for supporting multiple database types and destinations.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OrionWambert/pysinker.git
   cd pysinker
Install the required dependencies:
```pip install -r requirements.txt ```

Ensure you have access to a PostgreSQL database and AWS S3 bucket for storage.

### Usage

1. dump Command
The dump command triggers a backup process for the specified database according to the provided YAML configuration.

Example usage:

```python pysinker.py dump --config /path/to/your/config.yaml```

YAML Configuration Structure
Here’s an example of a YAML configuration file (config.yaml) for a PostgreSQL database:
```
source:
  - name: "MyPostgresDB"
    type: "postgres"
    host: "localhost"
    port: 5432
    user: "admin"
    password: "secret"
    database: "my_database"
    job:
      schedule_type: "interval"
      interval: 30
      year: "2024"
      month: "1-6"
      day: "1,15"
      week: "10-20"
      day_of_week: "mon-fri"
      hour: "1"
      minute: "0"
      second: "30"
    file:
      format: "tar"
      extension: "tar"
      path: "/path/to/store/backup"
      name: "my_backup"
target:
  s3:
    bucket_name: "s3_remote_backups"
    aws_access_key_id: "YOUR_AWS_ACCESS_KEY"
    aws_secret_access_key: "YOUR_AWS_SECRET_KEY"
    aws_region: "us-west-1"
action:
  notification:
    email:
      to: example@example.com,test@example.com,another@example.com
      from: sender@example.com
      smtp_server: smtp.example.com
      smtp_port: 587
      username: smtp_username
      password: smtp_password
```
2. stop Command
The stop command halts any ongoing backup processes. This command can be used to safely stop the CLI if needed.

#### Example usage:

```python your_module.py stop```

## Roadmap
This project is still in early development. The following features are planned for future versions:

- Multiple database support (e.g., MySQL, MongoDB, SQLite)
- More backup destinations (e.g., local filesystem, FTP, Google Drive).
- Advanced notification options (e.g., Slack, Discord, SMS).
- Custom actions for backups, like notifying social media or synchronizing with other services.

### Contribution

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request with your changes.

```
Fork the project.
Create your feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

```
### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Contact
If you have any questions or issues, feel free to reach out to the project maintainer at wambertorion@gmail.com.

cc: https://roadmap.sh/projects/database-backup-utility
