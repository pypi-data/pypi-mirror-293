import sdb_connector as sdb_connector
import time
import pandas as pd


start = time.time()
result = sdb_connector.select_measurement_data_with_db_connect("192.168.2.63", "8000", 
                "root", "root","main", "data", "amv_tag_49", "run_info:01J4XRFVTY9XSBCECW2NHWHMGK")


# Display the DataFrame
#print(df)
end = time.time()
print("Time taken for data: ", end - start)