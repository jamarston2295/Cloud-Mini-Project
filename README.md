Cloud-Mini-Project

Name: John Marston

Below are all the steps in creating my app.

Task 1: After creating an aws instance I had to set up my laptop to run this instance. To do this I installed putty and puttygen to convert my .pem file to a .ppk and run the instance using windows. I also installed an ubuntu app so I could use linux commands.

Task 2: I then created the file API_request.py, which retrieves stop and search data from the police API.

Task 3: The output from API_request.py was a JSON response of stop and search data and I converted this output to a csv file (stop_and_search.csv) and saved it in the home directory inside my aws instance. I added an ID column as the first column so each case had at least one unique element to it.

Task 4: Using the instructions from lab 10 I set up my Cassandra instance and stored my csv file using the following commands:
  - Create Cassandra instance (called project_container): sudo docker run --name project_container -p 9042:9042 -d cassandra:latest
  - Download csv file to Cassandra container image: wget -O stop_and_search.csv https://raw.githubusercontent.com/jamarston2295/Cloud-         Mini-Project/master/stop_and_search.csv
  - Copy data inside the container: sudo docker cp stop_and_search.csv project_container:/home/stop_and_search.csv
  - Edit data from CQL shell: sudo docker exec -it project_container cqlsh
  - Create table: CREATE TABLE stop_and_search_2.stats (ID int PRIMARY KEY, age_range text, datetime text, gender text, involved_person     boolean, legislation text, location_latitude decimal, location_longitude decimal, location_street_id int, location__street__name         text, object_of_search text, officer_defined_ethnicity text, operation boolean, operation_name text, outcome text,                       outcome_linked_to_object_of_search text, ect__id text, outcome_object__name text, removal_of_more_than_outer_clothing boolean,           self_defined_ethnicity text, type text);
  - Copy table contents from csv: COPY stop_and_search_2.stats(ID, age_range, datetime, gender, involved_person, legislation,               location_latitude, location_longitude, location_street_id, location__street__name, object_of_search, officer_defined_ethnicity,         operation, operation_name, outcome, outcome_linked_to_object_of_search, ect__id, outcome_object__name,                                   removal_of_more_than_outer_clothing, self_defined_ethnicity, type) FROM '/home/stop_and_search.csv' WITH DELIMITER=',' AND               HEADER=TRUE;
  
Task 5: I then used docker to build the container image using the following commands:
  - Build the image: sudo docker build . --tag=project_container:v1 
  - Run the container: sudo docker run -p 80:80 project_container:v1

Task 6: Following the guidance from the lab 10 manual I created my Dockerfile and requirements.txt, which were adjusted to specifically work for my code.

Task 7: I created my basic app CW.py, which is designed to perform a GET, POST, PUT and DELETE request by querying data from my stop and search table in Cassandra. The requests created are outlined below:
  - GET: Takes as argument an integer, ID, in the address bar (/id) and, if the id exists in the table, returns the id 
    number and the gender of the person for the specified id entry, or if the id doesn't exist will return an error message.
  - POST: Takes same argument as the GET request and if the id doesn't exist, creates the id along with a specified gender in the code,     otherwise returns an error.
  - PUT: Takes the id and gender (/id/gender) and will output a message containing the new id and gender specified, if the id           already exists, otherwise it should return an error.
  - DELETE: Takes the id as an argument and if it exists, it will delete the entry, otherwise an error message should appear.

Task 8: To test my code I used the following methods:
  - GET: http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/1 - should return successfully
         http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/64 - should return an error
  - POST: curl -X "POST" http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/64 - should create successfully
          curl -X "POST" http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/1 - should return error
  - PUT: curl -X "PUT" http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/1 - should create successfully
         curl -X "PUT" http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/65 - should return error
  - DELETE: curl -X "DELETE" http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/1 - should delete successfully
            curl -X "DELETE" http://ec2-18-215-235-173.compute-1.amazonaws.com/stop_and_search/65 - should return error
          
          
