# Distributed Update Buffer

A repo illustrating how one could construct a distributed update buffer.

## Reasoning

If you have a workload that needs to update based on an ID and multiple updates for the same ID are close together chronilogically, then this system could save computations.

These redis scripts are to showcase how to have an update buffer combined with a reader queue.

For example, say you have 1 ID that needs to calculate an update every time something changes. If you have 3 updates, you would do 3 calculations. Say those updates happen close to one another. If they're close enough, this system will instead queue these up as one update and then reduce that to one calculation based on the time buffer.

Example continued. ID - 101 writes at periods 1s, 2s, 5s, 15s with a 10s buffer time. Without this system, all 4 would be processed and 4 calculations would happen. With this system, the 1s, 2s, 5s updates would be calculated at (1s + 10s) the 11s time and the 15s update would be processed at (15s+10s) the 25s time - for a total of 2 updates. Across a massive distributed system, this could save lots of updates.

## Logic
- You write an ID with the amount of time you are willing to wait in seconds
- writefile.lua checks if the cache map already has an entry for that ID. If so, it no-ops; otherwise, add to the cache with a timestamp in the future. Also add and ID reference to a queue.
- On a polling strategy, readfile.lua when called will look at the head of the queue and see if the time duration has transpired. If so, it will digest the queue until the max return is met or the time duration logic fails. It then deletes from the cache map and will allow for more writes for that ID.


## Development
Command line query examples:

`redis-cli --eval writefile.lua buffermap bufferlist , 2224 60`

`redis-cli --eval readfile.lua buffermap bufferlist , 3`

With debugging flag:

`redis-cli --ldb --eval readfile.lua buffermap bufferlist , 10`
