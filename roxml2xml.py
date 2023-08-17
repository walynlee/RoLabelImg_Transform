import xml.etree.ElementTree as ET
import math
import os

def rotate_point(point, angle, origin):
    angle_rad = math.radians(angle)
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
    qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
    return qx, qy

def rotate_bbox(bbox, angle, origin):
    rotated_bbox = []
    for point in bbox:
        rotated_point = rotate_point(point, angle, origin)
        rotated_bbox.append(rotated_point)
    return rotated_bbox

def process_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Iterate through each object in the XML and update the bounding box coordinates
    for obj in root.findall('object'):
        robndbox = obj.find('robndbox')
        if robndbox is not None:
            cx = float(robndbox.find('cx').text)
            cy = float(robndbox.find('cy').text)
            w = float(robndbox.find('w').text)
            h = float(robndbox.find('h').text)
            angle = float(robndbox.find('angle').text)

            rotated_bbox = rotate_bbox([(cx, cy), (cx + w, cy), (cx + w, cy + h), (cx, cy + h)], angle, (cx, cy))
            min_x = min(rotated_bbox[0][0], rotated_bbox[3][0])
            max_x = max(rotated_bbox[1][0], rotated_bbox[2][0])
            min_y = min(rotated_bbox[0][1], rotated_bbox[1][1])
            max_y = max(rotated_bbox[2][1], rotated_bbox[3][1])

            # Create new <bndbox> elements
            bndbox = ET.SubElement(obj, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            ymin = ET.SubElement(bndbox, 'ymin')
            xmax = ET.SubElement(bndbox, 'xmax')
            ymax = ET.SubElement(bndbox, 'ymax')

            # Set the values for <bndbox> elements
            xmin.text = str(int(min_x))
            ymin.text = str(int(min_y))
            xmax.text = str(int(max_x))
            ymax.text = str(int(max_y))

            # Remove the <robndbox> element
            obj.remove(robndbox)

    # Save the modified XML back to the original file
    tree.write(xml_path)

# Specify the input directory containing XML files and the output directory
input_directory = r'F:\walyn\walyn\nanodet\retinal_hole\val_xml'


# Iterate through each XML file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.xml'):
        xml_path = os.path.join(input_directory, filename)
        print(xml_path)
        process_xml(xml_path)

print("Processing complete.")