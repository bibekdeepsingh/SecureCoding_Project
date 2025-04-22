"""
Description: A program that reads through transaction records and reports the results.
Author: ACE Faculty
Edited by: Bibekdeep Singh
Date: 06/03/2024
Usage: This program will read transaction data from a .csv file, summarize and 
report the results.
"""

import csv
import os

# Constant
VALID_TRANSACTION_TYPES = ['deposit', 'withdraw']


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_transactions(file_path):
    customer_data = {}
    rejected_records = []
    total_transaction_amount = 0
    transaction_count = 0

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Skip header

            for row in reader:
                is_valid = True
                error_message = ''

                # Validate number of columns
                if len(row) < 3:
                    rejected_records.append((row, "Missing fields in record."))
                    continue

                customer_id = row[0].strip()
                transaction_type = row[1].strip().lower()

                # VALIDATION 1: Check transaction type
                if transaction_type not in VALID_TRANSACTION_TYPES:
                    is_valid = False
                    error_message += "Invalid transaction type. "

                # VALIDATION 2: Check if amount is numeric
                try:
                    transaction_amount = float(row[2])
                    if transaction_amount < 0:
                        is_valid = False
                        error_message += "Negative transaction amount. "
                except ValueError:
                    is_valid = False
                    error_message += "Non-numeric transaction amount. "

                # PROCESS VALID RECORDS
                if is_valid:
                    if customer_id not in customer_data:
                        customer_data[customer_id] = {'balance': 0, 'transactions': []}

                    if transaction_type == 'deposit':
                        customer_data[customer_id]['balance'] += transaction_amount
                    elif transaction_type == 'withdraw':
                        customer_data[customer_id]['balance'] -= transaction_amount

                    customer_data[customer_id]['transactions'].append((transaction_amount, transaction_type))
                    transaction_count += 1
                    total_transaction_amount += transaction_amount
                else:
                    rejected_records.append((row, error_message.strip()))

    except FileNotFoundError:
        print(f"ERROR: File '{file_path}' not found.")
    except Exception as e:
        print(f"ERROR: {e}")

    return customer_data, rejected_records, total_transaction_amount, transaction_count


def print_report(customer_data, total_transaction_amount, transaction_count):
    print("PiXELL River Transaction Report\n===============================\n")

    for customer_id, data in customer_data.items():
        balance = data['balance']
        print(f"Customer ID: {customer_id}")
        print(f"Balance: ${balance:,.2f}")
        print("Transaction History:")
        for amount, trans_type in data['transactions']:
            print(f"\t{trans_type.capitalize()}: ${amount:,.2f}")
        print()

    if transaction_count > 0:
        avg = total_transaction_amount / transaction_count
        print(f"\nAVERAGE TRANSACTION AMOUNT: ${avg:,.2f}")
    else:
        print("\nNo valid transactions to calculate average.")


def print_rejected_records(rejected_records):
    print("\nREJECTED RECORDS\n================")
    if not rejected_records:
        print("No rejected records.")
    else:
        for row, error in rejected_records:
            print("REJECTED:", row, "| Reason:", error)


# === MAIN EXECUTION ===
clear_console()
file_path = 'bank_data_copy.csv'

customer_data, rejected_records, total_amount, trans_count = read_transactions(file_path)
print_report(customer_data, total_amount, trans_count)
print_rejected_records(rejected_records)
