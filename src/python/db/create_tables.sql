    CREATE TABLE transactions (
        tx_id BIGINT UNSIGNED NOT NULL UNIQUE,
        version TINYINT UNSIGNED NOT NULL,
        hash BIGINT NOT NULL,
        fee BIGINT,
        height BIGINT,
        unlocktime DATETIME,
        PRIMARY KEY (tx_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE txins (
        txin_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage BIGINT NOT NULL,
        PRIMARY KEY (txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE tx_txins (
        tx_id BIGINT UNSIGNED NOT NULL,
        txin_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (tx_id, txin_id),
        CONSTRAINT fk_tx_txins_txid
          FOREIGN KEY (tx_id)
          REFERENCES transactions (tx_id),
        CONSTRAINT fk_tx_txins_txin_id
          FOREIGN KEY (txin_id)
          REFERENCES txins (txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE txouts (
        txout_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage BIGINT NOT NULL,
        PRIMARY KEY (txout_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE tx_txouts (
        tx_id BIGINT UNSIGNED,
        txout_id BIGINT UNSIGNED,
        PRIMARY KEY (tx_id, txout_id),
        CONSTRAINT fk_txouts_txid
          FOREIGN KEY (tx_id)
          REFERENCES transactions (tx_id),
        CONSTRAINT fk_txouts_txoutid
          FOREIGN KEY (txout_id)
          REFERENCES txouts (txout_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE key_offsets (
        txin_id BIGINT UNSIGNED,
        offset BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (txin_id, offset),
        CONSTRAINT fk_keyoffsets_txin_id
          FOREIGN KEY (txin_id)
          REFERENCES txins (txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE output_details (
        txin_id BIGINT UNSIGNED,
        height BIGINT UNSIGNED NOT NULL,
        key_hex BIGINT NOT NULL,
        mask_hex BIGINT NOT NULL,
        unlocked BOOLEAN NOT NULL,
        PRIMARY KEY (txin_id, height, key_hex),
        CONSTRAINT fk_output_details_txin_id
          FOREIGN KEY (txin_id)
          REFERENCES txins (txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


