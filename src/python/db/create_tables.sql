/*
 Ignoring some fields such as orphan status, assuming to not store forked chains.
 For the same reasons, assuming height works as a unique block id
 */

    CREATE TABLE blocks (
        height INT UNSIGNED NOT NULL UNIQUE,
        block_size SMALLINT UNSIGNED NOT NULL,
        weight SMALLINT UNSIGNED NOT NULL,
        difficulty BIGINT NOT NULL,
        cumulative_difficulty BIGINT NOT NULL,
        hash CHAR(64) NOT NULL,
        long_term_weight SMALLINT UNSIGNED NOT NULL,
        major_version TINYINT UNSIGNED NOT NULL,
        minor_version TINYINT UNSIGNED NOT NULL,
        nonce BIGINT UNSIGNED NOT NULL,
        reward BIGINT UNSIGNED NOT NULL,
        block_time BIGINT UNSIGNED NOT NULL,
        wide_cumulative_difficulty VARCHAR(20) NOT NULL,
        wide_difficulty VARCHAR(12) NOT NULL,
        PRIMARY KEY (height)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE transactions (
        tx_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        version TINYINT UNSIGNED NOT NULL,
        hash CHAR(64) NOT NULL,
        fee BIGINT UNSIGNED NOT NULL,
        height INT UNSIGNED NOT NULL,
        unlocktime INT UNSIGNED NOT NULL,
        PRIMARY KEY (tx_id),
        CONSTRAINT fk_tx_height
          FOREIGN KEY (height)
          REFERENCES blocks (height)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE txins (
        txin_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        tx_id BIGINT UNSIGNED NOT NULL,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage CHAR(64) NOT NULL,
        coinbase BOOLEAN NOT NULL,
        PRIMARY KEY (txin_id),
        CONSTRAINT fk_txins_txid
          FOREIGN KEY (tx_id)
          REFERENCES transactions (tx_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE txouts (
        tx_id BIGINT UNSIGNED NOT NULL,
        amount BIGINT UNSIGNED NOT NULL,
        target_key CHAR(64) NOT NULL,
        PRIMARY KEY (tx_id, target_key),
        CONSTRAINT fk_txouts_txid
          FOREIGN KEY (tx_id)
          REFERENCES transactions (tx_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE key_offsets (
        txin_id BIGINT UNSIGNED,
        offset BIGINT UNSIGNED NOT NULL,
/**        PRIMARY KEY (txin_id, offset), <- key offsets are in relation to each other, so duplicates can be there. https://monero.stackexchange.com/questions/2136/understanding-the-structure-of-a-monero-transaction*/
        CONSTRAINT fk_keyoffsets_txin_id
          FOREIGN KEY (txin_id)
          REFERENCES txins (txin_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE output_details (
        txin_id BIGINT UNSIGNED,
        height INT UNSIGNED NOT NULL,
        key_hex CHAR(64) NOT NULL,
        mask_hex CHAR(64) NOT NULL,
        unlocked BOOLEAN NOT NULL,
        PRIMARY KEY (txin_id, height, key_hex),
        CONSTRAINT fk_output_details_txin_id
          FOREIGN KEY (txin_id)
          REFERENCES txins (txin_id),
        CONSTRAINT fk_od_height
          FOREIGN KEY (height)
          REFERENCES blocks (height)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


