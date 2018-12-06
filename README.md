# Steps
Must download magine and place in root directory.
```
git clone https://github.com/LoLab-VU/MAGINE Magine
```

Docker file for production (on puma) can be started with 
```
bash run_production.sh
```

For local testing

```
bash run_local.sh
```

## Information
Using sqlite as db. 

It stores a 'project' in a simple form. Enrichment output is stored in a separate table.


## Things to fix
Right now the first installation gives errors because one of the views 
requires the tables to be created, but when initializing the repo for the first time these tables are not made.

## TODO
Make enrichment calculation calls to be ran in the background using redis/rabbitmq. Right now they take long.
Users uplaod a zip file from raptr. This is processed and added to the 'project' table. Then enrichment is ran.
