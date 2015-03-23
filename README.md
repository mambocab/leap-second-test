A test rig for demonstrating Cassandra bugs triggered by the leap second.

This has some problems at the time of writing:

- The test rig assumes a number of things, like the location of Cassandra (~/git/cassandra)
- Nothing guarantees that the insertions happen over the scheduled leap second.
- The use of `leap-a-day` is off-label. The leap-second scheduling binary should be tightened up; for instance, it doesn't need to print that diagnostic information.
- `insert-keys.py` is minimal. It won't extend easily to setups with, e.g., multiple nodes.

I chose to use the Python driver rather than CCM because this test only needs one node, and so I could run the external leap-second-scheduling program between starting Cassandra and running `insert-keys.py`.
