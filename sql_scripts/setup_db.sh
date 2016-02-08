#!/bin/bash

set -euo pipefail

cat make_database.sql | psql
cat create_schema_and_enable_postgis.sql | psql nasatiled
zcat rainfall_all_tiled.sql.gz | psql nasatiled
cat make_index.sql | psql nasatiled