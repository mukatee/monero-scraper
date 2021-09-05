/*
 Ignoring some fields such as orphan status, assuming to not store forked chains.
 For the same reasons, assuming height works as a unique block id
 */

    CREATE TABLE blocks (
        height INT UNSIGNED NOT NULL UNIQUE,
        block_size MEDIUMINT UNSIGNED NOT NULL,
        weight MEDIUMINT UNSIGNED NOT NULL,
        difficulty BIGINT NOT NULL,
        cumulative_difficulty BIGINT NOT NULL,
        hash VARCHAR(64) NOT NULL,
        long_term_weight MEDIUMINT UNSIGNED NOT NULL,
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
        hash VARCHAR(64) NOT NULL,
        fee BIGINT UNSIGNED NOT NULL,
        height INT UNSIGNED NOT NULL,
        unlocktime BIGINT UNSIGNED NOT NULL, /** The daemon docs say this is block height, but actually can also be a timestamp in epoch seconds or millis. huh. for example, block 383000 has 1420722551128, so int is not enough. */
        tx_extra TEXT(65535) NOT NULL,
        amount_burnt BIGINT UNSIGNED NOT NULL,
        amount_minted BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (tx_id),
        CONSTRAINT fk_tx_height
          FOREIGN KEY (height)
          REFERENCES blocks (height)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE txins (
        txin_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        tx_id BIGINT UNSIGNED NOT NULL,
        amount BIGINT UNSIGNED NOT NULL,
        keyimage VARCHAR(64) NOT NULL,
        coinbase BOOLEAN NOT NULL,
        PRIMARY KEY (txin_id),
        CONSTRAINT fk_txins_txid
          FOREIGN KEY (tx_id)
          REFERENCES transactions (tx_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

    CREATE TABLE txouts (
        tx_id BIGINT UNSIGNED NOT NULL,
        amount BIGINT UNSIGNED NOT NULL,
        target_key VARCHAR(64) NOT NULL,
        tx_type VARCHAR(64) NOT NULL,
        asset_type VARCHAR(64) NULL,
        /* PRIMARY KEY (tx_id, target_key), */ /* <- it appears that txouts (vout in the api) are not unique. just some keys, and even amounts zeroed in later procol versions. */
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
        tx_id BIGINT UNSIGNED,
        txin_id BIGINT UNSIGNED,
        height INT UNSIGNED NOT NULL,
        key_hex VARCHAR(64) NOT NULL,
        mask_hex VARCHAR(64) NOT NULL,
        unlocked BOOLEAN NOT NULL,
/**        PRIMARY KEY (tx_id, txin_id, height, key_hex), <- block 327625 has a a txin with the same output details twice. hash 1c979b266366569f64509502968ad43e9eeb851b297511e683118d0cafee05ee , from block 00320816, amount 0.111111111111  */
        CONSTRAINT fk_output_details_txin_id
          FOREIGN KEY (txin_id)
          REFERENCES txins (txin_id),
        CONSTRAINT fk_od_height
          FOREIGN KEY (height)
          REFERENCES blocks (height)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


