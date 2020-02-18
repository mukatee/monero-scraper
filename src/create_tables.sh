export DB_HOST=
export DB_USER_PW=
export DB_NAME=
export DB_USER=

cd python/db
python create_tables.py &

unset DB_HOST
unset DB_USER_PW
unset DB_NAME
unset DB_USER
