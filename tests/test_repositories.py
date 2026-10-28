import sqlite3
import os
import sys
from data.database_manager import ConnectionManager
from data.repositories.complaint_repository import ComplaintRepository
from data.repositories.customer_repository import CustomerRepository
from data.repositories.account_repository import AccountRepository

# REPOSITORY FUNCTIONS TO TEST:
# Test valid, missing, and failure cases
# 
# CustomerRepository.get_by_id(id)
#
# AccountRepository.get_for_customer(customer_id)
#
# ComplaintRepository.get_by_id(id)
# ComplaintRepository.get_for_customer(customer_id)
# ComplaintRepository.create(...)


def main():
    connection = ConnectionManager()
    customer = CustomerRepository(connection)
    account = AccountRepository(connection)
    complaint = ComplaintRepository(connection)

    print("Test 1: valid Customer get_by_id")
    try:
        cus_id = "CUS001"
        result = customer.get_by_id(cus_id)

        assert result is not None
        print("\tT1 Contains something?")
        assert result[0] == "CUS001"
        print("\tT1 is CUS001 - PASS!")
    except:
        print("Test 1 Failed\n")

    print("Test 2: customer DNE")
    try:
        cus_id = "CUS999"
        result = customer.get_by_id(cus_id)

        assert result is not None
        print("\tT2 Contains something")
        assert result[0] == "CUS999"
        print("\tT2 is CUS999 - FAIL!")
    except:
        print("\tTest 2 pass.")

    print("Test 3: customer invalid id type")
    try:
        bad_customer = CustomerRepository(None)
        bad_customer.get_by_id("CUS001")

        print("\tTest 3 fail")
    except:
        print("\tTest 3 pass")

    print("Test 4: valid Account get_for_customer")
    try:
        cus_id = "CUS001"
        result = account.get_for_customer(cus_id)

        assert result is not None
        assert len(result) > 0
        for acct in result:
            assert acct[1] == "CUS001"
        print("\t Test 4 pass")
    except:
        print("Test 4 failed")

    print("Test 5: Account.Cust does not exist")
    try:
        cus_id = "CUS999"
        result = account.get_for_customer(cus_id)

        assert result is not None
        assert len(result) > 0
        for acct in result:
            assert acct[1] == "CUS999"
        print("\t Test 5 fail")
    except:
        print("\tTest 5 pass")

    print("Test 6: Account invalid customer id type")
    try:
        bad_account = AccountRepository(None)
        bad_account.get_for_customer("CUS001")

        print("\tTest 6 fail")
    except:
        print("\tTest 6 pass")

    print("Test 7 valid Complaint id")
    try:
        comp_id = "CMP001"
        result = complaint.get_by_id(comp_id)

        assert result is not None
        assert result[0] == "CMP001"
        print("\tTest7 pass")
    except:
        print("\tTest 7 failed")

    print("Test 8 Complaint id DNE")
    try:
        comp_id = "CMP999"
        result = complaint.get_by_id(comp_id)

        assert result is not None
        assert result[0] == "CMP999"
        print("\tTest 8 failed")
    except:
        print("\tTest 8 pass")

    print("Test 9: Complaint invalid id type")
    try:
        bad_complaint = ComplaintRepository(None)
        bad_complaint.get_by_id("CMP001")

        print("\tTest 9 fail")
    except:
        print("\tTest 9 pass")

    print("Test 10 Complaint Get Valid CUS id")
    try:
        cus_id = "CUS001"
        result = complaint.get_for_customer(cus_id)

        assert result is not None
        assert len(result) > 0
        for complaint in result:
            assert complaint[1] == "CUS001"
        print("\tTest 10 Passed")
    except:
        print("\tTest 10 failed")

    print("Test 11 Complaint Get CUS id DNE")
    try:
        cus_id = "CUS999"
        result = complaint.get_for_customer(cus_id)

        assert result is not None
        assert len(result) > 0
        for complaint in result:
            assert complaint[1] == "CUS999"
        print("\tTest 11 failed")
    except:
        print("\tTest 11 passed")

    print("Test 12: Complaint invalid customer id type")
    try:
        result = complaint.get_for_customer(None)

        print("\tTest 12 fail")
    except:
        print("\tTest 12 pass")

    print("Test 13 Complaint Create")
    compCreate = ComplaintRepository(connection)
    try:

        compCreate.create("CMP300", "CUS001", "ACC001", "Phone", "Service Delay", "Delay in account update", "Medium", "OPEN", "2025-01-01", "EMP001")
        result = compCreate.get_by_id("CMP300")

        assert result is not None
        assert result[0] == "CMP300"
        print("\t Test13 Pass")
    except Exception as e:
        print("\tTest13 fail")
        print(type(e))
        print(e)

    print("Test 14 Complaint Create Uniqueness")
    try:

        compCreate.create("CMP255", "CUS001", "ACC001", "Phone", "Service Delay", "Delay in account update", "Medium", "OPEN", "2025-01-01", "EMP001")
        result = compCreate.get_by_id("CMP255")

        assert result is not None
        assert result[0] == "CMP255"
        print("\t Test14 Fail")
    except:
        print("\tTest14 pass")

    print("test 15 Complaint Create Empty")
    try:
        compCreate.create()
        result = compCreate.get_by_id()
        assert result is not None
        print("\tTest 15 Fail")
    except:
        print("\tTest 15 pass")

main()