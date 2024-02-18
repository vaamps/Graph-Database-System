# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 5.5.0 installation and some cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# TODO: Complete the Dockerfile
# Downloading dataset, cloning and setting up code
WORKDIR /cse511
RUN apt-get update \
    && apt-get install -y git \
    && wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet \
    && git clone https://vaamps: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@github.com/CSE511-SPRING-2023/vamirap1-project-2.git \
    && cp -r vamirap1-project-2/data_loader.py /cse511/ \
    && rm -rf vamirap1-project-2 \
    && pip3 install pyarrow pandas neo4j 


# Configuring neo4j and setting up new password
RUN echo "server.default_listen_address=0.0.0.0" >> /etc/neo4j/neo4j.conf
ENV NEW_PASSWORD="project2phase1"
RUN echo "ALTER CURRENT USER SET PASSWORD FROM 'neo4j' TO '${NEW_PASSWORD}';" > change.cipher && neo4j start && sleep 30 && cat change.cipher | cypher-shell -d system -u neo4j -p neo4j --format plain && neo4j stop


# GDS Plugin setup
RUN wget https://graphdatascience.ninja/neo4j-graph-data-science-2.3.1.zip \
    && unzip neo4j-graph-data-science-2.3.1.zip \
    && echo "dbms.security.procedures.unrestricted=gds.*" >> /etc/neo4j/neo4j.conf \
    && mv neo4j-graph-data-science-2.3.1.jar /var/lib/neo4j/plugins/ \
    && rm neo4j-graph-data-science-2.3.1.zip

# Run the data loader script
RUN chmod +x /cse511/data_loader.py && \
    neo4j start && \
    python3 data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

# Start neo4j service and show the logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]
