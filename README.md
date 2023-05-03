* Main program

* Purpose: 
   To replace the fields and convert to the reference grid

* History: 
   24/03/2023 v1

* Note:

       You can find how to run this script in the comments. At the moment, 
   it can only handle single level and pseudo level fields. It cannot be 
   used to replace model level fields. If you need to do so, we can add more functions to it later.
       I am now using scipy.interpolate.RegularGridInterpolator to regrid the field. 
   However the results are different from those using cdo. So please check again to see 
   if you can use /g/data/p66/lz3062/replace_dumpfile/replace_fields/bi889a.da10500101_00_modified
   to run the experiments.
       Here we test the LAI, and other CNP related fields for CAABLE initial to use.
   Those fields in bi889a.da10500101_00 were wrong so that need to be replaced from ESM1.5 start dump.

 Generate by Lynn
 Lynn Zhou <Linjing.Zhou@bom.gov.au>

* Replacement script
 Replace fields in a start dump from a reference start dump
 - designed for replacing single level and pesudo level fields (vegetation)
 - does not work for model level fields (23 Mar 2023)

 Environment:
 module use /g/data/hh5/public/modules
 module load conda/analysis3
'''
# Usage:
 python3 replace_fields -s <stash1> <stash2> <stash3> ... -i <input file> -r <reference file> -o <output file>

python3 replace_fields.py -s 217 875 880 881 883 884 885 887 888 -i /g/data/p66/lz3062/replace_dumpfile/bi889a.da10500101_00 -r /g/data/p66/lz3062/replace_dumpfile/restart_dump.astart.esm1.5 -o /g/data/p66/lz3062/replace_dumpfile/delete_fields/bi889a.da10500101_00_modified
'''
 Author: Lynn Zhou (linjing.zhou@bom.gov.au)
 
 
 # Application (ars599):
The restart dump has been test under the job u-cf888 the AINITIAL need to be replaced:

u-cf888/suite.rc:            AINITIAL = /g/data/p66/ars599/ACCESSESM2/ancillary/ancil/lynn596a.da10500101_00

 
 
