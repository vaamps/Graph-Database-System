# Graph Database System with Neo4j

## Tools Utilized:
- Neo4j
- Docker
- Kubernetes (minikube)
- Python
- Helm

This project revolves around leveraging a Graph Database system using Neo4j. Through this endeavor, I acquired knowledge on creating fundamental components such as Nodes, Relationships, and Graphs. Additionally, the project implements and validates two algorithms:

- Page Rank algorithm
- Breadth First Search (BFS) algorithm

## Project Workflow:
- Dockerfile updates facilitate the download of essential files, setup, and data loading into Neo4j. Additionally, it configures the GDS plugin.
- The interface python script is enhanced to create two Graph objects, one for each algorithm.
- The tester python script is employed to assess the implementation against provided test cases.

To execute and evaluate the project implementation, follow these commands:

> docker build -t <image_name>:<image_tag> . 

> docker run -itd -p 7474:7474 -p 7687:7687 <image_name>:<image_tag>

This command launches the Neo4j database on the local system with specified ports. Port 7474 handles HTTP requests to the database, while port 7687 utilizes the _bolt_ protocol for TCP connections.

To validate the project implementation, execute the following command:

> python3 tester.py

This command tests the implemented functionalities against predefined test cases.
