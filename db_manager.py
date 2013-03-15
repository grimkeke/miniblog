from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import imp, os, os.path
from sys import argv

def db_create():
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, \
                            api.version(SQLALCHEMY_MIGRATE_REPO))

def db_migrate():
    migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % \
            (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, \
            SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)

    open(migration, "wt").write(script)
    a = api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def db_upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def db_downgrade():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def start_mailserver():
    os.system('python -m smtpd -n -c DebuggingServer localhost:25')

def print_usage(name):
    print '''Usage: python %s [-cmud]''' % name

def main():
    if len(argv) != 2:
        print_usage(argv[0])
        exit()

    cmd = argv[1]
    if cmd in ['-c', '--create']:
        db_create()
    elif cmd in ['-m', '--migrate']:
        db_migrate()
    elif cmd in ['-u', '--upgrade']:
        db_upgrade()
    elif cmd in ['-d', '--downgrade']:
        db_downgrade()
    elif cmd in ['-M', '--mail']:
        start_mailserver()
    else:
        print_usage()

if __name__ == '__main__':
    main()
