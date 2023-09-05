# Data Access Layer 

Data-driven innovation through the use of the data access layer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![ibm](https://img.shields.io/badge/-PlanningAnalytics-052FAD?logo=ibm&style=for-the-badge) 

Install
=======================
> copy the following files to your python development environment
- DEV.yml
- DAL.py

Config
=======================
```yaml
planning_analytics:
    address: <url to your ibm planning analytics instance>
    port: <http-port>
    user: <username>
    password: <password>
    ssl: <boolean>
```

Use
=======================
> import

``` python
from DAL import DataAccessLayer
```

> instantiate the Data Access Layer with the DEV environment
``` python
DAL = DataAccessLayer(path='DEV.yml')
```

> build example mdx-statement
``` python
mdx = {
    'columns':'{TM1FILTERBYLEVEL(TM1SUBSETALL([col.dim].[col.dim]) , 0)}',
    'rows':'{TM1FILTERBYLEVEL(TM1SUBSETALL([row.dim].[row.dim]) , 0)}',
    'where':[
        '[where.dim].[where.dim].[member]'
    ]
}

query = f"SELECT NON EMPTY {mdx['columns']} ON 0, NON EMPTY {mdx['rows']} ON 1 FROM [etl.data] WHERE ({','.join(mdx['where'])})"
```

> Call the Data Access Layer PULL request by MDX-Statement
``` python
data_raw = DAL.load_data_by_mdx(query)
```

Helper
=======================

> convert pandas multi-index to flat df
``` python
data = data_raw.dropna()
data = data.unstack()
data = data.reset_index()
data.columns = data.columns.map(''.join)
```

> Run TI
``` python
DAL.run_ti(name="test",parameters={'pnValue':1234})
```

Features
=======================

DAL has more tricks up its sleeve than a magician's hat when it comes to getting cozy with TM1py, such as

- Read data from TM1 via MDX and views as easy as possible 
- Write/Push data from outside into TM1 
- Retrieve TI processes from outside 
- Easily configurable via YAML files 
- Significantly more interfaces of source/target systems can be connected (compared to TurboIntegrator) - e.g. OData 
- Core technology extending application 
- Secure and encrypted connection via SSL; data is not transferred in plain text 
- Data transfer from cloud to cloud using the authorization scheme specified by the source and target system in each case


Requirements
=======================

- python (3.7 or higher)
- requests
- TM1 11 
- TM1py

Optional Requirements
=======================

- pandas
- requests_negotiate_sspi


Issues
=======================

If you find issues, sign up in Github and open an Issue in this repository


Contribution
=======================

DAL is like a magical show, where everyone in the TM1 community can become a wizard! 🧙‍♂️

If you happen to spot a pesky bug or have a spellbinding idea to enhance it, simply take your magical wand (fork the repository), weave your code incantations, and then conjure up a pull request. We'll be ready to merge in your enchanting contributions! ✨🪄