#!/usr/bin/env sh

STATUS=0
PBR="postgresql-backup-restore"
echo "${PBR}: restore: Started"

# Create database
create_db(){
    echo "${PBR}: creating DB ${DB_NAME}"
    result = $(psql --host=${DB_HOST} --username=${POSTGRES_USER} --command="CREATE DATABASE ${DB_NAME};")
    #if [ "${result}" != "CREATE DATABASE" ]; then
    #    message="Create database command failed: ${result}"
    #    echo "${PBR}: FATAL: ${message}"
    #    exit 1
    #fi
}

# Create database user
create_role(){
    echo "${PBR}: creating role ${POSTGRES_USER}"
    result=$(psql --host=${DB_HOST} --username=${POSTGRES_USER} --command="create role ${POSTGRES_USER} with login password '${POSTGRES_PASSWORD}' inherit;")
    if [ "${result}" != "CREATE ROLE" ]; then
        message="Create role command failed: ${result}"
        echo "${PBR}: FATAL: ${message}"
        exit 1
    fi
}

# Ensure the database user exists.
check_role(){
    echo "${PBR}: checking for DB user ${POSTGRES_USER}"
    result=$(psql --host=${DB_HOST} --username=${POSTGRES_USER} --command='\du' | grep ${POSTGRES_USER})
    if [ -z "${result}" ]; then
        create_role
    fi
}

# Ensure the database exists
check_db(){
    echo "${PBR}: checking for DB ${DB_NAME}"
    result=$(psql --host=${DB_HOST} --username ${POSTGRES_USER} --command='\l' | grep ${DB_NAME})
    if [ -z "${result}" ]; then
        message="Database "${DB_NAME}" on host "${DB_HOST}" does not exist."
        echo "${PBR}: LOG: ${message}"
        create_db
    else 
        echo "${PBR}: deleting database "
        result=$(psql --host=${DB_HOST} --dbname=${DB_NAME} --username=${POSTGRES_USER} --command="DROP DATABASE ${DB_NAME};")
        if [ "${result}" != "DROP DATABASE" ]; then
            message="Delete database command failed: ${result}"
            echo "${PBR}: FATAL: ${message}"
            exit 1
        fi
        create_db
    fi
}

# Restore database from file
restore_db(){
    echo "${PBR}: restoring ${DB_NAME}"
    start=$(date +%s)
    psql --host=${DB_HOST} --username=${POSTGRES_USER} -f /tmp/${DB_NAME}.sql || STATUS=$?
    end=$(date +%s)

    if [ $STATUS -ne 0 ]; then
        echo "${PBR}: FATAL: Restore of ${DB_NAME} returned non-zero status ($STATUS) in $(expr ${end} - ${start}) seconds."
        exit $STATUS
    else
        echo "${PBR}: Restore of ${DB_NAME} completed in $(expr ${end} - ${start}) seconds."
    fi

    echo "${PBR}: restore: Completed"
    exit $STATUS
}

# Execute
check_db
check_role
restore_db