#!/usr/bin/env sh

STATUS=0

echo "postgresql-backup-restore: backup: Started"

echo "postgresql-backup-restore: Backing up ${DB_NAME}"

start=$(date +%s)
$(PGPASSWORD=${DB_USERPASSWORD} pg_dump --host=${DB_HOST} --username=${DB_USER} --create --clean ${DB_OPTIONS} --dbname=${DB_NAME} > /tmp/${DB_NAME}.sql) || STATUS=$?
end=$(date +%s)

if [ $STATUS -ne 0 ]; then
    echo "postgresql-backup-restore: FATAL: Backup of ${DB_NAME} returned non-zero status ($STATUS) in $(expr ${end} - ${start}) seconds."
    exit $STATUS
else
    echo "postgresql-backup-restore: Backup of ${DB_NAME} completed in $(expr ${end} - ${start}) seconds, ($(stat -c %s /tmp/${DB_NAME}.sql) bytes)."
fi

echo "postgresql-backup-restore: backup: Completed"