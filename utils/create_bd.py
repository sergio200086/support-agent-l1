import _sqlite3


conn = _sqlite3.connect("telecom.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

def creation():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_identification INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL 
        )        
''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zones(
            id_zone INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_name TEXT NOT NULL,
            net_status TEXT NOT NULL    
        )
''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts(
            id_contract INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_zone INTEGER NOT NULL,
            service_plan TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES users(user_identification),
            FOREIGN KEY (id_zone) REFERENCES zones(id_zone)
        )
''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routers(
            mac_address TEXT PRIMARY KEY,
            id_contract INTEGER NOT NULL,
            brand TEXT NOT NULL,
            status TEXT NOT NULL,
            current_ip TEXT NOT NULL,
            FOREIGN KEY (id_contract) REFERENCES contracts(id_contract)
        )
''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets(
            id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contract INTEGER NOT NULL,
            creation_date DATE NOT NULL,
            problem TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (id_contract) REFERENCES contracts(id_contract)
        )
''')
    

def insert_data_user(id, name, email, address):
    user_data = (id, name, email, address)
    cursor.execute('''
        INSERT OR IGNORE INTO users (
            user_identification,
            name,
            email,
            address
        )
        VALUES (?,?,?,?)
''', user_data)
    
def insert_zone(zone_name, net_status):
    zone_data = (zone_name, net_status)
    cursor.execute('''
        INSERT INTO zones (zone_name, net_status)
        VALUES (?,?)
    ''', zone_data)
 
def insert_contract(id_user, id_zone, service_plan, status):
    contract_data = (id_user, id_zone, service_plan, status)
    cursor.execute('''
        INSERT INTO contracts (id_user, id_zone, service_plan, status)
        VALUES (?,?,?,?)
    ''', contract_data)
    return cursor.lastrowid
 
def insert_router(mac_address, brand, status, current_ip, id_contract):
    router_data = (mac_address, brand, status, current_ip, id_contract)
    cursor.execute('''
        INSERT INTO routers (mac_address, brand, status, current_ip, id_contract)
        VALUES (?,?,?,?,?)
    ''', router_data)




def get_all_user_data():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def get_all_zones():
    print("\n=== ZONES ===")
    cursor.execute("SELECT * FROM zones")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
 
def get_all_contracts():
    print("\n=== CONTRACTS ===")
    cursor.execute('''
        SELECT c.id_contract, u.name, z.zone_name, c.service_plan, c.status
        FROM contracts c
        JOIN users u ON c.id_user = u.user_identification
        JOIN zones z ON c.id_zone = z.id_zone
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
 
def get_all_routers():
    print("\n=== ROUTERS ===")
    cursor.execute('''
        SELECT r.mac_address, r.brand, r.status, r.current_ip, c.id_contract
        FROM routers r
        JOIN contracts c ON r.id_contract = c.id_contract
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


creation()
conn.commit()
insert_data_user(1000765543, "Alejandro Gonzalez", "alejandro@gmail.com", "cra 12 # 64 -109")
insert_data_user(1000987336, "Sergio suarez", "sergio@gmail.com", "cra 89 # 72 -1")
insert_data_user(1000654321, "Maria Rodriguez", "maria@gmail.com", "cra 45 # 23 -15")
insert_data_user(1000456789, "Carlos Martinez", "carlos@gmail.com", "cra 78 # 91 -22")
conn.commit()
 
insert_zone("North Zone", "active")
insert_zone("Center Zone", "active")
insert_zone("South Zone", "active")
conn.commit()
 
contract_1 = insert_contract(1000765543, 1, "100M Basic", "active")
conn.commit()
 
contract_2 = insert_contract(1000987336, 1, "200M Plus", "active")
conn.commit()
 
contract_3 = insert_contract(1000654321, 2, "400M Extra", "active")
conn.commit()
 
contract_4 = insert_contract(1000456789, 3, "1Gb Pro", "active")
conn.commit()
 
contract_5 = insert_contract(1000987336, 3, "1Gb Pro", "active")
conn.commit()
 
insert_router("AA:BB:CC:DD:EE:01", "TP-Link", "active", "192.168.1.1", contract_1)
 
insert_router("AA:BB:CC:DD:EE:02", "Cisco", "active", "192.168.1.2", contract_2)
 
insert_router("AA:BB:CC:DD:EE:03", "Netgear", "active", "192.168.2.1", contract_3)
 
insert_router("AA:BB:CC:DD:EE:04", "Arista", "active", "192.168.3.1", contract_4)
 
insert_router("AA:BB:CC:DD:EE:05", "Juniper", "active", "192.168.3.2", contract_5)
conn.commit()
 
get_all_user_data()
get_all_zones()
get_all_contracts()
get_all_routers()
 
conn.close()
print("\n✅ Base de datos creada y poblada exitosamente!")