__author__ = 'teemu kanstren'

from src.python.moneroscraper.transaction import Transaction
from src.python.moneroscraper.block import Block
from mysql.connector.connection import MySQLConnection, MySQLCursor
from codeprofile import profiler
from src.python.moneroscraper import logging_config

logger = logging_config.create_logger(__name__)

#https://stackoverflow.com/questions/775296/mysql-parameterized-queries
INSERT_BLOCK = "INSERT INTO blocks (height, block_size, weight, difficulty, cumulative_difficulty, hash, long_term_weight, major_version, minor_version, nonce, reward, block_time, wide_cumulative_difficulty, wide_difficulty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
INSERT_TRANSACTION_XMR = "INSERT INTO transactions (version, hash, fee, height, unlocktime, tx_extra) VALUES (%s, %s, %s, %s, %s, %s)"
INSERT_TRANSACTION_XHV = "INSERT INTO transactions (version, hash, fee, height, unlocktime, tx_extra, amount_burnt, amount_minted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
INSERT_TXIN = "INSERT INTO txins (tx_id, amount, keyimage, coinbase) VALUES (%s, %s, %s, %s)"
INSERT_TXOUT_XMR = "INSERT INTO txouts (tx_id, amount, target_key) VALUES (%s, %s, %s)"
INSERT_TXOUT_XHV = "INSERT INTO txouts (tx_id, amount, target_key, tx_type, asset_type) VALUES (%s, %s, %s, %s, %s)"
INSERT_KEY_OFFSET = "INSERT INTO key_offsets (txin_id, offset) VALUES (%s, %s)"
INSERT_OUTPUT_DETAILS = "INSERT INTO output_details (txin_id, tx_id, height, key_hex, mask_hex, unlocked) VALUES (%s, %s, %s, %s, %s, %s)"
SELECT_MAX_BLOCK_HEIGHT = "SELECT MAX(height) FROM blocks"

def insert_transaction(c: MySQLCursor, t: Transaction, coin_type):
    with profiler.profile("sql: insert tx"):
        if coin_type == 'xmr':
            c.execute(INSERT_TRANSACTION_XMR, (t.version, t.hash_hex, t.fee, t.block_height, t.unlock_time, t.tx_extra))
        elif coin_type == 'xhv':
            c.execute(INSERT_TRANSACTION_XHV, (t.version, t.hash_hex, t.fee, t.block_height, t.unlock_time, t.tx_extra, t.amount_burnt, t.amount_minted))
        else:
            raise NotImplementedError(f"Uknown coint type: {coin_type}")
    t.tx_id = c.lastrowid
    #print(f"inserted transaction, rows updated{c.rowcount}")
    for tx_in in t.tx_ins:
        with profiler.profile("sql: insert txin"):
            c.execute(INSERT_TXIN, (t.tx_id, tx_in.amount, tx_in.key_image, tx_in.coinbase))
        tx_in.txin_id = c.lastrowid
        for keyoffset in tx_in.key_offsets:
            with profiler.profile("sql: insert key offset"):
                c.execute(INSERT_KEY_OFFSET, (tx_in.txin_id, keyoffset))
        for od in tx_in.out_details:
            od.tx_id = t.tx_id
            with profiler.profile("sql: insert output details"):
                c.execute(INSERT_OUTPUT_DETAILS, (tx_in.txin_id, od.tx_id, od.height, od.key_hex, od.mask_hex, od.unlocked))
    for tx_out in t.tx_outs:
        with profiler.profile("sql: insert txout"):
            if coin_type == 'xmr':
                c.execute(INSERT_TXOUT_XMR, (t.tx_id, tx_out.amount, tx_out.target_key))
            elif coin_type == 'xhv':
                c.execute(INSERT_TXOUT_XHV, (t.tx_id, tx_out.amount, tx_out.target_key, tx_out.tx_type, tx_out.asset_type))
            else:
                raise NotImplementedError(f"Uknown coint type: {coin_type}")
    pass

def get_max_block(conn: MySQLConnection):
    c = conn.cursor()
    c.execute(SELECT_MAX_BLOCK_HEIGHT)
    height = c.fetchone()
    c.close()
    return height

def insert_block(conn: MySQLConnection, block: Block, coin_type: str):
    c = conn.cursor()
    try:
        b = block
        with profiler.profile("sql: insert block"):
            c.execute(INSERT_BLOCK, (b.height, b.block_size, b.block_weight, b.difficulty, b.cumulative_difficulty, b.hash, b.long_term_weight, b.major_version, b.minor_version, b.nonce, b.reward, b.timestamp, b.wide_cumulative_difficulty, b.wide_difficulty))
        bt = b.miner_tx
        with profiler.profile("insert cb transaction"):
            insert_transaction(c, bt, coin_type)
#        c.execute(INSERT_TRANSACTION, (bt.version, bt.hash_hex, bt.fee, bt.block_height, bt.unlock_time))
        bt.tx_id = c.lastrowid
        for t in b.txs:
#        hash_value = int(t.hash_hex, 16)
            with profiler.profile("insert transaction"):
                insert_transaction(c, t, coin_type)
#            c.execute(INSERT_TRANSACTION, (t.version, t.hash_hex, t.fee, t.block_height, t.unlock_time))
#            t.tx_id = c.lastrowid
#            print(f"inserted transaction, rows updated{c.rowcount}")
#            for tx_in in t.tx_ins:
#                c.execute(INSERT_TXIN, (t.tx_id, tx_in.amount, tx_in.key_image, tx_in.coinbase))
#                tx_in.txin_id = c.lastrowid
#                for keyoffset in tx_in.key_offsets:
#                    c.execute(INSERT_KEY_OFFSET, (tx_in.txin_id, keyoffset))
#                for od in tx_in.out_details:
#                    od.tx_id = t.tx_id
#                    c.execute(INSERT_OUTPUT_DETAILS, (od.tx_id, od.height, od.key_hex, od.mask_hex, od.unlocked))
#            for tx_out in t.tx_outs:
#                c.execute(INSERT_TXOUT, (t.tx_id, tx_out.amount, tx_out.target_key))
        conn.commit()
        c.close()
    except Exception as e:
        logger.exception(f"ERROR AT HEIGHT:{block.height}") #should automatically dump the stack
        conn.rollback()
        c.close()
