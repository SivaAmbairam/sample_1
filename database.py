# # db_connection.py
#
# import jaydebeapi
# import os
#
# # import jpype
# # jvm_path = r"C:\Program Files\Java\jdk-22\bin\server\jvm.dll"
# # jpype.startJVM(jvm_path)
#
# # Parameterize the connection details at the top of the script
# server = 'FSI-FSQL3-PROD'
# database = 'FlinnWebPriceDW'
# username = 'svc_webscrape'
# password = 'A9wCQKVPNLzm!d$AC$fY'
# domain = 'fsi'
#
# jdbc_driver_dir = r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Drivers\sqljdbc_12.6.3.0_enu\sqljdbc_12.6\enu\jars'
# jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
# jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
# jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
#
# # jdbc_driver_dir = r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Drivers\sqljdbc_12.6.3.0_enu\sqljdbc_12.6\enu\jars'
# # jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
# # jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
# # jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
#
# # JDBC connection URL
# connection_url = f'jdbc:sqlserver://{server};databaseName={database};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'
#
# # Additional connection properties
# connection_properties = {
#     'user': f'{username}',
#     'password': password,
#     'integratedSecurity': 'true',
#     'authenticationScheme': 'NTLM',
#     'domain': domain
# }
#
#
# def get_connection():
#     try:
#         connection = jaydebeapi.connect(
#             jdbc_driver_class,
#             connection_url,
#             connection_properties,
#             [jdbc_driver_path]
#         )
#         return connection
#     except jaydebeapi.DatabaseError as e:
#         print("Error connecting to the database: ", e)
#         return None
#
#
# def test_connection():
#     connection = get_connection()
#     if connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT @@version;")
#         row = cursor.fetchone()
#         while row:
#             print(row[0])
#             row = cursor.fetchone()
#         cursor.close()
#         connection.close()
#         print("Connection successful!")
#
#
# if __name__ == "__main__":
#     test_connection()


import jaydebeapi
import os
import jpype

# Parameterize the connection details at the top of the script
server = 'FSI-FSQL3-PROD'
database = 'FlinnWebPriceDW'
username = 'svc_webscrape'
password = 'A9wCQKVPNLzm!d$AC$fY'
domain = 'fsi'

# Set the JAVA_HOME environment variable programmatically
os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-22"
jvm_path = os.path.join(os.environ['JAVA_HOME'], 'bin', 'server', 'jvm.dll')

jdbc_driver_dir = r'C:\Program Files\sqljdbc_12.6\enu\jars'
jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'

# Add the JDBC driver JAR to the JVM classpath
jpype.startJVM(jvm_path, f"-Djava.class.path={jdbc_driver_path}")

# JDBC connection URL
connection_url = f'jdbc:sqlserver://{server};databaseName={database};encrypt=true;trustServerCertificate=true;integratedSecurity=false;'

# Additional connection properties
connection_properties = {
    'user': username,
    'password': password,
    'integratedSecurity': 'true',
    'authenticationScheme': 'NTLM',
    'domain': domain
}

def get_connection():
    try:
        connection = jaydebeapi.connect(
            jdbc_driver_class,
            connection_url,
            connection_properties
        )
        return connection
    except jaydebeapi.DatabaseError as e:
        print("Error connecting to the database: ", e)
        return None


def test_connection():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()
        cursor.close()
        connection.close()
        print("Connection successful!")


if __name__ == "__main__":
    test_connection()


