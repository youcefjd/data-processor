# data-processor


## Architecture Overview 
The data-processor service consumes messages from the user-login topic, processes them, and writes the results to two separate topics: processed-logins and user-aggregations.

data-processor: This is a Python application that reads messages from the user-login topic, processes the data (ex: aggregation), and writes processed data to other topics (processed-logins and user-aggregations).
Kafka Consumer and Producer: The Python application uses Kafka consumers to read messages and producers to send data to new topics.

##### Key Points:
###### Consumer: Reads messages from user-login, processes the data, and sends results to the processed-logins and user-aggregations topics.
###### Producer: Sends the processed and aggregated data to Kafka topics, making it available for other consumers.
###### Aggregation: The Python service performs simple aggregation, such as counting the number of logins per user.


## Production Deployment Considerations

#### At Least 3 Brokers in 3 Different AZs:
In a production environment, to ensure high availability and fault tolerance, it's very important to deploy Kafka brokers across at least 3 availability zones. This helps to avoid single points of failure and ensures that your Kafka cluster can withstand the failure of an entire AZ.
This also allows Kafka to replicate data across brokers in different AZs, providing data durability and availability.

#### Use of More Robust Infrastructure for Data Processing (Apache Flink or kSQL):
While a simple Python consumer-producer setup works for small-scale applications, in a production-grade setup, you’ll want a more robust data processing infrastructure like Apache Flink or kSQL.
These tools offer streaming analytics at scale, are fault-tolerant, and support advanced operations.

#### Consider Connect Instead of Python Producers/Consumers:

Kafka Connect simplifies clients' deployment - JSON files are easier to understand particularly for non-technical people compared to Python (or any other programming language) clients. The Connect infrastructure can also scale horizontally if set up correctly. 

#### Multiple Partitions per Topic:
Kafka allows topics to be divided into multiple partitions, which enables parallelism in message consumption. Each partition can be consumed by a different consumer in a consumer group.
Using multiple partitions per topic increases throughput and ensures that the data is distributed evenly across Kafka brokers.

### Additional Scaling Considerations
#### Replication Factor:
In a production environment, each topic should have a replication factor of at least 3. This ensures that messages are replicated across multiple brokers, providing data redundancy.

#### Monitor and Auto-Scale:
Implement monitoring of Kafka brokers, producers, and consumers. Tools like Prometheus or Datadog can be used to track key metrics (ex: message throughput, consumer lag, disk usage).

#### Secure the Infrastructure:
Ensure encrypted communication between Kafka brokers (via TLS) and authentication.
Secure consumer-producer interactions via SSL/TLS or client authentication to prevent unauthorized access to Kafka topics.




<img width="1585" alt="Screenshot 2024-12-15 at 5 33 47 PM" src="https://github.com/user-attachments/assets/ce199adf-c691-46dc-9f83-bff1fb2385b7" />
<img width="941" alt="Screenshot 2024-12-15 at 5 34 26 PM" src="https://github.com/user-attachments/assets/10d900ef-123d-4a04-b9f5-c7cbaafd79bf" />



