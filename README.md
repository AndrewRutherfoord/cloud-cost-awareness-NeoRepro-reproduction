# Cloud Cost Awareness - Replication Package

This repository contains supplementary material for the paper entitled:

**Mining Cost Awareness in the Deployments of Cloud-based Applications**

All data in this package originally comes from <https://github.com/feitosa-daniel/cloud-cost-awareness>
This replication package only contains the data for commits.

Once you run the application you will find:

- Configuration files that were used to drill the original Repository Data into the Neo4j Database
- Database dumps at different stages of the study which can be loaded and queried
- Scripts to load the labelled dataset onto Neo4j

> **Note**: This application is designed to be run on a local machine. No considerations of network
> security were made for public accessibility.

## Executing the Project

This project is built with Docker and must be run with Docker Compose:

1. Copy env from example:

```bash
cp .env.example .env
```

2. Run the docker container:

```bash
docker compose up -d
```

3. Change the permissions of the import directory. This is necessary so that the backend can access the import directory.

```bash
chmod -R 775 volumes/neo4j_import/
```

4. Navigate to <http://localhost:5173/>. (Use localhost, not 127.0.0.1 due to some issues on frontend.)

5. Navigate to http://localhost:5173/manage-database to load a dataset into Neo4j. Select
   `3_cost_awareness_labelled_shrunk.cypher` for the smallest pre-labelled dataset. This will take a
   few seconds to load. The earlier datasets are much larger. Expect upwards of 30 minutes to load
   them. See following section.

6. Navigate to <http://locahost:5173/query> to use the queries and write your own.

## Using the Database Dumps

We recommend you use a one of the database dumps so you don't need to re-drill the original source repositories. Do the following:

1. Navigate to <http://localhost:5173/manage-database>
2. In the database images section, click load on the image you wish to use. Each image is at a different stage in the process:

- `cost_awareness_full.cypher` - All of the raw drilled data. This will take **over an hour to load**
- `cost_awareness_full_labelled.cypher` - All of the drilled data with the commit message labels added.
- `cost_awareness_pruned_labelled.cypher` - Just the relevant commits and their labels. This loads quickly.

3. Navigate to <http://localhost:5173/query> where you can query the data using the Neo4j Cypher Query Language

## The drill configurations

The drilling of the repositories can be replicated by navigating to <http://localhost:5173/editor>
opening the `cost_awareness_488.yaml` config file in the left bar and clicking execute. This will
execute the drill jobs with the 3 driller workers that are set up by default. 

Performing the drill job will take some time so please be patient. You can track the progress of the drill in <http://localhost:5173/jobs> .

If you wish to increase the number of driller worker instances that are being used to perform the
drills, change line that says `replicas: 3` by replacing the 3 with the number of notes you want.

## Queries from the study

To perform the queries that were used during the study, navigate to <http://localhost:5173/query>
On the left bar, open the query you wish to run. You can then execute the query throught the
interface. There are a few queries to choose from:

- `example` - Folder of example queries to give you an idea of how the query language works

# NeoRepro Documentation

This replication package is created using NeoRepro, a tool for performing an MSR study and creating
a replication package for it. NeoRepro is centered around the Neo4j graph database in order to
create a unified storage system where data can be efficiently queried using the Neo4j Cypher query
language.

## Configuring a Repository Drill

With the drilling yaml configuration you can extract data from a list of Git repositories. The schema is made up of two primary sections:

- `defaults`: Object containing default values which are used for each drill job.
- `repositores`: List of repositories to be drilled and the configuration for that drill. If a configuration is set in the `defaults` section but not in the individual configuration, then the default is applied.

Here is an example configuration from the Mining Cost awareness case study:

```YAML
defaults:
  delete_clone: false
  index_file_modifications: true
  pydriller:
    to: "2022-05-30"
    only_modifications_with_file_types:
      - '.tf'
      - '.tf.json'
  filters:
    commit:
      - field: 'msg'
        value:
          - cheap
          - expens
          - cost
          - efficient
          - bill
          - pay
        method: 'contains'

repositories:
- name: iks_vpc_lab
  url: https://github.com/ibm-cloud-architecture/iks_vpc_lab.git
  delete_clone: true
  pydriller:
      to: "2023-05-30"
- name: cloud-platform-terraform-monitoring
  url: https://github.com/ministryofjustice/cloud-platform-terraform-monitoring.git
- name: terraform-google-nat-gateway
  url: https://github.com/GoogleCloudPlatform/terraform-google-nat-gateway.git
```

### Defaults

The `defaults` object contains the following fields:

- `pydriller`: Object containing configurations for pydriller `Repository` class. This application uses pydriller under the hood to drill the repositories. All options explained at [pydriller](https://pydriller.readthedocs.io/en/latest/repository.html).
  - `since`: Date from which to start drilling. Format: YYYY-MM-DD
  - `to`: Date to which commits should be drilled. Format: YYYY-MM-DD
  - `from_commit`: A commit hash from which to start drilling.
  - `to_commit`: A commit hash to which commits should be drilled.
  - `from_tag`: A tag from which to start drilling.
  - `to_tag`: A tag to which commits should be drilled.
  - `only_in_branch`: Name of branch to be drilled.
  - `only_no_merge`: Boolean. If true, only commits that are not merged will be included.
  - `only_authors`: List of strings. Only commits by these authors will be included.
  - `only_commits`: List of strings. Commit hashes for commits to be included.
  - `only_release`: Boolean. Only commits that are tagged release will be included.
  - `filepath`: Only commits that modify this file will be included.
  - `only_modifications_with_file_types`: List of string. Only commits that modify files of this type will be included.
- `filters`: Object containing string filters.

  - `commit`: List of filters. (Shown below)

- `delete_clone`: Boolean. Indicates whether to delete the cloned repository after the drilling is complete.
- `index_file_modifications`: Boolean. Indicates whether to drill the modified files. If false, only the commits will be drilled.
- `index_file_diff`: Boolean. Indicates whether the file diffs should be indexed. If false, it won't be added to database.

#### Filters

A filter contains the following fields:

- `field`: The field to be checked for the filter.
- `value`: A string or list of strings. The value(s) to be checked for the filter. If list, then behaves as an `OR` (if field contains any of the values).
- `method`: Can be one of the following:
  - `contains`: The value is contained in the field.
  - `!contains`: The value is not contained in the field.
  - `exact`: The value is equal to the field.
  - `!exact`: The value is not equal to the field.

### Repositories

Each repository can contain all of the fields from `defaults` but must also contain the following fields:

- `name`: Name of the repository.
- `url`: Https url to the repository to clone it in the case it isn't already cloned.

If any values are not provided in the repository, the default values from `defaults` will be used.

## Working with Neo4j

### Exporting the Database

Exports the database to a file in the `import` directory of Neo4j.

```
CALL apoc.export.cypher.all("all.cypher", {
    format: "cypher-shell",
    useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
})
YIELD file, batches, source, format, nodes, relationships, properties, time, rows, batchSize
RETURN file, batches, source, format, nodes, relationships, properties, time, rows, batchSize;
```

### Importing the Database

```
CALL apoc.import.cypher.all("all.cypher")
```

## Use cases

- I'm here to access the data
- I'm here to replicate the study
- I'm here to create a replication package
