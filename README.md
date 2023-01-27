# Django Rest Framework - BEMD

This repository contains a base project for BEMD task at EBS Integrator, each candidate should be able to develop a 
solution for this the task using this boilerplate. Fork it and bring it to the next level. 

More details about this task should be provided by your HR or TL.

## Requirements
- Solution should pass all tests
- Tests should cover 100% of code


# Implementation

**IMPORTANT**: *use of the python with version 3.10+ will give an error because module ```collections``` has been moved
to ```collections.abc.Callable```, make sure using Python 3.8 or 3.9*

**NOTE:**: correct error log, there is specified that ```psycofg2``` is required for ```AbstractJsonModel```, while
actually there is required ```psycopg2```

It is required to initialize virtual environment to evade version errors of modules. Becuase of that, for the project 
will be created virtual environment based on the Conda Python interpretator equal to Python 3.9. To make possible 
installation of modules inside of the virtual environment it is required to install ```virtualenv``` module and 
initialize environment:

```py -m pip install --user virtualenv```

```py -m venv env```

Environment is created, but it is required to activate it get inside of the virtual environment on the command line level 
and establish contact with inner python and pip. It is done via launching ```activate``` script inside of ```venv``` 
section. From CMD it is done using ```venv_name/Scripts/activate```. 
**IMPORTANT**: *it is required to activate it each time starting work over the project*.

Final preparation stage is in collecting modules out of ```requirements.txt``` using command 
```pip install -r requirements.txt```

## Stage 1: making a Product endpoint

Considering that at the stage of verification of the project was discovered that base of the products and price
intervals were made, it is required to check that they are present in the Django ```settings.py``` inside of the
```config``` directory. They are mentioned insider of the ```INSTALLED_APPS``` list as ```apps.common``` and
```apps.products```

There are 4 files with which we will be working: ```models.py``` mentioning classes with which we'll be working,
```serializers.py``` that will be responsible for handling object inside of the database (setting unique IDs, 
creating objects, deleting them, updating them), ```views.py``` responsible for establishing connection request
receiver and serializer making actions, ```urls.py``` covering URL strategy.

Serializer out of the box is able to remove elements from the DB, but it was required to add 2 custom methods to create
new elements (defining how) and to update them. In ```Views``` it was required to implement POST, PUT, GET, DELETE
requests.

## Stage 2: making a Price Interval endpoint

Price interval connects to the Product entity and shows how price was changing over time. There is repeated the same
endpoints as for the Product class, but this time there was added method ```get_average_price```. The idea behind
making average price, considering that prices can have different time intervals was to make time-weighted formula:

```Python
                 sum(PRICE_i * INTERVAL_DAYS_i)
average_price = --------------------------------, where i stands for intervals
                    sum(INTERVAL_DAYS_i)
```

The problem is that at the stage of writing this section of ```readme``` it was requiring to pass product ID in the
path instead of passing it as the POST-request body part.

## Stage 3: making average price endpoint

Considering presence of the Product Stats elements it was decided to use them to form endpoints for the average price
calculation. Original test suggestion is in using the GET request to the endpoint transmitting body. The problem is
that as a standard it is considered that GET should be empty, without body. Therefore, it is either required to
specify POST request (made in this case) with body or to make a GET with data transmitted in the address. GET was
modified to the POST and it provides average price back to the requester.

It was required to make rework of the Price Interval class considering that old records can be rewritten by the new
ones.

**Suggestion**: *maybe performance will improve in case of setting alternative class structure. Instead of having
```PriceInterval``` can be set ```PriceDatemark``` setting one ```Date``` field and having two fields: ```beforePrice```
registering price before this date landmark and ```afterPrice``` with price after this date landmark.