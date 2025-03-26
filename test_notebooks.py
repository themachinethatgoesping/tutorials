#!/usr/bin/env python3
# Clean the notebook cache to save memory online
# Tutorial notebooks are pushed to git lfs!

import os
import shutil as sh
import subprocess as sub
from tqdm.auto import tqdm

notebooks = []

# delete all '.ipynb_checkpoints' folders
del_folders = []
for r,d,f in os.walk('.'):
	for folder in d:
		if folder.endswith('.ipynb_checkpoints'):
			del_folders.append(r + '/' + folder)

for folder in del_folders:
	if os.path.exists(folder):
		# delete folder even if it is not empty
		sh.rmtree(folder,ignore_errors=True)

for r_,d_,f_ in os.walk('.'):
	if not 'test_notebooks' in f_:
		continue
	
	for r,d,f in os.walk(r_):
		if 'no_testing' in f:
			continue
		for file in f:
			if file.endswith('.ipynb'):
				notebooks.append(r + '/' + file)
				print(f'found {notebooks[-1]}')

# delete jupyter_nbconvert.log if it exists
if os.path.exists('jupyter_nbconvert.log'):
  os.remove('jupyter_nbconvert.log')

# delete pytest.log if it exists
if os.path.exists('pytest.log'):
	  os.remove('pytest.log')

# call pytest --nbmake on each notebook
# if pytest fails, exit and print error
# if pytest succeeds, continue
# print('Running pytest on each notebook...')
# print(f'found {notebooks}')
# for notebook in notebooks:
# 	if sub.run(['pytest', '--nbmake', notebook]).returncode != 0:
# 		exit()

# call pytest --nbmake on each notebook
# if pytest fails, exit and print error
# if pytest succeeds, continue
print('Running pytest on each notebook...')
print(f'found {notebooks}')
if sub.run(['pytest', '--nbmake', *notebooks]).returncode != 0:
	exit()


# call jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace on each notebook
# use subprocess instead of os.system
# print stderr output to jupyter_nbconvert.log
if False:
	for notebook in tqdm(notebooks):
		sub.run(['jupyter', 'nbconvert', '--ClearOutputPreprocessor.enabled=True', '--inplace', notebook], stderr=open('jupyter_nbconvert.log', 'a'))




