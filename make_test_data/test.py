# %%
import os
from pathlib import Path
import numpy as np
from tqdm.auto import tqdm
import pickle
from collections import defaultdict
import importlib

from themachinethatgoesping.echosounders import kongsbergall, simradraw, index_functions
from themachinethatgoesping import pingprocessing as pp
from themachinethatgoesping import tools as ptools

# %%
import themachinethatgoesping as tmtgp
tmtgp.version()

# %%
#create the output path
path_out = "../unittest_data"
path_in = "./data_in/"

os.makedirs(path_out,exist_ok=True)
os.makedirs(path_in,exist_ok=True)

# %% [markdown]
# ## Explore and sort input data

# %%
folders = index_functions.find_folders_with_files(path_in, [".all",".wcd"], followlinks=True)
folders.sort()
N = 20

for input_path in folders:
    print(input_path)

# %%
import gc

fms = []
for i in range(10):

    input_path = folders[4]

    print(f"\rCreating {i} test data for {input_path}", end="")
    input_files = index_functions.find_files(input_path,['all','wcd'], followlinks=True, verbose=False)

    #open and index files
    index = index_functions.load_index_files(input_files)
    #index = {}
    fm = kongsbergall.KongsbergAllFileHandler_mapped(input_files, cached_index = index, show_progress = False, init = False)
    dm = fm
    del fm

    gc.collect()

gc.collect()

# %%
if False:
    for input_path in folders:
        for endings,prefix,postfix in [
            [".all"         , "all"     , ".all",],
            [".wcd"         , "wcd"     , ".wcd",],
            [[".all",".wcd"], "combined", ".all",]
            ]:

            print(f"Creating {prefix} test data for {input_path}")
            input_files = index_functions.find_files(input_path,endings, followlinks=True)

            #open and index files
            index = index_functions.load_index_files(input_files)
            fm = kongsbergall.KongsbergAllFileHandler_mapped(input_files, cached_index = index)
            index_functions.update_index_files(fm.get_cached_file_index())

            # sort primary file numbers per folder and then per first time stamp

            interfaces = defaultdict(list)

            for interface in tqdm(fm.datagramdata_interface.per_primary_file(),delay=1):
                path = Path(interface.get_file_path())
                interfaces[path.parent].append(interface)

            for path, interfaces_ in tqdm(interfaces.items(),delay=1):
                interfaces_.sort(key=lambda x: x.get_timestamp_first())

            # split the pings per (primary) file path
            pings_per_file_path = pp.split_pings.by_file_path(fm.get_pings, progress=True)

            path_out_ = f"{path_out}/{prefix}"
            os.makedirs(path_out_,exist_ok=True)

            # for each final folder in path_in
            for path, interfaces_ in tqdm(interfaces.items(),delay=1):
                #take the first N pings of the file in the middle of the folder
                middle_file_interface = interfaces_[len(interfaces_)//2]
                file_path = middle_file_interface.get_file_path()
                pings = pings_per_file_path[file_path]

                #get the last timestamp of the Nth ping
                pings = pings[:N]
                last_timestamp = pings[-1].file_data.get_timestamp_last()
                channel_ids = list(pp.split_pings.by_channel_id(pings).keys())

                #build the file nam,e
                d = middle_file_interface.datagrams("InstallationParametersStart")[0]

                time = ptools.timeconv.unixtime_to_datestring(d.get_timestamp(), format="%Y%m%d_%H%M%S")
                is_dual_rx = d.is_dual_rx()
                model = f"EM{d.get_model_number()}"
                channel_id_string = "|".join(channel_ids)
                parent = str(Path(file_path).parent).split("/")[-1]

                key = f"{parent}-{time}-{model}-[{channel_id_string}]-dual_rx({is_dual_rx})"
                print(f" -{key}")

                with open(f"{path_out_}/{key}{postfix}","wb") as ofi:
                    #loop through all datagrams in the file
                    for d in middle_file_interface.datagrams():
                        #if the datagram is after the last timestamp of the Nth ping, stop
                        if d.get_timestamp() > last_timestamp + 5:
                            break

                        #write the datagram to the file
                        ofi.write(d.to_binary())


            


