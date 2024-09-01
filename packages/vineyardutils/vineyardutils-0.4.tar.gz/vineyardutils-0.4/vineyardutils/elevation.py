import subprocess
import sys
import os
import platform
import pandas as pd

def get_elevation(osgeopath, coordmode, geotiff_filename, lat, lon):
    # Gather values for the gdallocationinfo command string
    systeminfo=platform.system()
    if "Windows" in systeminfo:
        cmd = [
            osgeopath,
            'gdallocationinfo',
            coordmode,
            '-valonly',
            #'-geoloc',
            #'-b 1',
            geotiff_filename,
            str(lon),
            str(lat)
        ]
    elif "Linux" in systeminfo:
        cmd = [
            'gdallocationinfo',
            coordmode,
            '-valonly',
            #'-geoloc',
            #'-b 1',
            geotiff_filename,
            str(lon),
            str(lat)
    ]
    
    result_string = ' '.join(cmd)
    try:
        # Execute the gdallocationinfo command)
        result = subprocess.run(result_string, shell=True, capture_output=True, text=True, check=True)
        elevation=float(result.stdout)/10
        return elevation

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stdout)
        return None

def crop_geotiff(osgeopath, srsmode, minlon, minlat, maxlon, maxlat, source_path_tif, output_path_tif):
    systeminfo=platform.system()
    if "Windows" in systeminfo:
        cmd = [
            osgeopath,
            'gdalwarp -t_SRS',
            srsmode,
            '-overwrite',
            '-te',
            str(minlon),
            str(minlat),
            str(maxlon),
            str(maxlat),
            source_path_tif,
            output_path_tif
        ]
    elif "Linux" in systeminfo:
        cmd = [
            #osgeopath,
            'gdalwarp -t_SRS',
            srsmode,
            '-overwrite',
            '-te',
            str(minlon),
            str(minlat),
            str(maxlon),
            str(maxlat),
            source_path_tif,
            output_path_tif
        ]
    result_string = ' '.join(cmd)
    result = subprocess.run(result_string, shell=True, capture_output=True, text=True, check=True)
    #print("Done, check in folder")
    
def get_elevation_list(osgeopath, sourcename, coordmode, geotiff_filename):
    # Gather values for the gdallocationinfo command string
    systeminfo=platform.system()
    if "Windows" in systeminfo:
        cmd = [
            osgeopath,
            'type',
            sourcename,
            '|',
            osgeopath, 
            'gdallocationinfo',
            coordmode,
            '-valonly',
            geotiff_filename
        ]
    elif "Linux" in systeminfo:
        #"cat /media/pierluigi/OS/OSGeo4W/coordinates2.txt | gdallocationinfo -wgs84 -valonly /media/pierluigi/OS/OSGeo4W/output.tif", shell=True, capture_output=True, text=True, check=True)
        cmd = [
            'cat',
            sourcename,
            '|',
            'gdallocationinfo',
            coordmode,
            '-valonly',
            geotiff_filename
        ]        
    result_string = ' '.join(cmd)
    #print(result_string)
    try:
        # Execute the gdallocationinfo command)
        result = subprocess.run(result_string, shell=True, capture_output=True, text=True, check=True)
        result=result.stdout.splitlines()
        result_list=[]
        for i in result:
            num=float(i)/10
            if num<0:
                num=0
            result_list.append(num)
        return result_list

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stdout)
        return None

def add_elevation_to_df(df,latcolname:str,loncolname:str, osgeopath, coordmode, geotiff_filename, crop:bool=0, type_srs:str="EPSG:4326"):
    #if "Latitudes" not in df:
    #    raise ValueError("Latitudes column not present in dataframe")
    #if "Longitudes" not in df:
    #    raise ValueError("Longitudes column not present in dataframe")
    #if len(Latitudes) != len(Longitudes):
    #   raise ValueError("Latitude list and Longitude list have different length!")
    Longitudes = df[loncolname].tolist()
    Latitudes = df[latcolname].tolist()

    #Some checks and data conversion might be needed. Numbers could have been read as strings
    if all(isinstance(item, (int, float)) for item in Longitudes)==False:
        try:
            Longitudes = list(map(float, Longitudes))
        except ValueError:
            print("At least one element in longitudes is not a number")

    if all(isinstance(item, (int, float)) for item in Latitudes)==False:
        try:
            Latitudes = list(map(float, Latitudes))
        except ValueError:
            print("At least one element in latitudes is not a number")

                         
    # Create tuples of lon, lat coordinates and write them to a file
    coord_tuples = [(elem1, elem2) for elem1, elem2 in zip(Longitudes, Latitudes)]
    output_file = "coordinate_test.txt"
    with open(output_file, 'w') as file:
        for lon, lat in coord_tuples:
            file.write(f"{lon} {lat}\n")
    file.close()

    if crop==1:
        #Time to crop the geotiff to maxmin lat and long to save time
        minlatitude=min(Latitudes)
        maxlatitude=max(Latitudes)
        minlongitude=min(Longitudes)
        maxlongitude=max(Longitudes)
        outfile= 'TEMPFILEdem_crop.tif'
        crop_geotiff(osgeopath, type_srs, minlongitude, minlatitude, maxlongitude, maxlatitude, geotiff_filename, outfile)
    
    list_elevation=get_elevation_list(osgeopath, output_file, coordmode, geotiff_filename)
    df['Elevation']=list_elevation
    if crop==1:
        os.remove('TEMPFILEdem_crop.tif')

    return df
