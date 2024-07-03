# import jaydebeapi
# import os
# import datetime
# import csv
# from database import get_connection
#
# # CSV file path
# csv_file_path = r'C:\Users\G6\PycharmProjects\Web-Scrapping_v2\Test_script\Output\Flinn Products.csv'
#
# # SQL table details
# table_name = 'FlinnCompetitors.Product_Comparison'
#
#
# def push_csv_to_db(csv_file_path, table_name):
#     connection = get_connection()
#     if connection:
#         try:
#             cursor = connection.cursor()
#
#             # Open the CSV file
#             with open(csv_file_path, newline='') as csvfile:
#                 csv_reader = csv.reader(csvfile)
#
#                 # Skip the header row if your CSV has headers
#                 headers = next(csv_reader)
#
#                 # Prepare the insert query
#                 placeholders = ','.join(['?'] * len(headers))
#                 insert_query = f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})"
#
#                 # Insert each row from the CSV file into the database
#                 for row in csv_reader:
#                     cursor.execute(insert_query, row)
#
#             # Commit the transaction
#             connection.commit()
#
#             # Close the cursor and connection
#             cursor.close()
#             connection.close()
#
#             print("CSV file successfully uploaded to the database!")
#
#         except jaydebeapi.DatabaseError as e:
#             print("Error executing insert statement: ", e)
#
#         except Exception as e:
#             print("An error occurred: ", e)
#
#
# def update_timestamp(table_name):
#     current_time = datetime.datetime.now()
#
#     formatted_time = current_time.strftime("%b %d %Y %I:%M%p")
#     print(formatted_time)
#     connection = get_connection()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             update_query = f"""
#             UPDATE {table_name}
#             SET timestamp = '{formatted_time}'
#             WHERE timestamp IS NULL;
#             """
#             cursor.execute(update_query)
#             connection.commit()
#             print("Timestamp updated successfully!")
#
#             # Close the cursor and connection
#             cursor.close()
#             connection.close()
#
#         except jaydebeapi.DatabaseError as e:
#             print("Error executing update statement: ", e)
#
#         except Exception as e:
#             print("An error occurred: ", e)
#
#
# if __name__ == "__main__":
#     push_csv_to_db(csv_file_path, table_name)
#     update_timestamp(table_name)

import os
import jaydebeapi
import csv
import datetime
import jpype


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

        print("CSV file successfully uploaded to the database!")

    except jaydebeapi.DatabaseError as e:
        print("Error executing insert statement: ", e)

    except Exception as e:
        print("An error occurred: ", e)


def update_timestamp(connection, table_name):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%b %d %Y %I:%M%p")
    print(formatted_time)

    try:
        cursor = connection.cursor()
        update_query = f"""
        UPDATE {table_name}
        SET timestamp = '{formatted_time}'
        WHERE timestamp IS NULL;
        """
        cursor.execute(update_query)
        connection.commit()
        print("Timestamp updated successfully!")

        # Close the cursor and connection
        cursor.close()

    except jaydebeapi.DatabaseError as e:
        print("Error executing update statement: ", e)

    except Exception as e:
        print("An error occurred: ", e)


if __name__ == "__main__":
    connection_file = 'Scrapping Scripts/Output/temp/db_connection_file.txt'
    csv_file_path = r'D:\svc_webscrape\Webscrapping- Webpage V2.2 (WebSocket)\Webscrapping- Webpage V2.2 (WebSocket)\Scrapping Scripts\Output\Master_Matched_Products.csv'
    table_name = 'FlinnCompetitors.Product_Comparison'

    connection = get_connection(connection_file)
    if connection:
        push_csv_to_db(connection, csv_file_path, table_name)
        update_timestamp(connection, table_name)
        connection.close()
