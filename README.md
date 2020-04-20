Cloud-Mini-Project

Below are all the steps in creating my app.

Task 1: After creating an aws instance I had to set up my laptop to run this instance. To do this I installed putty and puttygen to convert my .pem file to a .ppk and run the instance using windows. I also installed an ubuntu app so I could use linux commands.

Task 2: I then created the file API_request.py, which retrieves stop and search data from the police API.

Task 3: The output from API_request.py was a JSON response of stop and search data and I converted this output to a csv file (stop_and_search.csv) and saved it in the home directory inside my aws instance.

Task 4: Using the instructions from lab 10 I set up my Cassandra instance and stored my csv file using the following commands:
  - Create Cassandra instance (called project_container): sudo docker run --name project_container -p 9042:9042 -d cassandra:latest
  - Download csv file to Cassandra container image: wget -O stop_and_search.csv 
