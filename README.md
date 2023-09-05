# Data Access Layer 

Data-driven innovation through the use of the Data Access Layer based on [TM1py](https://github.com/cubewise-code/tm1py) ❤️

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![ibm](https://img.shields.io/badge/-PlanningAnalytics-052FAD?logo=ibm&style=for-the-badge)](https://www.ibm.com/de-de/products/planning-analytics?utm_content=SRCWW&p1=Search&p4=43700075197142448&p5=e&gclid=CjwKCAjwo9unBhBTEiwAipC11-CQKNzBaWXDT2LYKf345cWn_zRCW87X-ShO3_hRVHAlY3eXR_iCaRoC0t8QAvD_BwE&gclsrc=aw.ds)

Install
=======================
> copy the following files to your python development environment
- DEV.yml
- DAL.py

Configure the DEV.yml
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

query = f"SELECT NON EMPTY {mdx['columns']} ON 0, NON EMPTY {mdx['rows']} ON 1 FROM [cube] WHERE ({','.join(mdx['where'])})"
```

> Call the DAL request by MDX-Statement
``` python
data_raw = DAL.load_data_by_mdx(query)
```

Helper
=======================

> convert pandas multi-index to standard pandas.DataFrame
``` python
data = data_raw.dropna()
data = data.unstack()
data = data.reset_index()
data.columns = data.columns.map(''.join)
```

> Call the DAL request by View
``` python
data_raw = DAL.load_data_by_view(query)
```

>  Write dataframe
``` python
DAL.write_dataframe(cube="cube",dataframe=data)
```

>  Write cellset
``` python
DAL.write_cellset(cube="cube",cellset=data)
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
- Easily configurable via YAML files
- Significantly more interfaces of source/target systems can be connected (compared to TurboIntegrator) - e.g. OData
- Core technology extending application
- Secure and encrypted connection via SSL; data is not transferred in plain text
- Data transfer from cloud to cloud using the authorization schema specified by the source and target system in each case

Requirements
=======================

- [![Static Badge](https://img.shields.io/badge/Python-3.7-yellow)](https://www.python.org/)
- [![Static Badge](https://img.shields.io/badge/TM1py-1.11.3-yellow)](https://pypi.org/project/TM1py/)
- [![Static Badge](https://img.shields.io/badge/requests-2.31.0-yellow)](https://pypi.org/project/requests/)
- [![Static Badge](https://img.shields.io/badge/typing_extensions-4.7.1-yellow)](https://pypi.org/project/typing-extensions/)
- [![Static Badge](https://img.shields.io/badge/IBM_Planning_Analytics-11-blue)](https://www.ibm.com/de-de/products/planning-analytics?utm_content=SRCWW&p1=Search&p4=43700075197142448&p5=e&gclid=CjwKCAjwo9unBhBTEiwAipC11-CQKNzBaWXDT2LYKf345cWn_zRCW87X-ShO3_hRVHAlY3eXR_iCaRoC0t8QAvD_BwE&gclsrc=aw.ds)

Optional Requirements
=======================

- [![Static Badge](https://img.shields.io/badge/pandas-2.1.0-yellow)](https://pypi.org/project/pandas/)
- [![Static Badge](https://img.shields.io/badge/requests_negotiate_sspi-0.5.2-yellow)](https://pypi.org/project/requests-negotiate-sspi/)

Issues
=======================

If you find issues, sign up in Github and open an Issue in this repository


Contribution
=======================

DAL is like a magical show, where everyone in the TM1 community can become a wizard! 🧙‍♂️

If you happen to spot a pesky bug or have a spellbinding idea to enhance it, simply take your magical wand (fork the repository), weave your code incantations, and then conjure up a pull request. We'll be ready to merge in your enchanting contributions! ✨🪄