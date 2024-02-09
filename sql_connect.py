import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
host_IP = os.getenv('mysql_host')
db_user = os.getenv('mysql_user')
db_pw = os.getenv('mysql_pw')

print(host_IP)
print(db_user)
pharmacogenomics_db = mysql.connector.connect(
    host=f'{host_IP}',
    user=f'{db_user}',
    password=f'{db_pw}'
)
print("Connection ID:", pharmacogenomics_db.connection_id)

sql_sel_database = "USE pharmacogenomics_dev"
cursor = pharmacogenomics_db.cursor()
cursor.execute(sql_sel_database)

total_InChiKeys = []
sql = f"SELECT * pharmacogenomics_dev.refold_parameters;"

cursor = pharmacogenomics_db.cursor(buffered=True)
cursor.execute(sql)
pharmacogenomics_db.commit()
total_InChiKeys = cursor.fetchall()
print((total_InChiKeys))