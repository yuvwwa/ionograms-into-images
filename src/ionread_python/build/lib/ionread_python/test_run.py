import ionread_python

# from .ionread_python import *

# iono_path = "/mnt/d/Homework/data/Ионограммы/Proverka_CIV/bolshie_tory_tory/01_08_04_44_00.dat" # max_dist = 1280 , в CIV: ~2400
# iono_path = "/mnt/d/Homework/data/Ионограммы/Proverka_CIV/malenkie_tory_tory/03_28_23_00_00.dat" # max_dist = 750, в CIV: ~1500
# iono_path = "/mnt/d/Homework/data/Ионограммы/Proverka_CIV/malenkie_usolie_tory/03_28_23_00_01.dat" # max_dist = 750, в CIV: ~1500 (ВЗ)
iono_path = '/mnt/d/Homework/data/piv_identity/missing_piv/маш_обуч_спокойные/01_01_06_48_00.dat' #53
# iono_path =  "/mnt/d/Homework/data/Ионограммы/for_neuro_proc/Magadan-Tory/10_20_15_50_00.dat" # max_dist =  4280, в CIV примерно также
# iono_path = 'test_data/03_02_05_08_00.dat'


ingr = ionread_python.read_ionogram(
            iono_path)

max_dist = max(ingr.data, key=lambda x: x.num_dist).dist 

print('Success!')