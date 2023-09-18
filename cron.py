from functions import *

sample_seed = random.randint(0, 999999)


# step 1: connect to google sheets
gs_connection = connect_to_gs(
    "/Users/connormcdonald/Desktop/GitHub/doc-swap-backend/gcp_service_account.json"
)
print("step 1 complete")

# step 2: pull all data submitted via forms
user_submissions = fetch_google_sheets_data(
    gs_connection, user_submissions_table, prod_google_sheet_key, []
)
user_status = fetch_google_sheets_data(
    gs_connection, user_status_table, prod_google_sheet_key, []
)
print("step 2 complete")

# step 3: transfer new records to user-status and return user-status table
user_status, new_submissions = update_user_status(user_submissions, user_status)
if new_submissions is not None:
    write_google_sheets_data(
        gs_connection, new_submissions, user_status_table, prod_google_sheet_key
    )

# step 3a: account for people reapplying
user_status, update_flag = get_reapplications(user_submissions, user_status)
if update_flag is not None:
    # write_google_sheets_data(gs_connection, user_status, user_status_table, prod_google_sheet_key)
    update_swap_status(gs_connection, user_status, prod_google_sheet_key)
print("step 3 complete")

for i in range(5):
    # step 4: generate selection pool
    selection_pool = generate_selection_pool(
        user_submissions, user_status, n_sample, sample_seed
    )
    print("step 4 complete")

    # step 5: melt selection pool
    melted_selection_pool_df = melt_choices(selection_pool, choice_max)
    print("step 5 complete")

    # step 6: generate graph
    G = nx.MultiDiGraph()

    for i in melted_selection_pool_df.index:
        G.add_edge(
            melted_selection_pool_df.choice[i],
            melted_selection_pool_df.current_placement[i],
            edge_key=i,
            weight=melted_selection_pool_df.choice_number[i],
        )
    print("step 6 complete")

    # step 7: Find all cycles in the graph
    cycles = list(nx.simple_cycles(G))
    print("step 7 complete")
    if len(cycles) > 0:
        # step 8: generate average weight per edge to assess cycle quality
        cycle_data = []
        for cycle in cycles:
            cycle_length = len(cycle)
            cycle.append(cycle[0])
            path_wt = nx.path_weight(G, cycle, "weight")
            avg_wt = path_wt / cycle_length
            cycle_data.append(
                {
                    "cycle": cycle,
                    "weight": path_wt,
                    "avg_weight_per_edge": avg_wt,
                    "cycle_len": cycle_length,
                }
            )

        cycle_df = pd.DataFrame(cycle_data)
        cycle_df = cycle_df.sort_values(
            by=["avg_weight_per_edge", "cycle_len"], ascending=[True, False]
        )
        print("step 8 complete")

        # step 9: remove overlapping cycles
        best_cycles = remove_overlapping_cycles(cycle_df)
        best_cycles = best_cycles[
            best_cycles.avg_weight_per_edge <= avg_weight_per_edge_threshold
        ]
        print("step 9 complete")

        # step 10 generate swaps:
        try:
            generate_swaps(
                gs_connection,
                best_cycles,
                melted_selection_pool_df,
                G,
                user_status,
                turn_on_email,
            )
            print("step 10 complete")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    else:
        print("no swaps found")

curr_time = time.strftime("%H:%M:%S", time.localtime())
print(f"finished at :{curr_time}")
