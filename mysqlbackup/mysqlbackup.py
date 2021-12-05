import os
import gzip
from gpm import config, logging, formatting
from gpm import os as gpmos

cfg = config.Config(script=__file__, create=True)
cfg.read()

log = logging.Log(script=__file__, log_level=cfg.LOG_LEVEL, log_entry_format_separator=cfg.LOG_ENTRY_SEPARATOR,
                  tsformat='YYYYMMDD')


def do():
    errcode = 0

    # Check backup dir, if it does not exist, create it
    if not os.path.exists(cfg.BACKUP_DIR):
        os.mkdir(cfg.BACKUP_DIR)

    # Configure commands
    mysqlcliauth = "--host={host} --port={port} --user={user} --password={passw}"
    mysqlclidocker = "docker run --network=host -i {image}"

    mysqlcliauth = mysqlcliauth.format(
        host=cfg.MYSQL['HOST'],
        port=cfg.MYSQL['PORT'],
        user=cfg.MYSQL['USER'],
        passw=cfg.MYSQL['PASSW'],
    )

    mysqlclicmd = "{program} {options} " + mysqlcliauth

    mysqldump = mysqlclicmd.format(program="mysqldump", options="--single-transaction --quick --lock-tables=false")
    mysql = mysqlclicmd.format(program="mysql", options="--silent --skip-column-names")

    if cfg.MYSQLCLI_USE_DOCKER:
        log.debug('using docker')
        mysqlclidocker = mysqlclidocker.format(image=cfg.MYSQLCLI_DOCKER_IMAGE)
        mysqldump = mysqlclidocker + " " + mysqldump
        mysql = mysqlclidocker + " " + mysql

    log.debug('mysqlcliauth: {}'.format(mysqlcliauth))
    log.debug('mysqldump: {}'.format(mysqldump))
    log.debug('mysql: {}'.format(mysql))

    # Get a list of databases
    log.info('getting a list of databases')

    cmd = mysql + " --execute='show databases'"
    log.debug("cmd: {}".format(cmd))
    out = gpmos.run(cmd)

    log.debug('returncode: {}'.format(out['returncode']))

    # Was the execution successful?
    if out['returncode'] > 0:
        errcode = 1
        log.error('error getting list of databases')
        log.error('stderr: {}'.format(out['stderr']))
        return errcode

    log.debug('stdout: {}'.format(out['stdout']))
    databases = out['stdout'].splitlines()
    log.info('found {} databases'.format(len(databases)))
    log.info(databases)

    if len(databases) > 0:
        for database in databases:
            if database not in cfg.EXCLUDE and (database in cfg.INCLUDE or cfg.INCLUDE[0] == '*'):
                ts = formatting.time_now(cfg.BACKUP_FILE_TSFORMAT)
                backup_file = os.path.join(cfg.BACKUP_DIR, database + "_" + ts + ".sql.gz")
                log.debug("backup file name {}".format(backup_file))
                cmd = mysqldump + " --databases " + database
                log.debug("cmd: {}".format(cmd))
                out = gpmos.run(cmd)

                if out['returncode'] > 1:
                    log.error('error backing up database {}'.format(database))
                    log.error('stderr: {}'.format(out['stderr']))
                    return errcode

                log.debug('writing to backup file {}'.format(backup_file))
                with gzip.open(backup_file, "wb") as f:
                    f.write(out['stdout'].encode('utf-8'))

                log.info('successfully backed up database {} to {}'.format(database, backup_file))
            else:
                log.info('excluding {}'.format(database))

    else:
        log.error('no databases found')
        errcode = 1


    return errcode


if __name__ == "__main__":
    log.start()
    errcode = do()
    log.end()
    exit(errcode)

