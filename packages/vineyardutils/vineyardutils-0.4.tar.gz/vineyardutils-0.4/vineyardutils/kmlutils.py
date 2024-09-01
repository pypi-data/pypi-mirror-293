import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import math
import statistics
import simplekml
import alphashape
from sklearn.linear_model import LinearRegression
import itertools

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="Mean of empty slice")
warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in double_scalars")

def extract_coordinates(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    coordinates_element = root.find('.//{http://www.opengis.net/kml/2.2}coordinates')

    if coordinates_element is not None:
        coords_str = coordinates_element.text.strip()
        coords = [tuple(map(float, coord.split(','))) for coord in coords_str.split()]

        data = {'Longitude': [lon for lon, _, _ in coords],
                'Latitude': [lat for _, lat, _ in coords]}

        df = pd.DataFrame(data)
        return df
    else:
        print("No coordinates found in the KML file.")
        return None

def calculate_angle(x1, y1, x2, y2, x3, y3):
    v1 = np.array([x1 - x2, y1 - y2])
    v2 = np.array([x3 - x2, y3 - y2])
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.degrees(np.arccos(cos_theta))
    return angle

def calculate_angle_list(point1, center_point, point3):
    def angle_between_points(p1, p2, p3):
        angle_rad = math.atan2(p3[1] - p2[1], p3[0] - p2[0]) - math.atan2(p1[1] - p2[1], p1[0] - p2[0])
        angle_rad = angle_rad % (2 * math.pi)
        return math.degrees(angle_rad)

    return angle_between_points(point1, center_point, point3)

def haversine_distance(coord1, coord2):
    R = 6371  # Earth radius in kilometers

    lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
    lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def calculate_formula(value1, value2):
    return math.sqrt(abs((value1 + value2) / 2)) + abs(value1 - value2)

def find_min_pair(slopes):
    n = len(slopes)
    num_pairs = int(0.2 * n)  # 20% of the list

    first_20_percent = slopes[:num_pairs]
    last_20_percent = slopes[-num_pairs:]

    pairs = list(itertools.product(first_20_percent, last_20_percent))

    min_pair = min(pairs, key=lambda pair: calculate_formula(pair[0], pair[1]))
    min_pair_indices = (
        slopes.index(min_pair[0]),
        slopes.index(min_pair[1])
    )    
    return(min_pair, min_pair_indices)

def remove_duplicate_tuples(index_list):
    newlist = []
    for i in range(len(index_list)):
        delete = 0  # Reset delete for each outer loop iteration
        for j in range(i + 1, len(index_list)):
            tuple1 = set(index_list[i])
            tuple2 = set(index_list[j])
            common_elements = tuple1.intersection(tuple2)

            if len(common_elements) >= 2:
                newlist.append(tuple(sorted(set(index_list[i] + index_list[j]))))
                delete = len(common_elements)

        if delete == 0:
            newlist.append(tuple(sorted(set(index_list[i]))))

    return(newlist)

def iterate_check_angle(longitudes, latitudes, tanklevels, min_angle, max_angle, elevation):
    if len(longitudes) != len(latitudes):
        raise ValueError("The length of Longitude and Latitude lists must be the same.")

    index_list = []
    k = 0
    mlist = []

    for i in range(len(longitudes) - 2):
        x1, y1 = longitudes[i], latitudes[i]
        x2, y2 = longitudes[i + 1], latitudes[i + 1]
        x3, y3 = longitudes[i + 2], latitudes[i + 2]

        angle = calculate_angle_list([x1, y1], [x2, y2], [x3, y3])
        
        if min_angle < angle < max_angle:
            #distance_x1_x3 = haversine_distance([x1, y1], [x3, y3])
            #print((elevation[i+2] - elevation[i]) / distance_x1_x3)
            tup_test = (k, k + 1, k + 2)
            index_list.append(tup_test)

            X = np.array([[x1], [x2], [x3]])
            y = np.array([y1, y2, y3])

            model = LinearRegression().fit(X, y)
            m_coeff = model.coef_[0]
            mlist.append(m_coeff)

        k += 1

    common_pairs = []
    newlist = index_list
    delete = 0
    #print(index_list)
    testlist=0
    while testlist==0:
        beforecheck=len(newlist)
        newlist=remove_duplicate_tuples(newlist)
        aftercheck=len(newlist)
        #print(f"Before: {beforecheck}, After: {aftercheck}")
        if beforecheck==aftercheck:
            break
    try:
        #q1 = np.percentile(mlist, 20)
        #q3 = np.percentile(mlist, 80)
        #mlist = [m_param for m_param in mlist if q1 <= m_param <= q3]
        #mean_m_param = np.mean(mlist)
        mlist = [m_param for m_param in mlist if not np.isnan(m_param) and np.isfinite(m_param)]
        if not mlist:
            raise ValueError("mlist is empty after removing NaN and Inf values")
        q1 = np.percentile(mlist, 20)
        q3 = np.percentile(mlist, 80)
        filtered_mlist = [m_param for m_param in mlist if q1 <= m_param <= q3]
        if not filtered_mlist:
            raise ValueError("Filtered mlist is empty, cannot compute mean")
        mean_m_param = np.mean(filtered_mlist)
    except (ValueError, IndexError) as e:
        #print(f"An error occurred: {e}")
        mean_m_param = 0
    #except:
    #   mean_m_param = 0
    list_q_coeff=[] 
    for i in range(len(longitudes)):
        x1, y1 = longitudes[i], latitudes[i]
        q_coeff=y1-(mean_m_param*x1)
        list_q_coeff.append(q_coeff)
    
    slope_list=[]
    for row_tuple in newlist:
        coordinates = []
        elevations = []
        for row_num in row_tuple:
            coordinates.append((longitudes[row_num], latitudes[row_num]))
            elevations.append(elevation[row_num])
        distance_X1_Xn = haversine_distance(coordinates[0], coordinates[-1])
        try:
            slope_calc = (elevations[-1]-elevations[0])/distance_X1_Xn
            slope_list.append(slope_calc)
        except Exception as e:
            slope_list.append(99)
    #mean_m_param
    #min & max list_q_coeff        
    try:
        calc_best_slopes=find_min_pair(slope_list)
        tup1=newlist[calc_best_slopes[1][0]]
        tanklev=[]
        tup2=newlist[calc_best_slopes[1][1]]
        tanklev2=[]
        for tups in tup1:
            tanklev.append(tanklevels[tups])
        lev1=statistics.mode(tanklev)

        for tups in tup2:
            tanklev2.append(tanklevels[tups])
        lev2=statistics.mode(tanklev2)
        deltatank=(lev1-lev2)
        selected_slopes=calc_best_slopes[0]
        selected_tuples=calc_best_slopes[1]
    except:
        selected_slopes=[]
        selected_tuples=[]
        deltatank=999
    return(newlist, selected_slopes, selected_tuples, deltatank)

def generate_alpha_shapes(dataframe, alpha=0.2):
    points = [(lon, lat) for lon, lat in zip(dataframe['Longitude'], dataframe['Latitude'])]
    alpha_shape = alphashape.alphashape(points, alpha)
    return alpha_shape

def create_kml(dataframe, row_tuples, kml_filename='outputfile.kml'):
    kml = simplekml.Kml()
    alpha_shape = generate_alpha_shapes(dataframe)
    alpha_polygon = kml.newpolygon(name='Alpha Shape', outerboundaryis=list(alpha_shape.exterior.coords))
    alpha_polygon.style.linestyle.width = 2
    alpha_polygon.style.linestyle.color = simplekml.Color.green

    for row_tuple in row_tuples:
        coordinates = []
        for row_num in row_tuple:
            coordinates.append((dataframe.iloc[row_num]['Longitude'], dataframe.iloc[row_num]['Latitude']))

        linestring = kml.newlinestring(name=f'Line {row_tuple}', coords=coordinates)
        linestring.style.linestyle.width = 3

    kml.save(kml_filename)
    return(list(alpha_shape.exterior.coords))
