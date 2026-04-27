from langchain_core.tools import tool
from utils.field_validator import UserModel
import sqlite3


@tool("get_user_profile", args_schema=UserModel)
def get_user_profile(cc):
    """Use this tool when the user reports problems on its services, you must ask about his identification card number, it is required to start the service and validate his identification. This tool provides a full description of the user profile in the system. It will give you features such as the full name, the physical address, email, the contract or contracts the user has, the zone of those contracts and the routers they have"""
    with sqlite3.connect("telecom.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.name, u.email, u.address, c.id_contract, c.service_plan, z.zone_name, z.net_status, r.mac_address, r.status, r.current_ip
            FROM contracts c
            JOIN users u ON c.id_user = u.user_identification
            JOIN zones z ON c.id_zone = z.id_zone
            JOIN routers r ON c.id_contract = r.id_contract
            WHERE c.id_user = ?
        ''', (cc,))
        rows = cursor.fetchall()

        if(len(rows) == 0):
            return "There is no registered user with that identification. User must provide a valid identification number"

        if(len(rows) == 1):
            return f"The user {rows[0]['name']} with email {rows[0]['email']} has the plan:\n{rows[0]['service_plan']} with the contract ID: {rows[0]['id_contract']}, in the zone {rows[0]['zone_name']} with the net status of {rows[0]['net_status']} and with the information of the device: MAC {rows[0]['mac_address']} (Status: {rows[0]['status']})"
        
        if (len(rows) >1):
            partialStr = ""
            for index, row in enumerate(rows):
                partialStr = partialStr + f"{index+1}. {row['service_plan']} with the contract ID: {row['id_contract']}, in the zone {row['zone_name']} with the net status of {row['net_status']} and with the information of the device: MAC {row['mac_address']} (Status: {row['status']}) \n"
            return f"The user {rows[0]['name']} with email {rows[0]['email']} has the plans:\n{partialStr}"
