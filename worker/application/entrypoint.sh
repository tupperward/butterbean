#!/usr/bin/env sh

# hostname:port:database:username:password
echo ${DB_HOST}:*:*:${POSTGRES_USER}:${POSTGRES_PASSWORD}      > /root/.pgpass
chmod 600 /root/.pgpass

STATUS=0

case "${MODE}" in
    backup|restore)
        /data/${MODE}.sh || STATUS=$?
        ;;
    *)
        echo postgresql-backup-restore: FATAL: Unknown MODE: ${MODE}
        exit 1
esac

if [ $STATUS -ne 0 ]; then
    echo postgresql-backup-restore: Non-zero exit: $STATUS
fi

exit $STATUS