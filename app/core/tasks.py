from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


@shared_task
def execute_mysql_query():
    print(os.environ.get('MYSQL_CA'))
    # SSL configuration
    ssl_config = {
        'ca': os.environ.get('MYSQL_CA'),
        'cert': os.environ.get('MYSQL_CERT'),
        'key': os.environ.get('MYSQL_KEY'),
    }

    # MySQL connection configuration
    config = {
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'host': os.environ.get('MYSQL_HOST'),
        'port': int(os.environ.get('MYSQL_PORT')),
        'database': os.environ.get('MYSQL_DATABASE'),
        'ssl_ca': ssl_config['ca'],
        'ssl_cert': ssl_config['cert'],
        'ssl_key': ssl_config['key'],
        'ssl_verify_cert': False,  # Verify server certificate
        'ssl_disabled': False,  # Enable SSL
    }

    # Create a connection
    cnx = mysql.connector.connect(**config)

    # Create a cursor
    cursor = cnx.cursor()

    # Execute a query
    query = "SELECT * FROM elegiveis_cv"
    cursor.execute(query)

    # Fetch and print the results
    for row in cursor:
        print(row)

    # Close cursor and connection
    cursor.close()
    cnx.close()

# @shared_task
# def execute_mysql_query():

#     # SSL configuration
#     ssl_config = {
#         'ca': '/home/xavier/Documents/certificado/ca.pem',
#         'cert': '/home/xavier/Documents/certificado/client-cert.pem',
#         'key': '/home/xavier/Documents/certificado/client-key.pem',
#     }

#     # MySQL connection configuration
#     config = {
#         'user': 'nXavier',
#         'password': 'Lun@rOrbit',
#         'host': 'epts-sofala.fgh.org.mz',
#         'port': 23307,
#         'database': 'aux_central_db',
#         'ssl_ca': ssl_config['ca'],
#         'ssl_cert': ssl_config['cert'],
#         'ssl_key': ssl_config['key'],
#         'ssl_verify_cert': False,  # Verify server certificate
#         'ssl_disabled': False,  # Enable SSL
#     }

#     # Create a connection
#     cnx = mysql.connector.connect(**config)

#     # Create a cursor
#     cursor = cnx.cursor()

#     # Execute a query
#     query = "SELECT * FROM elegiveis_cv"
#     cursor.execute(query)

#     # Fetch and print the results
#     for row in cursor:
#         print(row)

#     # Close cursor and connection
#     cursor.close()
#     cnx.close()
