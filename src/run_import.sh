export DB_HOST=
export DB_USER_PW=
export DB_NAME=
export DB_USER=

cd python
python mytest.py >file.log 2>&1

unset DB_HOST
unset DB_USER_PW
unset DB_NAME
unset DB_USER


