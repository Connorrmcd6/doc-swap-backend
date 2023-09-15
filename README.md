Once enough users have submitted their choices, run `cron.py` on a cron every 20 mins (`*/20 * * * *`) to determine swaps. This may need to be adjusted as gmail only allows 100 emails per day I think.

Adjust the configs of the algorthim accordingly in the `configs.py` file:

- `n-sample`: the number of people to randomly select from the selection pool
- `choice_max`: the maximum choice weight to include
- `avg_weight_per_edge_threshold`: maximum average choice per user in a cycle to consider as a valid swap. Lower value will be less swaps but higher quality swaps.

The users emails and swap diagrams will be named as a reference number which the users can then use to query their swap. These are stored in the swaps folder.
