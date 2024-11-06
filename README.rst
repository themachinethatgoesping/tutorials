.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/themachinethatgoesping/tutorials/main

Tutorials
=========

Tutorials and demos for themachinethatgoesping

Use
---

- You need your own testdata (Currently Kongsberg .all/.wcd files or Simrad EK80, more formats will be added in the future)
- If you don't have any, send me a message (peter.urban@ugent.be) 
- We will add information on getting testdata in the future
- Use the notebooks in the folder "demo". These are currently the only ones that will be kept up to date with other changes in ping
- See also https://themachinethatgoesping.readthedocs.io/en/latest/first_steps/run_tutorials.html

Prerequisites
-------------

- Windows, Linux or Mac: Development is done on Linux, so this is the most tested

# Install (using miniforge & poetry)

1. Install miniforge (or equivalent e.g. miniconda https://conda-forge.org/miniforge/)
2. Create a new environment, with suitable python version and package manager package `poetry`:

.. code-block:: shell

   $ conda create -n ping python=3.12
   $ conda activate ping
   $ pip install poetry

3. clone this repository

.. code-block:: shell
    
    git clone https://github.com/themachinethatgoesping/tutorials.git
    cd tutorials

3. Navigate to the directory where the `poetry.lock` file is located and run:

.. code-block:: shell

   # This will install the exact version specified in the provided poetry.lock file
   poetry install


4. If there are problems with installing `poetry`, when creating the environment, try instead:

.. code-block:: shell

   conda create -n ping python=3.12
   conda activate ping
   pip install poetry
   poetry install


Run demos
----

Open jupyterlab in the demo folder

.. code-block:: shell
    
    jupyter lab .

Find ping interesting?
----------------------
- Drop me an email and we can have a chat: peter.urban@ugent.be

