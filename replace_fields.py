# Replace fields in a start dump from a reference start dump
# - designed for replacing single level and pesudo level fields (vegetation)
# - does not work for model level fields (23 Mar 2023)
#
# Environment:
# module use /g/data/hh5/public/modules
# module load conda/analysis3
#
# Usage:
# python3 replace_fields -s <stash1> <stash2> <stash3> ... -i <input file> -r <reference file> -o <output file>
# e.g. python3 replace_fields.py -s 217 875 880 881 883 884 885 887 888 -i /g/data/p66/lz3062/replace_dumpfile/bi889a.da10500101_00 -r /g/data/p66/lz3062/replace_dumpfile/restart_dump.astart.esm1.5 -o /g/data/p66/lz3062/replace_dumpfile/delete_fields/bi889a.da10500101_00_modified
#
# Author: Lynn Zhou (linjing.zhou@bom.gov.au)

import numpy as np
from scipy.interpolate import RegularGridInterpolator
import argparse
import mule
import warnings
warnings.filterwarnings('ignore')

def get_grid(umf,stash):
    for ifield, field in enumerate(umf.fields):
        if field.lbuser4 == stash:
            nlat,nlon = field.get_data().shape
            lat_s = field.bzy+field.bdy
            dlat = field.bdy
            lon_s = field.bzx+field.bdx
            dlon = field.bdx
            break
    lon = np.arange(lon_s,lon_s+dlon*nlon,dlon)
    lat = np.arange(lat_s,lat_s+dlat*nlat,dlat)
    return lon,lat

class replaceOperator(mule.DataOperator):
    """Operator which replace data with delta"""
    def __init__(self,delta):
        self.delta = delta
    def new_field(self, source_field):
        """Creates the new field object"""
        field = source_field.copy()
        return field
    def transform(self, source_field, new_field):
        """Performs the data manipulation"""
        data = source_field.get_data()
        data_out = self.delta
        return data_out
    
def replace(stash,src,trg):
    print(f'=========================================================================================')
    print(f' Replacing stash code {stash}')
    print(f'=========================================================================================')
    lon_src,lat_src = get_grid(src,stash)
    lon_trg,lat_trg = get_grid(trg,stash)
    lats_trg,lons_trg = np.meshgrid(lat_trg,lon_trg,indexing='ij')
    for src_ifield, src_field in enumerate(src.fields):
        if src_field.lbuser4 == stash:
            data = np.where(src_field.get_data()==-1073741824,np.nan,src_field.get_data())
            interp = RegularGridInterpolator((lat_src,lon_src),data,bounds_error=False,fill_value=None)
            data_int = interp((lats_trg,lons_trg))
            for trg_ifield,trg_field in enumerate(trg.fields):
                if trg_field.lbuser4 == src_field.lbuser4 and trg_field.lbuser5 == src_field.lbuser5:
                    print(f'[Info] Field {trg_ifield} in the target file matches field {src_ifield} in the source file. Replacing...')
                    replace_operator = replaceOperator(data_int)
                    trg.fields[trg_ifield] = replace_operator(trg_field)
                    print('[Info] Replaced.')
    return trg

def main(inargs):
    stash_list = inargs.stash
    src_file = inargs.reference
    trg_file = inargs.input
    ofile = inargs.output
    
    src = mule.DumpFile.from_file(src_file)
    trg = mule.DumpFile.from_file(trg_file)
    print(f'=========================================================================================')
    print(f'Target file: {trg_file}')
    print(f'Source file {src_file}')
    print(f'=========================================================================================')
    print(f' Removing stash code 151, 152 and 153')
    print(f'=========================================================================================')
    print('[Info] Removing...')
    for field in list(trg.fields):
        if field.lbuser4 in [151,152,153]:
            trg.fields.remove(field)
    print('[Info] Removed.')

    for stash_str in stash_list:
        stash = int(stash_str)
        trg = replace(stash,src,trg)

    print(f'=========================================================================================')
    print(f' Write to file')
    print(f'=========================================================================================')
    print('[Info] Writing...')
    trg.to_file(ofile)
    print('[Info] Done.')
    
if __name__ == '__main__':
    description = 'Replace fields in a start dump from a reference start dump.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s','--stash', nargs="+", help='stash code separated by space, eg. --stash 271 888')
    parser.add_argument('-i','--input', help='full path to input start dump')
    parser.add_argument('-r','--reference', help='full path to reference start dump')
    parser.add_argument('-o','--output', help='full path to output start dump')
    args = parser.parse_args()
    main(args)
    
