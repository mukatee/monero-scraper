# Notes on data structures

These are just my personal notes trying to understand the Monero protocol and related data structures.
Based on reading the [daemon documentation](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html), [StackExchange](https://monero.stackexchange.com/) posts, and running the RPC protocol and looking at what it gives.

## Block Structure

Main RPC call: [get_block](https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#get_block)

* Height: height of the blockchain at which this block appears
* Block size: block size in bytes
* Block weight: weighted block size. somehow different from raw block size, [weighted by different factors](https://monero.stackexchange.com/questions/11809/how-to-compute-block-weight). [affects block fees](https://monero.stackexchange.com/questions/4562/how-does-the-dynamic-blocksize-and-the-dynamic-fees-work-together-in-monero), etc. still a bit unclear to me how this works in Monero vs [other](https://en.bitcoin.it/wiki/Weight_units), but that seems to be the general idea.
* Cumulative difficulty: Cumulative difficulty of all blocks in the blockchain. I think it just sums up all difficulties of all blocks. Which sounds too much, but if you look the numbers up, they are huge.
* Cumulative difficulty top 64: Some kind of smaller summary of cumulative difficulty. Either 64 top blocks, or top bits, is what I think...
* Difficulty: Block difficulty (non-cumulative)
* Difficulty top 64: Same as "Cumulative difficulty top 64" but for block level (non-cumulative).




