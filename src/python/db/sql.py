import os

TABLES = {}

DB_NAME = "xmr"
CREATE_DB_SQL = "CREATE DATABASE IF NOT EXISTS "+DB_NAME+" DEFAULT CHARACTER SET 'utf8'"
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PW = os.environ['DB_USER_PW']

TABLES['transactions'] = """
    CREATE TABLE transactions (
        tx_id BIGINT UNSIGNED NOT NULL,
        version TINYINT UNSIGNED NOT NULL,
        hash BIGINT NOT NULL,
        fee BIGINT,
        height BIGINT,
        unlocktime DATETIME,
        PRIMARY KEY (tx_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

#map tx_ins to transactions
TABLES['tx_txins'] = """
    CREATE TABLE tx_txins (
        tx_id BIGINT NOT NULL AUTO_INCREMENT,
        txin_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (tx_id, txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

#map tx_outs to transactions
TABLES['tx_txouts'] = """
    CREATE TABLE tx_txouts (
        tx_id BIGINT NOT NULL AUTO_INCREMENT,
        txout_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (tx_id, txout_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

#TODO: is autoincrement ok or not? or need to track transactions otherwise?
#TODO: check keyimages and other CHAR sizes
#https://monero.stackexchange.com/questions/2883/what-is-a-key-image
TABLES['txins'] = """
    CREATE TABLE txins (
        txin_id BIGINT NOT NULL AUTO_INCREMENT,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage BIGINT NOT NULL,
        PRIMARY KEY (txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

TABLES['key_offsets'] = """
    CREATE TABLE key_offsets (
        txin_id BIGINT,
        offset BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (txin_id, offset)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

TABLES['output_details'] = """
    CREATE TABLE output_details (
        txin_id BIGINT,
        height BIGINT UNSIGNED NOT NULL,
        key_hex BIGINT NOT NULL,
        mask_hex BIGINT NOT NULL,
        unlocked BOOLEAN NOT NULL,
        PRIMARY KEY (txin_id, height, key_hex)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

TABLES['txouts'] = """
    CREATE TABLE txouts (
        txout_id BIGINT NOT NULL AUTO_INCREMENT,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage BIGINT NOT NULL,
        PRIMARY KEY (txout_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

