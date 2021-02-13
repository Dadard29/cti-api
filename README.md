# CTI API

This API can be used to extract data from the Mitre STIX repository, and format this data to JSON.

This JSON can be imported to an ArangoDB database.

The controllers in this API can be used to access this ArangoDB database.

## Docs

### Data extraction

The extract script uses the package [attackcti](https://attackcti.readthedocs.io/en/latest/) to access the STIX data.

### Controllers documentation

The API is documented on [Postman](https://documenter.getpostman.com/view/7424587/TWDRtLFb).

### Database

The API uses the community driver [python-arango](https://github.com/Joowani/python-arango).

The objects are stored in 3 collections:
- `groups`
- `tools`
- `techniques`

The edges connecting those are stored in 2 collections:
- `group_tools` connects `groups` to `tools` objects.
- `tool_techniques` connects `tools` to `techniques` objects.

The edges are unidirectional.


## Usage

### Database

I used Docker for the database. Set the `<path-to-host>` variable to make the database data persistent.
```
docker pull arangodb:latest
docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -d --name arangodb -p 8529:8529 -v <path-to-host-db>:/var/lib/arangodb3 arangodb
docker logs arangodb
```
Retrieve the root password generated randomly from the logs.
At this point, the database is empty.
You can access the database panel from your browser at `http://localhost:8529`.
You'll need to extract data from the STIX repository with the `/extract` scripts.
Then, you'll have to import the extracted data to the database.
You can use the [arangoimport](https://www.arangodb.com/docs/stable/programs-arangoimport.html) utility.

### Libraries
Install the required packages:
```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Setup the environment
```
export ARANGO_ROOT_PASSWORD=<db-root-password>
```

### Run
Run the API
```
python main.py
```
