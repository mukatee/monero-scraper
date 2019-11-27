TABLES = {}

TABLES['transactions'] = """
    CREATE TABLE transactions (
        tx_id BIGINT UNSIGNED NOT NULL,
        version TINYINT UNSIGNED NOT NULL,
        hash CHAR(32) NOT NULL,
        fee BIGINT,
        height BIGINT,
        unlocktime DATETIME,
        PRIMARY KEY (hash)
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
TABLES['txins'] = """
    CREATE TABLE txins (
        txin_id BIGINT NOT NULL AUTO_INCREMENT,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage CHAR(32) NOT NULL,
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
        key_hex CHAR(32) NOT NULL,
        mask_hex CHAR(32) NOT NULL,
        unlocked BOOLEAN NOT NULL,
        PRIMARY KEY (hash)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

TABLES['txouts'] = """
    CREATE TABLE txins (
        txout_id BIGINT NOT NULL AUTO_INCREMENT,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage CHAR(32) NOT NULL,
        PRIMARY KEY (txout_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""
