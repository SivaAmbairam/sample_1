# import os
# import jaydebeapi
# import csv
# import datetime
#
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
# def push_csv_to_db(connection, csv_file_path, table_name):
#     try:
#         cursor = connection.cursor()
#
#         with open(csv_file_path, newline='') as csvfile:
#             csv_reader = csv.reader(csvfile)
#
#             headers = next(csv_reader)
#
#             placeholders = ','.join(['?'] * len(headers))
#             insert_query = f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})"
#
#             for row in csv_reader:
#                 cursor.execute(insert_query, row)
#         connection.commit()
#         cursor.close()
#
#         print("CSV file successfully uploaded to the database!")
#
#     except jaydebeapi.DatabaseError as e:
#         print("Error executing insert statement: ", e)
#
#     except Exception as e:
#         print("An error occurred: ", e)
#
#
# def update_timestamp(connection, table_name):
#     current_time = datetime.datetime.now()
#     formatted_time = current_time.strftime("%b %d %Y %I:%M%p")
#     print(formatted_time)
#
#     try:
#         cursor = connection.cursor()
#         update_query = f"""
#         UPDATE {table_name}
#         SET timestamp = '{formatted_time}'
#         WHERE timestamp IS NULL;
#         """
#         cursor.execute(update_query)
#         connection.commit()
#         print("Timestamp updated successfully!")
#
#         # Close the cursor and connection
#         cursor.close()
#
#     except jaydebeapi.DatabaseError as e:
#         print("Error executing update statement: ", e)
#
#     except Exception as e:
#         print("An error occurred: ", e)
#
#
# if __name__ == "__main__":
#     connection_file = 'db_connection_file.txt'
#     csv_file_path = [r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Flinn_Products.csv', r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Frey_Products.csv', r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Nasco_Products.csv', r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Carolina_Products.csv', r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\VWR_WARDS_Products.csv', r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Fisher_Products.csv', r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Wardsci_Products.csv']
#     table_name = ['FlinnCompetitors.Flinn_Products', 'FlinnCompetitors.Frey_Products', 'FlinnCompetitors.Nasco_Products', 'FlinnCompetitors.Carolina_Products', 'FlinnCompetitors.VWR_WARDS_Products', 'FlinnCompetitors.Fisher_Products', 'FlinnCompetitors.Wardsci_Products']
#
#     connection = get_connection(connection_file)
#     if connection:
#         push_csv_to_db(connection, csv_file_path, table_name)
#         update_timestamp(connection, table_name)
#         connection.close()


import os
import csv
import datetime
import jaydebeapi
import jpype
import chardet


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


def push_csv_to_db(connection, csv_file_path, table_name):
    try:
        cursor = connection.cursor()

        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)

            headers = next(csv_reader)

            placeholders = ','.join(['?'] * len(headers))
            insert_query = f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})"

            for row in csv_reader:
                cursor.execute(insert_query, row)

        connection.commit()
        cursor.close()

        print(f"CSV file '{csv_file_path}' successfully uploaded to the database!")

    except jaydebeapi.DatabaseError as e:
        print(f"Error executing insert statement for CSV '{csv_file_path}': {e}")

    except Exception as e:
        print(f"An error occurred for CSV '{csv_file_path}': {e}")


def update_timestamp(connection, table_name):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%b %d %Y %I:%M%p")
    print(f"Updating timestamp for table '{table_name}' at {formatted_time}")

    try:
        cursor = connection.cursor()
        update_query = f"""
        UPDATE {table_name}
        SET timestamp = '{formatted_time}'
        WHERE timestamp IS NULL;
        """
        cursor.execute(update_query)
        connection.commit()
        print(f"Timestamp updated successfully for table '{table_name}'")

        cursor.close()

    except jaydebeapi.DatabaseError as e:
        print(f"Error executing update statement for table '{table_name}': {e}")

    except Exception as e:
        print(f"An error occurred for table '{table_name}': {e}")


if __name__ == "__main__":
    connection_file = r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)/Scrapping Scripts/Output/temp/db_connection_file.txt'
    csv_file_paths = [
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Flinn_Products.csv',
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Frey_Products.csv',
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Nasco_Products.csv',
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Carolina_Products.csv',
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\VWR_WARDS_Products.csv',
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Fisher_Products.csv',
        r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Wardsci_Products.csv'
    ]
    table_names = [
        'FlinnCompetitors.Flinn_Products',
        'FlinnCompetitors.Frey_Products',
        'FlinnCompetitors.Nasco_Products',
        'FlinnCompetitors.Carolina_Products',
        'FlinnCompetitors.VWR_WARDS_Products',
        'FlinnCompetitors.Fisher_Products',
        'FlinnCompetitors.WardsScience_Products'
    ]

    connection = get_connection(connection_file)

    if connection:
        for csv_file_path, table_name in zip(csv_file_paths, table_names):
            push_csv_to_db(connection, csv_file_path, table_name)
            update_timestamp(connection, table_name)

        connection.close()
