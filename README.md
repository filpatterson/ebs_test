# Django Rest Framework - BEMD

This repository contains a base project for BEMD task at EBS Integrator, each candidate should be able to develop a 
solution for this the task using this boilerplate. Fork it and bring it to the next level. 

More details about this task should be provided by your HR or TL.

## Requirements
- Solution should pass all tests
- Tests should cover 100% of code


# Implementation

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

