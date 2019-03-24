[![CircleCI](https://circleci.com/gh/vikc07/mysqlbackup.svg?style=svg)](https://circleci.com/gh/vikc07/mysqlbackup)

# mysqlbackup
A simple mysql backup program

**Why use it?**

You will find the program useful over plain `mysqldump` in the following ways:
1) `mysqlbackup` can perform backup of all databases in one go or select few and provides you ability to "include" or
 "exclude" certain databases
2) `mysqlbackup` will create one backup file per database which is automatically `gzip` compressed and has timestamp 
in the name
3) `mysqlbackup` logs all the activity in the backend in plain text log files and provides an ability to adjust logging 
level which is extremely handy for audit and troubleshooting

Usually, one would create some sort of script on top of `mysqldump` to accomplish all of that. `mysqlbackup` takes 
the effort out by providing an out-of-the-box program that does all of this.

`mysqlbackup` uses `mysqldump` under the hood and so the backup files are created are compatible with `mysqldump`.

## Requirements ##
* Python 3 is needed
* [mysqlcli](https://dev.mysql.com/doc/refman/8.0/en/programs-client.html) either installed locally on 
the machine where this program will run or a docker container that
 has cli installed on that machine (such as [here](https://cloud.docker.com/repository/docker/vikramchauhan/mysqlcli))
 
## Installing ##

**Clone the repository**

    git clone https://github.com/vikc07/mysqlbackup.git


**Install dependencies**

    pip install -r mysqlbackup/requirements.txt


**Edit config file**

If using `mysqlci` on Docker

    cp mysqlbackup/mysqlbackup/cfg/sample_docker_mysqlbackup.json mysqlbackup/mysqlbackup/cfg/mysqlbackup.json

If using local `mysqlcli`

    cp mysqlbackup/mysqlbackup/cfg/sample_mysqlbackup.json mysqlbackup/mysqlbackup/cfg/mysqlbackup.json

Use your favorite text editor to edit the file

    nano mysqlbackup/mysqlbackup/cfg/mysqlbackup.json

Run `mysqlbackup`

    python mysqlbackup/mysqlbackup/mysqlbackup.py

Options explained

|Option|Description|
|------|-----------|
|LOG_LEVEL|Standard Python [Logging Levels](https://docs.python.org/3/library/logging.html)|
|LOG_ENTRY_SEPARATOR|Single space character ' ' by default|
|MYSQL HOST|MySQL host name|
|MYSQL PORT|MySQL host port|
|MYSQL USER|MySQL user|
|MYSQL PASSW|MySQL user password|
|MYSQLCLI_PATH|(not used currently) - leave default ""|
|MYSQLCLI_USE_DOCKER|Set to `true` if using `mysqlcli` on Docker otherwise set to `false`|
|MYSQLCLI_DOCKER_IMAGE|Docker image name|
|INCLUDE|List of databases to include. If the first entry is '*', all databases will be included|
|EXCLUDE|List of databases to exclude. This overrides '*' in the include above|
|BACKUP_DIR|Directory where backups should be stored|
|BACKUP_FILE_TSFORMAT|Timestamp format in the backup file name. Default YYYYMMDD. See below for other values|

**tsformat values**

Refer to the following chart to understand what you can use as `tsformat`. The keys represent the format to use and 
values represent the translation in Python

    "YYYYMMDDHHMISS": "%Y%m%d%H%M%S",
    "YYYYMMDDHHMI": "%Y%m%d%H%M",
    "YYYYMMDDHH": "%Y%m%d%H",
    "YYYYMMDD": "%Y%m%d",
    "YYYYMM": "%Y%m",
    "YYYY": "%Y",
    "hour_only": "%-I %p",
    "day_hour_only": "%A %-I %p",
    "day_only": "%A",
    "date_time_footer": "%b %d, %Y at %-I:%M:%S %p"
    
## Issues ##
This is an early stage product and there is going to be a ton of issues. Please report all issues here on github