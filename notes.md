# Notes on data structures

These are just my personal notes trying to understand the Monero protocol and related data structures.
Based on reading the [daemon documentation](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html), [StackExchange](https://monero.stackexchange.com/) posts, and running the RPC protocol and looking at what it gives.
Reding the code would likely be needed for the final details but I don't have the resources to go there now.
Also, maybe I don't need all the details, so let me know if you have any updates :) (pull req or other)

## Block Structure

Main RPC call: [get_block](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#get_block)

* Height: height of the blockchain at which this block appears
* Block size: block size in bytes
* Block weight: weighted block size. somehow different from raw block size, [weighted by different factors](https://monero.stackexchange.com/questions/11809/how-to-compute-block-weight). [affects block fees](https://monero.stackexchange.com/questions/4562/how-does-the-dynamic-blocksize-and-the-dynamic-fees-work-together-in-monero), etc. still a bit unclear to me how this works in Monero vs [other](https://en.bitcoin.it/wiki/Weight_units), but that seems to be the general idea.
* Cumulative difficulty: Cumulative difficulty of all blocks in the blockchain. I think it just sums up all difficulties of all blocks. Which sounds too much, but if you look the numbers up, they are huge.
* Cumulative difficulty top 64: Some kind of smaller summary of cumulative difficulty. Either 64 top blocks, or top bits, is what I think...
* Difficulty: Block difficulty (non-cumulative)
* Difficulty top 64: Same as "Cumulative difficulty top 64" but for block level (non-cumulative).
* Hash: Block hash
* Long term weight: Seems to be [block weight](long_term_block_weight the long term block weight of the block (transactions and all)), assuming some kind of sum of "block weight" over time. Some [Monero Labs notes](https://web.getmonero.org/2019/02/04/logs-for-the-Monero-Research-Lab-meeting-held-on-2019-02-04.html) at least discuss using it as part of network fees. Whatever that means..
* Miner transaction hash: The hash for the coinbase transaction in the block, paying the miner. I just noticed I [asked about it](https://monero.stackexchange.com/questions/11893/what-is-miner-tx-hash) on Stack Exchange before..
* Major version: [Major version](https://monero.stackexchange.com/questions/3958/what-is-the-format-of-a-block-in-the-monero-blockchain) of Monero protocol at this block height. Defines block header parsing rules.
* Minor version: [Minor version](https://monero.stackexchange.com/questions/3958/what-is-the-format-of-a-block-in-the-monero-blockchain) of Monero protocol at this block height. Defines interpretation details, not related to header parsing.
* Nonce: The random value used to find the hash for this block.
* Number of transactions (num_txs): Number of transactions in the block, excluding the coinbase transaction.
* Previous hash (prev_hash): Hash for the previous block in the chain.
* Reward: Number of atomic units assigned to the miner in this block.
* Timestamp: The unix time at which the block was recorded into the blockchain. I guess it is epoch.. in seconds.
* Wide Difficulty: Hard to find what this means, except this one [Monero commit](https://git.xmr.pm/monero-project/monero/commit/91f4c7f45f794fc7bee99356e56853369c98c410) which is described as changing difficulty to 128 bit instead of 64 bit. So I guess this wide difficulty is just reference to 128 bits. Maybe top64 is also bit reference..?
* Wide Cumulative Difficulty: Its just the cumulative version..
* Credits: ??? Always appears to be 0, cannot find any reference to what this is.
* Status: OK or error code (RPC).
* Top hash: Again, this seems empty. But I guess it would be a reference to the hash of the block on top of the chain. Because there is something called "top_block_hash" in the [Daemon get_info() docs](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#get_info).
* Untrusted: Being untrusted (=this value is true) means the node has not been fully synced from scratch but rather bootstrapper from some other source. Like a checkpoint dump I guess.

