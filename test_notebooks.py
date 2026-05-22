#!/usr/bin/env python3
# Clean the notebook cache to save memory online
# Tutorial notebooks are pushed to git lfs!

import os
import shutil as sh
import subprocess as sub
from tqdm.auto import tqdm

notebooks = []


def is_testing_disabled(path):
	current = os.path.abspath(path)
	while True:
		if os.path.exists(os.path.join(current, 'no_testing')):
			return True
		parent = os.path.dirname(current)
		if parent == current:
			return False
		current = parent

# delete all '.ipynb_checkpoints' folders
del_folders = []

for root, dirs, files in os.walk('.'):
	for folder in dirs:
		if folder.endswith('.ipynb_checkpoints'):
			del_folders.append(os.path.join(root, folder))

for folder in del_folders:
	if os.path.exists(folder):
		# delete folder even if it is not empty
		sh.rmtree(folder, ignore_errors=True)

for root, dirs, files in os.walk('.'):
	if not any(name.startswith('test_notebooks') for name in files):
		continue
	if is_testing_disabled(root):
		dirs[:] = []
		continue

	for current_root, current_dirs, current_files in os.walk(root):
		if is_testing_disabled(current_root):
			current_dirs[:] = []
			continue
		current_dirs[:] = [folder for folder in current_dirs if not folder.startswith('.')]
		if 'no_testing' in current_files:
			continue
		for file in current_files:
			if file.endswith('.ipynb'):
				notebooks.append(os.path.join(current_root, file))
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




