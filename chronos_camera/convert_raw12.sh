raw_file=$1
dng_folder=$(echo "${raw_file%.*}")
filename=basename ${raw_file} .raw
dng_files="${dng_folder}/${filename}_{:06d}.tiff"

echo Prevadim RAW soubor $raw_file
echo na soubory $dng_files

mkdir $dng_folder

echo "Spoustim prevod"
python3 /home/roman/repos/chronos-utils/python_raw2dng/pyraw2dng.py -M -w 928 -l 928 -p $raw_file $dng_files

echo DONE
