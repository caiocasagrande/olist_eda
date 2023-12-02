

# Importing libraries
import sqlite3
import pandas   as pd

# Setting database path
db_path = '../../data/raw/db_olist.sqlite'

# Creating a connection to the database
connection = sqlite3.connect(db_path)

# Using SQL to join the tables
query = '''
    SELECT 
        oi.order_id                         AS order_id,
        oi.order_item_id                    AS order_item_id,
        oi.price                            AS price,
        oi.freight_value                    AS freight_value,
        p.product_id                        AS product_id,
        p.product_category_name             AS product_category,
        op.payment_type                     AS payment_type,
        op.payment_value                    AS payment_value,
        op.payment_installments             AS installments,
        orv.review_score                    AS review_score,
        o.order_status                      AS order_status,
        o.order_purchase_timestamp          AS order_purchase,
        o.order_approved_at                 AS approved_at,
        o.order_delivered_customer_date     AS delivered_at_customer,
        c.customer_id                       AS customer_id,
        c.customer_city                     AS customer_city,
        c.customer_state                    AS customer_state
    FROM 
        order_items AS oi   INNER JOIN products AS p        ON (oi.product_id = p.product_id)
                            INNER JOIN order_payments AS op ON (oi.order_id = op.order_id)
                            INNER JOIN order_reviews AS orv ON (oi.order_id = orv.order_id)
                            INNER JOIN orders AS o          ON (oi.order_id = o.order_id)
                            INNER JOIN customer AS c        ON (o.customer_id = c.customer_id);
'''

# Executing the query and reading the result into a DataFrame
dataset = pd.read_sql_query(query, connection)

# Closing the database connection
connection.close()

# The DataFrame contains the result of the SQL join 

# Exporting the DataFrame to a CSV file
dataset.to_csv('../../data/interim/olist_dataset.csv', index=False)
