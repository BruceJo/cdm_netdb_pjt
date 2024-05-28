# CDM_NETDB_PJT

## Dir.
```
./
|-- .gitignore
|-- conf
|   |-- app.conf
|   `-- status.conf
|-- schema
|   |-- detailDbSchema.sql
|   |-- naverCloudSchema.sql
|   `-- recoveryDbSchema.sql
|-- src
|   |-- apiClient.py
|   |-- connDbnApi.py
|   |-- createALL.py
|   |-- createSchema.py
|   |-- createVPC.py
|   |-- cyclicSub.py
|   |-- cyclicSync.py
|   |-- demo_test.ipynb
|   |-- getConfig.py
|   |-- history.pkl
|   |-- insertDetail.py
|   |-- insert_query.log
|   |-- main.py
|   |-- masterController.py
|   |-- naverCloud.py
|   |-- naverController.py
|   |-- readVPC2InsertDB.py
|   `-- vudVPC.py
`-- README.md
```

## Env.
```
Windows 10 Edu.
python 3.11
```


## Requirements
```
Flask==3.0.3
Flask-Cors==4.0.1
psycopg2==2.9.9
configparser==7.0.0
pandas==2.2.2
SQLAlchemy==2.0.30
sqlalchemy-cockroachdb==2.0.2
requests==2.31.0
pickle-mixin==1.0.2
pika==1.3.2
```
