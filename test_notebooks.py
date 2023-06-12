#!/usr/bin/env python3
# Clean the notebook cache to save memory online
# Tutorial notebooks are pushed to git lfs!

import os
import subprocess as sub
from tqdm.auto import tqdm

notebooks = []

for r,d,f in os.walk('.'):
  if '.ipynb_checkpoints' in r:
    continue

  for file in f:
    if file.endswith('.ipynb'):
      notebooks.append(r + '/' + file)

# delete jupyter_nbconvert.log if it exists
if os.path.exists('jupyter_nbconvert.log'):
  os.remove('jupyter_nbconvert.log')

# delete pytest.log if it exists
if os.path.exists('pytest.log'):
	  os.remove('pytest.log')

		# call pytest --nbmake on each notebook
# if pytest fails, exit and print error
# if pytest succeeds, continue
it = tqdm(notebooks)
for notebook in it:
	it.set_description(notebook)
	try:
		if sub.run(['pytest', '--nbmake', '--verbose', notebook], stdout=open('pytest.log', 'a')).returncode != 0:
			exit()
	except:
		print('pytest failed on ' + notebook)
		sub.run(['pytest', '--nbmake', notebook])
		exit()


# call jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace on each notebook
# use subprocess instead of os.system
# print stderr output to jupyter_nbconvert.log
for notebook in tqdm(notebooks):
	sub.run(['jupyter', 'nbconvert', '--ClearOutputPreprocessor.enabled=True', '--inplace', notebook], stderr=open('jupyter_nbconvert.log', 'a'))




