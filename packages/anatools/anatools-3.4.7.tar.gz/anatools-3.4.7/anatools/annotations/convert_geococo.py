import json
import math
import os
import datetime
from PIL import Image
def create_cocodata():
    cocodata = dict()
    cocodata['info'] = {    
        "description":  "Rendered.AI Synthetic Dataset",
        "url":          "https://rendered.ai/",
        "contributor":  "info@rendered.ai",
        "version":      "1.0",
        "year":         str(datetime.datetime.now().year),
        "date_created": datetime.datetime.now().isoformat()}
    cocodata['licenses'] = [{
        "id":   0,
        "url":  "https://rendered.ai/",     # "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "name": "Rendered.AI License"}]     # "name": "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"}]
    cocodata['images'] = list()
    cocodata['categories'] = list()
    return cocodata
def get_rotated_bbox_coordinates(center_x, center_y, width, height, angle_degrees):
    """
    Calculates the pixel-space coordinates of a rotated bounding box.
    Parameters:
    - center_x, center_y: The center of the bounding box in pixel space
    - width, height: The width and height of the bounding box
    - angle_degrees: The rotation angle of the bounding box in degrees
    Returns:
    - A list of coordinates starting from the topmost point and proceeding anti-clockwise.
    """
    
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle_degrees)
    # Half dimensions
    half_width = width / 2.0
    half_height = height / 2.0
    # Calculate the coordinates of the four corners relative to the center
    corners = [
        (-half_width, -half_height),  # Top-left
        (half_width, -half_height),   # Top-right
        (half_width, half_height),    # Bottom-right
        (-half_width, half_height)    # Bottom-left
    ]
    # Rotate the corners relative to the center
    rotated_corners = []
    for x, y in corners:
        rotated_x = center_x + (x * math.cos(angle_radians) + y * math.sin(angle_radians))
        rotated_y = center_y + (-x * math.sin(angle_radians) + y * math.cos(angle_radians))
        rotated_corners.append((rotated_x, rotated_y))
    # Sort by angle to get counter-clockwise order
    rotated_corners.sort(key=lambda point: math.atan2(point[1] - center_y, point[0] - center_x))
    # Find the topmost point to start from
    topmost_point = max(rotated_corners, key=lambda point: point[1])
    # Reorder points to start with the topmost
    topmost_index = rotated_corners.index(topmost_point)
    rotated_corners = rotated_corners[topmost_index:] + rotated_corners[:topmost_index]
    # Flatten the list of tuples
    return [coord for point in rotated_corners for coord in point]
class geo_image:
    def __init__(self, image_width, image_height, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon):
        """
         Parameters:
        - image_width: The width of the image in pixels.
        - image_height: The height of the image in pixels.
        - top_left_lat: The latitude of the top-left corner of the image.
        - top_left_lon: The longitude of the top-left corner of the image.
        - bottom_right_lat: The latitude of the bottom-right corner of the image.
        - bottom_right_lon: The longitude of the bottom-right corner of the image.
        """
 
        self.image_width = image_width
        self.image_height = image_height
        self.top_left_lat = top_left_lat
        self.top_left_lon = top_left_lon
        self.bottom_right_lat = bottom_right_lat
        self.bottom_right_lon = bottom_right_lon
    def pixel_to_geo(self, pixel_coords):
        """
        Converts a flattened list of pixel coordinates to geographic coordinates (latitude, longitude).
        Parameters:
        - pixel_coords: A flattened list of pixel coordinates [x1, y1, x2, y2, ...].
        Returns:
        - A flattened list of geographic coordinates [lat1, lon1, lat2, lon2, ...].
        """
        # Calculate the width and height of the geographic area covered by the image
        lat_range = abs(self.top_left_lat - self.bottom_right_lat)
        lon_range = abs(self.bottom_right_lon - self.top_left_lon)
        # Initialize the list for geographic coordinates
        geographic_coords = []
        # Iterate over the pixel coordinates in pairs (x, y)
        for i in range(0, len(pixel_coords), 2):
            pixel_x = pixel_coords[i]
            pixel_y = pixel_coords[i + 1]
            # Calculate the geographic coordinates of the pixel
            lat = self.top_left_lat - (pixel_y / self.image_height) * lat_range
            lon = self.top_left_lon + (pixel_x / self.image_width) * lon_range
            # Append the result to the list
            geographic_coords.append(lon)
            geographic_coords.append(lat)
        return geographic_coords
def convert_geococo(datadir, outdir, mapping):
    annsdir = os.path.join(datadir, "annotations")
    metadir = os.path.join(datadir, "metadata")
    imgdir = os.path.join(datadir, "images")
    annsfiles = os.listdir(annsdir)
    
    cocodata = create_cocodata()
    cats = {}
    imgid = 0
    annid = 0
    with open(os.path.join(outdir,'geococo.json'), 'w+') as of:
        of.write('{"annotations": [')
        first = True
        # for each interpretation, gather annotations and map categories
        for f in sorted(annsfiles):
            if not f.endswith('.json'):
                continue
            with open(os.path.join(annsdir,f), 'r') as af: anns = json.load(af)
            with open(os.path.join(metadir,f.replace('ana','metadata')), 'r') as mf: metadata = json.load(mf)
            # check for required fields for rotated bounding box calculation
            calc_rotated_bbox = False
            rb_meta_fields = ['meters_per_pixel', 'azimuth']
            if 'sensor' in metadata:
                img_width =  metadata['sensor']['resolution'][0]
                img_height =  metadata['sensor']['resolution'][1]
                if 'frame' in metadata['sensor']: metadata['frame'] = metadata['sensor']['frame']
                if all(metadata['sensor'].get(field) is not None for field in rb_meta_fields):
                    calc_rotated_bbox = True
            else:
                im = Image.open(os.path.join(imgdir, anns['filename']))
                img_width, img_height = im.size
            
            # check for required metadata fields for geolocation
            calc_geo = False
            geo_fields = ['lat', 'lon', 'bottom', 'right']
            if 'environment' in metadata:
                if all(metadata['environment'].get(field) is not None for field in geo_fields):
                    img_geo = geo_image(img_width, img_height, *[metadata['environment'][field] for field in geo_fields])
                    calc_geo = True
            # for each object in the metadata file, check if any of the properties are true
            for obj in metadata['objects']:
                for prop in mapping['properties']:
                    if eval(prop):
                        for ann in anns['annotations']:
                            if ann['id'] == obj['id']: 
                                class_num = mapping['properties'][prop]
                                cats[class_num] = mapping['classes'][class_num]
                                annotation = {}
                                annotation['id'] = annid
                                annotation['image_id'] = imgid
                                annotation['category_id'] = class_num
                                annotation['segmentation'] = ann['segmentation']
                                annotation['area'] = ann['bbox'][2] * ann['bbox'][3]
                                annotation['bbox'] = ann['bbox']
                                annotation['iscrowd'] = 0
                                ### Begin GEOCOCO fields
                                annotation['keypoints'] = []
                                annotation['num_keypoints'] = 0
                                annotation['bbox_rotated'] = []
                                annotation['object_center'] = [ann['centroid'][1], ann['centroid'][0]]
                                annotation['bbox_geo'] = []
                                annotation['bbox_rotated_geo'] = []
                                annotation['object_center_geo'] = []
                                annotation['keypoints_geo'] = []
                                annotation['classification'] = 'Undefined'
                                if 'keypoints' in ann:
                                    annotation['keypoints'] = ann['keypoints']
                                    annotation['num_keypoints'] = len(ann['keypoints'])
                                    if calc_geo:
                                        annotation['keypoints_geo'] = img_geo.pixel_to_geo(ann['keypoints'])
                                if calc_rotated_bbox:
                                    obj_width = ann['size'][0] / metadata['sensor']['meters_per_pixel']
                                    obj_length = ann['size'][1] / metadata['sensor']['meters_per_pixel']
                                    rotation = (math.degrees(ann['rotation'][2]) - metadata['sensor']['azimuth']) % 360
                                    annotation['bbox_rotated'] = [ann['centroid'][1], ann['centroid'][0], obj_width, obj_length, rotation]
                                    if calc_geo:
                                        bbox_rotated_coords = get_rotated_bbox_coordinates(*annotation['bbox_rotated'])
                                        annotation['bbox_rotated_geo'] = img_geo.pixel_to_geo(bbox_rotated_coords)
                                if calc_geo:
                                    annotation['bbox_geo'] = img_geo.pixel_to_geo(annotation['bbox'])
                                    annotation['object_center_geo'] = img_geo.pixel_to_geo(annotation['object_center'])
                                if 'classification' in ann:
                                    annotation['classification'] = ann['classification']
                                annid += 1
                                if not first:
                                    of.write(', ')
                                json.dump(annotation, of)
                                first = False
                                break
            imgdata = {
                'id':               imgid, 
                'file_name':        metadata['filename'], 
                'date_captured':    metadata['date'], 
                'license':          0, 
                'width':            img_width,
                'height':           img_height}
            cocodata['images'].append(imgdata)
            imgid += 1
        sorted_cats = dict(sorted(cats.items()))
        for class_num, cat in sorted_cats.items():
            cocodata['categories'].append({
                'id':               class_num, 
                'name':             cat[-1],
                'supercategory':    cat[0]
            })
        of.write('], ')
        of.write(f'"info": {json.dumps(cocodata["info"])}, ')
        of.write(f'"licenses": {json.dumps(cocodata["licenses"])}, ')
        of.write(f'"images": {json.dumps(cocodata["images"])}, ')
        of.write(f'"categories": {json.dumps(cocodata["categories"])}')
        of.write('}')