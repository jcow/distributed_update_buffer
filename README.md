# Distributed Update Buffer

A repo illustrating how one could construct a distributed update buffer.

## Reasoning

If you have a workload that needs to update based on a trigger; however, if you have a lot of triggers firing at the same time, then you could be doing redundant work. These redis scripts are to showcase how to have an update
buffer combined with a reader queue.
