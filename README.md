Design
======
A location-based popular products search software based on Flask. 
The problem we aim to solve is that finding to find the most popular products 
near selected point by using spatial search. 

Spatial search is expensive. It should be used on few targets as possible. 
In order to do this, we developed a cheaper filter by using `python-geohash` 
library. 
We make use of this filter with a tag or without tags. 
A fast popular product search cannot be implemented without a DBMS, 
but we are not going to use any external databases at the moment. 
Instead, we use `pandas` to handle data structures and to work with relational data. 
Spatial search and database modules are implemented without Flask to test it 
individually. 
See more details in `spatialindex.py` and `data.py` respectively. 

For preprocessing data, we created refined data from raw data. 
Firstly we removed products which quantity is zero. 
Secondly we sorted product lists for each shop. 
Thirdly we created shop list for each tag. 
Those three steps provide more actionable data ready to available 
and help us to use software with significant improveid performance. 

How to start
============

  ```
  $ python runserver.py
  $ cd client
  $ python -m SimpleHTTPServer
  ```
