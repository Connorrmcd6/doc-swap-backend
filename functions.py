import numpy as np
from configs import *
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from gspread_dataframe import set_with_dataframe
import gspread
import random
from google.oauth2 import service_account
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders


def connect_to_gs(path):
    gs_connection = gspread.service_account(path)
    return gs_connection


def write_google_sheets_data(_gc, df, sheet_name, sheet_key):
    try:
        # Open specific sheet
        gs = _gc.open_by_key(sheet_key)

        # Open specific tab within the sheet
        tab = gs.worksheet(sheet_name)

        df_values = df.values.tolist()
        gs.values_append(sheet_name, {"valueInputOption": "RAW"}, {"values": df_values})

        return None

    except gspread.exceptions.APIError as e:
        print("Error accessing Google Sheets API:", e)
        return None
    except gspread.exceptions.WorksheetNotFound as e:
        print(f"Error: Worksheet not found, please create a new tab named:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def fetch_google_sheets_data(_gc, sheet_name, sheet_key, columns_list):
    try:
        # Open specific sheet
        gs = _gc.open_by_key(sheet_key)

        # Open specific tab within the sheet
        tab = gs.worksheet(sheet_name)

        data = tab.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)

        # to handle numeric columns that are imported as strings
        for column in columns_list:
            df[column] = pd.to_numeric(df[column])

        return df

    except gspread.exceptions.APIError as e:
        print("Error accessing Google Sheets API:", e)
        return None
    except gspread.exceptions.WorksheetNotFound as e:
        print("Error: Worksheet not found:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def get_latest_record_per_email(df):
    # Convert the timestamp column to datetime if not already
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort the DataFrame by email and timestamp
    df.sort_values(by=["email", "timestamp"], ascending=[True, False], inplace=True)

    # Group by email and select the first record in each group (latest due to sorting)
    latest_records = df.groupby("email").first().reset_index()

    return latest_records


def generate_selection_pool(user_submissions_df, user_status_df, n_sample, sample_seed):
    # Convert the timestamp column to datetime if not already
    user_submissions_df["timestamp"] = pd.to_datetime(user_submissions_df["timestamp"])

    # Sort the DataFrame by email and timestamp
    user_submissions_df.sort_values(
        by=["email", "timestamp"], ascending=[True, False], inplace=True
    )

    # Group by email and select the first record in each group (latest due to sorting)
    latest_submissions = user_submissions_df.groupby("email").first().reset_index()

    # Filter the user_status_df DataFrame to only include records where 'swapped' is 'no'
    user_status_df_no = user_status_df[user_status_df["swapped"] == "no"]

    # Filter the latest_submissions DataFrame to only include records where email appears in user_status_df
    latest_submissions_filtered = latest_submissions[
        latest_submissions["email"].isin(user_status_df_no["email"])
    ]

    # Exclude the last column of user_submissions_df
    try:
        latest_submissions_filtered = latest_submissions_filtered.sample(
            n=n_sample, random_state=sample_seed
        ).iloc[:, [0, 1, 2, 3, 4, 5]]
    except:
        latest_submissions_filtered = latest_submissions_filtered.iloc[
            :, [0, 1, 2, 3, 4, 5]
        ]

    return latest_submissions_filtered


def melt_choices(df, choice_max):
    # Define the columns to keep as identifier variables (email and current_placement)
    id_vars = ["email", "current_placement"]

    # Use melt to unpivot the DataFrame, specifying the id_vars
    melted = pd.melt(df, id_vars=id_vars, var_name="choice_number", value_name="choice")

    # Map choice_number to numbers 1, 2, and 3
    choice_number_mapping = {"first_choice": 1, "second_choice": 2, "third_choice": 3}
    melted["choice_number"] = melted["choice_number"].map(choice_number_mapping)

    # Sort the DataFrame by email for better organization
    melted.sort_values(by="email", inplace=True)
    melted = melted[melted.choice_number <= choice_max]

    return melted


def remove_overlapping_cycles(df):
    # Initialize an empty list to keep track of unique cycles
    unique_cycles = []

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the current cycle has any common element with unique cycles
        has_common_element = False
        for cycle in unique_cycles:
            if any(item in cycle for item in row["cycle"]):
                has_common_element = True
                break

        # If there's no common element, add the cycle to unique_cycles
        if not has_common_element:
            unique_cycles.append(row["cycle"])
        else:
            # Remove rows with a common element from the DataFrame
            df.drop(index, inplace=True)

    return df


def generate_random_csv(n, output_file):
    # Define the list of 15 unique colors
    unique_colors = [
        "hospital_0",
        "hospital_1",
        "hospital_2",
        "hospital_3",
        "hospital_4",
        "hospital_5",
        "hospital_6",
        "hospital_7",
        "hospital_8",
        "hospital_9",
        "hospital_10",
        "hospital_11",
        "hospital_12",
        "hospital_13",
        "hospital_14",
        "hospital_15",
        "hospital_16",
        "hospital_17",
        "hospital_18",
        "hospital_19",
        "hospital_20",
        "hospital_21",
        "hospital_22",
        "hospital_23",
        "hospital_24",
        "hospital_25",
        "hospital_26",
        "hospital_27",
        "hospital_28",
        "hospital_29",
        "hospital_30",
        "hospital_31",
        "hospital_32",
        "hospital_33",
        "hospital_34",
        "hospital_35",
        "hospital_36",
        "hospital_37",
        "hospital_38",
        "hospital_39",
        "hospital_40",
        "hospital_41",
        "hospital_42",
        "hospital_43",
        "hospital_44",
        "hospital_45",
        "hospital_46",
        "hospital_47",
        "hospital_48",
        "hospital_49",
        "hospital_50",
        "hospital_51",
        "hospital_52",
        "hospital_53",
        "hospital_54",
        "hospital_55",
        "hospital_56",
        "hospital_57",
        "hospital_58",
        "hospital_59",
        "hospital_60",
        "hospital_61",
        "hospital_62",
        "hospital_63",
        "hospital_64",
        "hospital_65",
        "hospital_66",
        "hospital_67",
        "hospital_68",
        "hospital_69",
    ]

    # Create an empty DataFrame
    df = pd.DataFrame(
        columns=[
            "email",
            "current_placement",
            "first_choice",
            "second_choice",
            "third_choice",
        ]
    )

    for _ in range(n):
        # Shuffle the colors to ensure randomness
        random.shuffle(unique_colors)

        # Randomly select colors for the last four columns
        first_choice = unique_colors[0]
        second_choice = unique_colors[1]
        third_choice = unique_colors[2]
        current_placement = unique_colors[4]

        # Generate random values for the 'email' and 'current_placement' columns
        email = f"user{_}@example.com"
        # current_placement = random.randint(1, 10)

        # Append the row to the DataFrame
        df = df.append(
            {
                "email": email,
                "current_placement": current_placement,
                "first_choice": first_choice,
                "second_choice": second_choice,
                "third_choice": third_choice,
            },
            ignore_index=True,
        )

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)


def send_email(sender, passwd, recipients, subject, body, attachment_path=None):
    try:
        message = MIMEMultipart()

        message["From"] = sender
        # message['To'] = ", ".join(recipients)
        message["Cc"] = ", ".join(recipients)
        message["Subject"] = subject

        # Add the body of the email
        message.attach(MIMEText(body, "html"))

        # Attach the PNG image if provided
        if attachment_path:
            with open(attachment_path, "rb") as attachment_file:
                attachment = MIMEImage(attachment_file.read(), _subtype="png")
                attachment.add_header(
                    "Content-Disposition", f'attachment; filename="{attachment_path}"'
                )
                message.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(sender, passwd)
        server.sendmail(sender, recipients, message.as_string())
        server.quit()
        print("Send successful")
    except Exception as e:
        print(f"Error sending mail: {e}")


def check_consecutive(tuple_to_check, n_bunch):
    # Iterate through the list to find the first occurrence of the first element in the tuple
    for i in range(len(n_bunch)):
        if n_bunch[i] == tuple_to_check[0]:
            # Check if the remaining elements of the tuple occur consecutively in the list
            for j in range(1, len(tuple_to_check)):
                if i + j >= len(n_bunch) or n_bunch[i + j] != tuple_to_check[j]:
                    return False
            return True
    return False


def generate_swaps(
    gs_connection, best_cycles, melted_selection_pool_df, G, user_status, turn_on_email
):
    # Create the "swaps" directory if it doesn't exist
    if not os.path.exists(
        "/Users/connormcdonald/Desktop/GitHub/doc-swap-backend/swaps"
    ):
        os.makedirs("/Users/connormcdonald/Desktop/GitHub/doc-swap-backend/swaps")

    for iteration, n_bunch in enumerate(best_cycles.cycle, start=1):
        G2 = nx.subgraph(G, nbunch=n_bunch)
        edge_list = list(G2.edges(data=True))

        consecutive_edges = []
        n_bunch_indices = {node: [] for node in n_bunch}
        unique_edges = {}

        # Build the dictionary of node indices in n_bunch
        for idx, node in enumerate(n_bunch):
            n_bunch_indices[node].append(idx)

        # Iterate through edge_list and check for consecutive nodes
        for node1, node2, edge_data in edge_list:
            edge_weight = edge_data["weight"]
            edge_key = edge_data["edge_key"]
            is_consecutive = check_consecutive((node1, node2), n_bunch)

            if is_consecutive and (
                (node1, node2) not in unique_edges
                or edge_weight < unique_edges[(node1, node2)]["weight"]
            ):
                unique_edges[(node1, node2)] = {
                    "weight": edge_weight,
                    "edge_key": edge_key,
                }

                edge_keys_list = [
                    edge_data["edge_key"] for edge_data in unique_edges.values()
                ]

                final_edge_df = melted_selection_pool_df.loc[edge_keys_list, :]

        F = nx.DiGraph()

        for i in final_edge_df.index:
            F.add_edge(
                final_edge_df.current_placement[i],
                final_edge_df.choice[i],
                key=final_edge_df.email[i],
            )

        edge_labels = {
            (final_edge_df.current_placement[i], final_edge_df.choice[i]): str(
                final_edge_df.email[i]
            )
            for i in final_edge_df.index
        }

        swap_size = len(final_edge_df.index)
        figsize = (np.ceil(swap_size * 3), np.ceil(swap_size * 3))
        pos = nx.spectral_layout(F)

        fig = plt.figure(1, figsize=figsize, dpi=100)
        nx.draw_networkx(
            F,
            pos=pos,
            with_labels=True,
            width=1,
            arrowsize=20,
            node_size=2000,
            node_color="#A398F0",
        )
        nx.draw_networkx_edge_labels(F, pos, edge_labels=edge_labels)

        # Generate the filename with timestamp and iteration number
        timestamp = int(time.time())
        filename = f"/Users/connormcdonald/Desktop/GitHub/doc-swap-backend/swaps/{timestamp}_{iteration}.png"
        filename2 = f"/Users/connormcdonald/Desktop/GitHub/doc-swap-backend/swaps/{timestamp}_{iteration}.csv"

        # Create a new DataFrame containing only the selected column
        emails = final_edge_df[["email"]]
        recipients = list(final_edge_df.email)
        # Save the selected column to a CSV file
        emails.to_csv(filename2, index=False)

        # Save the plot as an image
        plt.savefig(filename)

        # Close the plot to release resources
        plt.close()

        # ---- send emails here ---
        if len(recipients) > 2:
            attachment_path = filename
        else:
            attachment_path = None

        n_swap = len(recipients)
        ref_number = f"{timestamp}_{iteration}"

        body = f"""<html>
                    <body>
                        <p>It's your lucky day 🎉</p>

                        <p>We have found a <strong>{n_swap}-way swap</strong> for your internship placement! You can find their email(s) in the recipients section of this mail.</p>

                        <p>So what's next?</p>
                        <ul>
                            <li>You should get in touch with each other and coordinate your swap; it's probably best to do this with a group chat. If you have more than a 2-way swap, a diagram will be attached to this mail to guide you on who needs to swap with who.</li>
                            <li>Notify your hospitals of the swap.</li>
                            <li>Tell your friends about DocSwap!</li>
                        </ul>

                        <p>🚨 Some important things to consider</p>
                        <ul>
                            <li>Due to the nature of multiway swaps, they will <strong>ONLY</strong> work if everyone is onboard. If one of you backs out, the chain will be broken, and the swap will no longer work!</li>
                            <li>If this happens to your SwapGroup, you should re-apply on <a href="https://docswap.streamlit.app/">DocSwap</a> so that we can find you another SwapGroup.</li>
                            <li>If you are not happy with your SwapGroup, you should notify them ASAP so that everyone can re-apply</li>
                            <li>Some people don't check their emails; don't sit around waiting forever. If someone in your SwapGroup hasn't responded to any of your emails, you should notify them one last time that you are backing out of the swap and re-applying for a different SwapGroup.</li>
                        </ul>

                        <p>If you have any questions or feedback, please submit it on <a href="https://forms.gle/kW8PFEtboYf3JiKS6">this form</a> with the reference number: <strong>{ref_number}</strong></p>
                    </body>
                    </html>
                    """

        # send_email(email_sender, email_passwd, recipients, email_subject, body, attachment_path=attachment_path)
        if turn_on_email == 0:
            print(f"would send email to {recipients}")
        if turn_on_email == 1:
            send_email(
                email_sender,
                email_passwd,
                recipients,
                email_subject,
                body,
                attachment_path=attachment_path,
            )

        # ---- update user status table here ---

        user_status = update_swapped_column(user_status, recipients)
        update_swap_status(gs_connection, user_status, prod_google_sheet_key)


def update_user_status(user_submissions_df, user_status_df):
    # Extract unique emails from user_submissions_df
    unique_emails = set(user_submissions_df["email"])

    # Filter out emails that already exist in user_status_df
    new_emails = [
        email
        for email in unique_emails
        if email not in user_status_df["email"].tolist()
    ]

    if not new_emails:
        # No new emails to add
        new_records = None
        return user_status_df, new_records

    # Create a DataFrame with new email addresses
    new_records = pd.DataFrame({"email": new_emails, "swapped": "no"})

    # Add the current human-readable time to the 'updated_at' column
    current_time = pd.Timestamp("now").strftime("%m/%d/%Y %H:%M:%S")
    new_records["updated_at"] = current_time
    # new_records['updated_at'] = pd.to_datetime(user_submissions_df['timestamp'])

    # Append the new records to user_status_df
    updated_user_status_df = pd.concat([user_status_df, new_records], ignore_index=True)

    return updated_user_status_df, new_records


def get_reapplications(user_submissions_df, user_status_df):
    # Find the latest timestamp for each email
    user_submissions_df["timestamp"] = pd.to_datetime(
        user_submissions_df["timestamp"], format="%m/%d/%Y %H:%M:%S"
    )
    user_status_df["updated_at"] = pd.to_datetime(
        user_status_df["updated_at"], format="%m/%d/%Y %H:%M:%S"
    )
    latest_timestamps = (
        user_submissions_df.groupby("email")["timestamp"].max().reset_index()
    )

    # Merge the latest timestamps with user_status_df
    user_status_df = user_status_df.merge(
        latest_timestamps, on="email", how="left", suffixes=("", "_latest")
    )

    # Convert 'updated_at' and 'timestamp' columns to datetime
    # user_status_df[['updated_at', 'timestamp']] = user_status_df[['updated_at', 'timestamp']].apply(pd.to_datetime)

    if (user_status_df["timestamp"] < user_status_df["updated_at"]).all():
        update_flag = None
    else:
        update_flag = 1

    # Update 'swapped' and 'updated_at' columns based on the condition
    user_status_df["swapped"] = user_status_df.apply(
        lambda row: "no" if row["timestamp"] > row["updated_at"] else row["swapped"],
        axis=1,
    )
    user_status_df["updated_at"] = user_status_df.apply(
        lambda row: max(row["timestamp"], row["updated_at"]), axis=1
    )
    # Drop the last column
    user_status_df["updated_at"] = user_status_df["updated_at"].dt.strftime(
        "%m/%d/%Y %H:%M:%S"
    )
    user_status_df = user_status_df.iloc[:, :-1]
    return user_status_df, update_flag


def update_swapped_column(df, email_list):
    df.loc[df["email"].isin(email_list), "swapped"] = "yes"
    return df


def update_swap_status(_gc, df, sheet_key):
    try:
        # Open specific sheet
        gs = _gc.open_by_key(sheet_key)

        # Open specific tab within the sheet
        tab = gs.worksheet("user-status")

        set_with_dataframe(tab, df)

        return None

    except gspread.exceptions.APIError as e:
        print("Error accessing Google Sheets API:", e)
        return None
    except gspread.exceptions.WorksheetNotFound as e:
        print(f"Error: Worksheet not found, please create a new tab named:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None
