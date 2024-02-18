import pyarrow.parquet as pq
import pandas as pd
from neo4j import GraphDatabase
import time


class DataLoader:

    def __init__(self, uri, user, password):
        """
        Connect to the Neo4j database and other init steps
        
        Args:
            uri (str): URI of the Neo4j database
            user (str): Username of the Neo4j database
            password (str): Password of the Neo4j database
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self.driver.verify_connectivity()


    def close(self):
        """
        Close the connection to the Neo4j database
        """
        self.driver.close()


    # Define a function to create nodes and relationships in the graph
    def load_transform_file(self, file_path):
        """
        Load the parquet file and transform it into a csv file
        Then load the csv file into neo4j

        Args:
            file_path (str): Path to the parquet file to be loaded
        """

        # Read the parquet file
        trips = pq.read_table(file_path)
        trips = trips.to_pandas()

        # Some data cleaning and filtering
        trips = trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount']]

        # Filter out trips that are not in bronx
        bronx = [3, 18, 20, 31, 32, 46, 47, 51, 58, 59, 60, 69, 78, 81, 94, 119, 126, 136, 147, 159, 167, 168, 169, 174, 182, 183, 184, 185, 199, 200, 208, 212, 213, 220, 235, 240, 241, 242, 247, 248, 250, 254, 259]
        trips = trips[trips.iloc[:, 2].isin(bronx) & trips.iloc[:, 3].isin(bronx)]
        trips = trips[trips['trip_distance'] > 0.1]
        trips = trips[trips['fare_amount'] > 2.5]

        # Convert date-time columns to supported format
        trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
        trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
        
        # Convert to csv and store in the current directory
        save_loc = "/var/lib/neo4j/import/" + file_path.split(".")[0] + '.csv'
        trips.to_csv(save_loc, index=False)

        # TODO: Your code here
        # COLUMNS: tpep_pickup_datetime, tpep_dropoff_datetime, PULocationID, DOLocationID, trip_distance, fare_amount

        session = self.driver.session()
        with open(save_loc, 'r') as f:
            next(f)
            for line in f:
                row = line.strip().split(",")
                node_query = f'''
                MERGE (pickup:Location {{name:  {int(row[2])}}})
                MERGE (dropoff:Location {{name: {int(row[3])}}})
                '''
                session.run(node_query)

                # datetime_format = "%Y-%m-%d %H:%M:%S"
                # time_obj = datetime.strptime(row[0], datetime_format)
                # pickup = time_obj.isoformat()
                # time_obj2 = datetime.strptime(row[1], datetime_format)
                # dropoff = time_obj2.isoformat()

                pickup_tuple = time.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                pickup_seconds = time.mktime(pickup_tuple)
                pickup_new = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(pickup_seconds))

                dropoff_tuple = time.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                dropoff_seconds = time.mktime(dropoff_tuple)
                dropoff_new = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(dropoff_seconds))


                relationship_query = f'''
                MATCH (pickup:Location{{name: {int(row[2])}}}), (dropoff:Location{{name: {int(row[3])}}})
                CREATE (pickup)-[relation:TRIP
                {{
                    distance: {float(row[4])}, 
                    fare: {float(row[5])}, 
                    pickup_dt: datetime("{pickup_new}"), 
                    dropoff_dt: datetime("{dropoff_new}") 
                }}
                ]->(dropoff)               
                '''
                session.run(relationship_query)        

def main():

    total_attempts = 10
    attempt = 0

    # The database takes some time to starup!
    # Try to connect to the database 10 times
    while attempt < total_attempts:
        try:
            data_loader = DataLoader("neo4j://localhost:7687", "neo4j", "project2phase1")
            data_loader.load_transform_file("yellow_tripdata_2022-03.parquet")
            data_loader.close()
            
            attempt = total_attempts

        except Exception as e:
            print(f"(Attempt {attempt+1}/{total_attempts}) Error: ", e)
            attempt += 1
            time.sleep(10)


if __name__ == "__main__":
    main()

