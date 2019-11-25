TABLES = {}

TABLES['transactions'] = """
    CREATE TABLE transactions (
      version TINYINT UNSIGNED NOT NULL,
      hash char(32) NOT NULL,
      fee BIGINT,
      height BIGINT,
      unlocktime DATETIME,
      PRIMARY KEY (hash)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

--TODO: is autoincrement ok or now? or need to track transactions otherwise?
TABLES['txins'] = """
    CREATE TABLE txins (
      txin_id BIGINT NOT NULL AUTO_INCREMENT,
      amount BIGINT UNSIGNED NOT NULL,
      keyimage char(32) NOT NULL,
      PRIMARY KEY (hash)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

TABLES['key_offsets'] = """
    CREATE TABLE key_offsets (
      txin_id BIGINT,
      offset BIGINT UNSIGNED NOT NULL,
      PRIMARY KEY (hash)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""
