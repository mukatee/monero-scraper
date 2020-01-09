__author__ = 'teemu kanstren'

from monero.transaction import Transaction
from monero.block import Block
from mysql.connector.connection import MySQLConnection, MySQLCursor
import traceback


#https://stackoverflow.com/questions/775296/mysql-parameterized-queries
INSERT_BLOCK = "INSERT INTO blocks (height, block_size, weight, difficulty, cumulative_difficulty, hash, long_term_weight, major_version, minor_version, nonce, reward, block_time, wide_cumulative_difficulty, wide_difficulty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
INSERT_TRANSACTION = "INSERT INTO transactions (version, hash, fee, height, unlocktime) VALUES (%s, %s, %s, %s, %s)"
INSERT_TXIN = "INSERT INTO txins (tx_id, amount, keyimage, coinbase) VALUES (%s, %s, %s, %s)"
INSERT_TXOUT = "INSERT INTO txouts (tx_id, amount, target_key) VALUES (%s, %s, %s)"
INSERT_KEY_OFFSET = "INSERT INTO key_offsets (txin_id, offset) VALUES (%s, %s)"
INSERT_OUTPUT_DETAILS = "INSERT INTO output_details (txin_id, height, key_hex, mask_hex, unlocked) VALUES (%s, %s, %s, %s, %s)"

def insert_transaction(c: MySQLCursor, t: Transaction):
    c.execute(INSERT_TRANSACTION, (t.version, t.hash_hex, t.fee, t.block_height, t.unlock_time))
    t.tx_id = c.lastrowid
    print(f"inserted transaction, rows updated{c.rowcount}")
    for tx_in in t.tx_ins:
        c.execute(INSERT_TXIN, (t.tx_id, tx_in.amount, tx_in.key_image, tx_in.coinbase))
        tx_in.txin_id = c.lastrowid
        for keyoffset in tx_in.key_offsets:
            c.execute(INSERT_KEY_OFFSET, (tx_in.txin_id, keyoffset))
        for od in tx_in.out_details:
            od.tx_id = t.tx_id
            c.execute(INSERT_OUTPUT_DETAILS, (od.tx_id, od.height, od.key_hex, od.mask_hex, od.unlocked))
    for tx_out in t.tx_outs:
        c.execute(INSERT_TXOUT, (t.tx_id, tx_out.amount, tx_out.target_key))


def insert_block(conn: MySQLConnection, block: Block):
    c = conn.cursor()
    try:
        b = block
        c.execute(INSERT_BLOCK, (b.height, b.block_size, b.block_weight, b.difficulty, b.cumulative_difficulty, b.hash, b.long_term_weight, b.major_version, b.minor_version, b.nonce, b.reward, b.timestamp, b.wide_cumulative_difficulty, b.wide_difficulty))
        bt = b.miner_tx
        #TODO: make insert_transaction with all txin etc and call that here as well
        insert_transaction(c, bt)
#        c.execute(INSERT_TRANSACTION, (bt.version, bt.hash_hex, bt.fee, bt.block_height, bt.unlock_time))
        bt.tx_id = c.lastrowid
        for t in b.txs:
#        hash_value = int(t.hash_hex, 16)
            insert_transaction(c, t)
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
        conn.rollback()
        traceback.print_exc()
        c.close()
