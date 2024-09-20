# baseball-card-website
baseball card website


Start a docker container. Open terminal. Change dir to scripts.

get dynamodb container

scripts python3 -m venv venv 
➜  scripts source venv/bin/activate
(venv) ➜  scripts python3 list_tables.py 

create_table_new.py
list table
read_excel_import_dynamo
add gsi to dynamo
run script for new backend api -  change port to 5001 as 5000 is used by MAC
http://localhost:3000/

http://localhost:3000/api/cards


for data persistence:
	1.	Find where your database stores data in the container (e.g., /var/lib/mysql for MySQL, /var/lib/postgresql/data for PostgreSQL).
	2.	Create and run the container with a volume:

docker run -d \
--name your_container_name \
-v /path/on/host:/path/in/container \
your_image