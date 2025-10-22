# MDS-IRRS-Lab2

## Setup Instructions

### 1. Set up Docker images

#### Option 1: Using Docker Compose (Recommended)
Simply run:
```
docker-compose up -d
```
#### Option 2: Manually using Docker CLI

1. Setup a Docker Network
```bash
docker network create elasticsearch-internal
```

2. Setup Elasticsearch
```bash
docker run -d --name elasticsearch --net elasticsearch-internal -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:9.1.5
```

3. Setup Kibana
This is optional, but useful for visualizing and interacting with Elasticsearch.
```bash
docker run -d --name kibana --net elasticsearch-internal -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" docker.elastic.co/kibana/kibana:9.1.5
```

## 2. Install Required Python Packages
To do so, make sure you have Python 3.10+ and the `uv` package manager installed.

> [!NOTE]
> You can install `uv` by following the instructions at [uv's official documentation](https://docs.astral.sh/uv/guides/install-python/).

Then, run the following command to install the required packages:
```bash
uv sync
```

This will create a virtual environment and install all dependencies listed in `uv.lock` and `pyproject.toml`.
One of these dependencies is the Data Version Control (`dvc`) package.

## 3. Download Dataset using DVC

To download the dataset required for this lab, run the following command:
```bash
dvc repro
```

This will step through the DVC pipeline to download and process the necessary data files into the `data/` directory.


## 4. Index Documents into Elasticsearch

To index the documents into Elasticsearch, run the following command:
```bash
python -m elastic.indexer --path ./data/processed/arxiv --index arxiv [--token {standard,whitespace,classic,letter}] [--filter ...]
```
