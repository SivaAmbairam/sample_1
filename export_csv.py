# import csv
# import os
# import jaydebeapi
# import datetime
#
# def read_connection_details(file_path):
#     connection_details = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             key, value = line.strip().split(': ')
#             connection_details[key.strip()] = value.strip()
#     return connection_details
#
#
# def get_connection(connection_file):
#     try:
#         connection_details = read_connection_details(connection_file)
#
#         username = connection_details.get('user-name')
#         password = connection_details.get('password')
#         schema = connection_details.get('schema')
#
#         jdbc_driver_dir = r'C:\Users\G6\Downloads\sqljdbc_12.6\enu\jars'
#         jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
#         jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
#         jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
#
#         server = 'FSI-FSQL3-PROD'
#         connection_url = f'jdbc:sqlserver://{server};databaseName={schema};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'
#
#         connection_properties = {
#             'user': username,
#             'password': password,
#             'integratedSecurity': 'true',
#             'authenticationScheme': 'NTLM',
#             'domain': 'fsi'
#         }
#
#         connection = jaydebeapi.connect(
#             jdbc_driver_class,
#             connection_url,
#             connection_properties,
#             [jdbc_driver_path]
#         )
#
#         return connection
#
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         return None
#
#
# def export_to_csv(query, csv_file_path, connection):
#     if connection:
#         cursor = None
#         try:
#             cursor = connection.cursor()
#             cursor.execute(query)
#             rows = cursor.fetchall()
#             column_names = [desc[0] for desc in cursor.description]
#             with open(csv_file_path, mode='w', newline='') as csvfile:
#                 csv_writer = csv.writer(csvfile)
#                 csv_writer.writerow(column_names)
#                 csv_writer.writerows(rows)
#             print(f"Data successfully exported to {csv_file_path}")
#             cursor.close()
#             connection.close()
#         except jaydebeapi.DatabaseError as e:
#             print("Error executing query: ", e)
#         except Exception as e:
#             print("An error occurred: ", e)
#         finally:
#             if cursor:
#                 try:
#                     cursor.close()
#                 except jaydebeapi.Error as e:
#                     print(f"Error closing cursor: {e}")
#             if connection:
#                 try:
#                     connection.close()
#                 except jaydebeapi.Error as e:
#                     print(f"Error closing connection: {e}")
#
#
# if __name__ == "__main__":
#     connection_file = 'Output/temp/db_connection_file.txt'
#     connection = get_connection(connection_file)
#     if connection:
#         query = "SELECT * FROM FlinnCompetitors.Product_Comparison_Manual"
#         # export_csv_file_path = 'Scrapping Scripts/Output/Product_Comparison_Manual_export.csv'
#         export_csv_file_path = 'Output/Product_Comparison_Manual_export.csv'
#         export_to_csv(query, export_csv_file_path, connection)
#
#         connection.close()

import csv
import os
import jaydebeapi
import jpype
import datetime

def read_connection_details(file_path):
    connection_details = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            connection_details[key.strip()] = value.strip()
    return connection_details

def get_connection(connection_file):
    try:
        connection_details = read_connection_details(connection_file)

        username = connection_details.get('user-name')
        password = connection_details.get('password')
        schema = connection_details.get('schema')

        os.environ['JAVA_HOME'] = r"C:\Program Files\Java\jdk-22"
        jvm_path = os.path.join(os.environ['JAVA_HOME'], 'bin', 'server', 'jvm.dll')

        jdbc_driver_dir = r'C:\Program Files\sqljdbc_12.6\enu\jars'
        jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
        jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
        jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'

        # Add the JDBC driver JAR to the JVM classpath
        jpype.startJVM(jvm_path, f"-Djava.class.path={jdbc_driver_path}")

        server = 'FSI-FSQL3-PROD'
        connection_url = f'jdbc:sqlserver://{server};databaseName={schema};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'

        connection_properties = {
            'user': username,
            'password': password,
            'integratedSecurity': 'true',
            'authenticationScheme': 'NTLM',
            'domain': 'fsi'
        }

        connection = jaydebeapi.connect(
            jdbc_driver_class,
            connection_url,
            connection_properties,
            [jdbc_driver_path]
        )

        return connection

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def export_to_csv(query, csv_file_path, connection):
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        with open(csv_file_path, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(column_names)
            csv_writer.writerows(rows)
        print(f"Data successfully exported to {csv_file_path}")
    except jaydebeapi.DatabaseError as e:
        print("Error executing query: ", e)
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        if cursor:
            try:
                cursor.close()
            except jaydebeapi.Error as e:
                print(f"Error closing cursor: {e}")
        if connection:
            try:
                connection.close()
            except jaydebeapi.Error as e:
                print(f"Error closing connection: {e}")


if __name__ == "__main__":
    connection_file = r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)/Scrapping Scripts/Output/temp/db_connection_file.txt'
    connection = get_connection(connection_file)
    if connection:
        query = "SELECT * FROM FlinnCompetitors.Product_Comparison_Manual"
        export_csv_file_path = r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)/Scrapping Scripts/Output/Product_Comparison_Manual_export.csv'
        export_to_csv(query, export_csv_file_path, connection)
