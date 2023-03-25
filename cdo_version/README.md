# Author info
Replace fields in the start dump using fields in another start dump.

Lynn Zhou linjing.zhou@bom.gov.au

# Replace fields in the start dump using fields in another start dump
## Fields to replace
| Description | Stash code| netcdf variable name|
|:--|--:| --:|
|LEAF AREA INDEX OF PLANT FUNC TYPES | `m01s00i217`| field1392|
|Stash code  = 875 | `m01s00i875`| temp |
|Stash code  = 880 | `m01s00i880`| temp_1|
|Stash code  = 881 | `m01s00i881`| temp_2|
|Stash code  = 883 | `m01s00i883`| temp_3|
|Stash code  = 884 | `m01s00i884`| temp_4|
|Stash code  = 885 | `m01s00i885`| temp_5|
|Stash code  = 887 | `m01s00i887`| temp_6|
|Stash code  = 888 | `m01s00i888`| temp_7|
* These netcdf variable names only work if you extract only theses 9 fields from a start dump. If it is not the case, please see the netcdf file variable attributes to find the corresponding variable name for certain stash code or um varaible name, and make sure you use these for `-V` when replacing field.

## Extract reference fields
* Open the reference file (here is `restart_dump.astart.esm1.5`) using `xconv`
```
module use ~access/modules
module load xconv
xconv restart_dump.astart.esm1.5
```

* Extract fields from referenc file

Select all fields to replace (left-click), give a output file name with full path (here I call it `reference.nc`), make sure the output format is `netcdf` and click `Convert`. Note that the fields in the reference file are on `192x145` grid, which is not `192x144` grid used in `astart` file. Need regridding.

# Regrid reference fields
* Open the start dump file and extract one field on target grid

Open the start dump file using `xconv` and do the same to extract one field. Any field with `192x144` grid is fine. Save as `astart.nc`. 

* Generate grid file using `cdo`
```
module load cdo
cdo griddes astart.nc > grid
```
`grid` is a text file that contains grid information.

* Regrid `reference.nc` into target grid
```
cdo remapbil,grid reference.nc reference_regrid.nc
```
Here I use bi-linear method. Other methods available. See `cdo` documentation.

## Replace fields
* Copy the start dump
```
cp bi889a.da10500101_00  bi889a.da10500101_00_lynn
```
* Load modules
```
module use ~access/modules
module load pythonlib/umfile_utils/cmip6
```
* Run the repalce script
```
python ~access/apps/pythonlib/umfile_utils/um_replace_field.py -v <stash code> -n reference_regrid.nc -V <netcdf variable name> bi889a.da10500101_00_lynn
```
Stash code and netcdf variable name pairs are listed in the table. One command for replacing one field.
