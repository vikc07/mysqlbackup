import os
import shutil
from gpm import os as gpmos
from mysqlbackup import mysqlbackup

cfg_file_path = mysqlbackup.cfg._file_path
cfg_file_path_backup = cfg_file_path + "_backup"

def backup_config():
    if os.path.exists(cfg_file_path):
        shutil.move(cfg_file_path, cfg_file_path_backup)


def restore_config():
    if os.path.exists(cfg_file_path_backup):
        shutil.move(cfg_file_path_backup, cfg_file_path)


def use_config(cfg_num):
    restore_config()
    backup_config()
    cfg_file_path_new = os.path.join(os.path.dirname(__file__), 'test_config_{}.json'.format(str(cfg_num)))
    shutil.copy(cfg_file_path_new, cfg_file_path)


def remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def test_backup_all():
    use_config(1)
    mysqlbackup.cfg.read()
    mysqlbackup.cfg.BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
    restore_config()
    assert mysqlbackup.do() == 0
    remove_folder(mysqlbackup.cfg.BACKUP_DIR)


def test_backup_two():
    use_config(2)
    mysqlbackup.cfg.read()
    mysqlbackup.cfg.BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
    restore_config()
    value = mysqlbackup.do()
    assert (value == 0) and (len(gpmos.ls(mysqlbackup.cfg.BACKUP_DIR)) == 2)
    remove_folder(mysqlbackup.cfg.BACKUP_DIR)


def test_invalid_credentials():
    use_config(3)
    mysqlbackup.cfg.read()
    mysqlbackup.cfg.BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
    restore_config()
    assert mysqlbackup.do() > 0
