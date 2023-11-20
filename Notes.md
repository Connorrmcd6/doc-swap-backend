Check list:

- Make sure users-submission table is empty and has the columns:
  timestamp email consent current_placement first_choice second_choice third_choice

case and spelling IMPORTANT for all except consent column

- Run script with emails turned off to check if everything is working
- Remove swapped status from users that swapped in test run or email them manually
- Run a few times testing different parameters
  default: n-sample =50; choice_max = 3, avg_weight_per_edge_threshold=1.5

  ############################################

Once enough users have submitted their choices, run `cron.py` on a cron every 20 mins (`*/20 * * * *`) to determine swaps. This may need to be adjusted as gmail only allows 100 emails per day I think.
_/10 _ \* \* \* /Users/connormcdonald/opt/anaconda3/bin/python /Users/connormcdonald/Desktop/GitHub/doc-swap-backend/cron.py >> /Users/connormcdonald/Desktop/GitHub/doc-swap-backend/logs.txt

Adjust the configs of the algorthim accordingly in the `configs.py` file:

- `n-sample`: the number of people to randomly select from the selection pool
- `choice_max`: the maximum choice weight to include
- `avg_weight_per_edge_threshold`: maximum average choice per user in a cycle to consider as a valid swap. Lower value will be less swaps but higher quality swaps.
- `turn_on_email`: this switch will turn emails on or off, if it is set to 0 the emails will be printed to console otherwise they will be sent to the real addresses.

The users emails and swap diagrams will be named as a reference number which the users can then use to query their swap. These are stored in the swaps folder.
