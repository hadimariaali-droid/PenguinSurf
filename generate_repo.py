import os
import hashlib
import xml.etree.ElementTree as ET
from xml.dom import minidom

# --- Configuration ---
# The directory where the video addon is located
ADDON_DIR = "plugin.video.penguinsurf"
# The directory where the repository files will be generated
REPO_FILES_DIR = "repository_files"
# The ID of the repository addon
REPO_ID = "repository.penguinsurf"

def generate_addons_xml():
    """
    Reads the addon.xml from the video addon and generates the repository's addons.xml.
    """
    print(f"--- Generating addons.xml for {ADDON_DIR} ---")
    
    # 1. Read the video addon's addon.xml
    addon_xml_path = os.path.join(ADDON_DIR, "addon.xml")
    if not os.path.exists(addon_xml_path):
        print(f"Error: Addon XML not found at {addon_xml_path}")
        return False

    try:
        # Parse the video addon's addon.xml
        addon_tree = ET.parse(addon_xml_path)
        addon_root = addon_tree.getroot()
        
        # 2. Create the root element for the repository's addons.xml
        addons_root = ET.Element("addons")
        
        # 3. Copy the video addon's XML content into the repository's addons.xml
        # We need to remove the 'assets' tag as it's not needed in the repository index
        # and copy the rest of the addon's XML structure.
        
        # Create a deep copy of the addon element
        addon_element = ET.Element(addon_root.tag, addon_root.attrib)
        for child in addon_root:
            if child.tag != "extension" or child.attrib.get("point") != "xbmc.addon.metadata":
                addon_element.append(child)
            else:
                # Copy metadata extension, but remove assets
                metadata_element = ET.Element(child.tag, child.attrib)
                for meta_child in child:
                    if meta_child.tag != "assets":
                        metadata_element.append(meta_child)
                addon_element.append(metadata_element)
        
        addons_root.append(addon_element)
        
        # 4. Add the repository addon's own metadata (if needed, but usually not)
        # For simplicity, we'll only include the video addon for now.
        
        # 5. Write the final addons.xml file
        addons_xml_path = os.path.join(REPO_FILES_DIR, "addons.xml")
        
        # Use minidom to pretty-print the XML
        xml_string = ET.tostring(addons_root, encoding="utf-8")
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="    ", encoding="utf-8")
        
        # Remove the extra blank lines minidom adds
        pretty_xml_lines = pretty_xml.decode().split('\n')
        clean_xml = '\n'.join([line for line in pretty_xml_lines if line.strip()])
        
        with open(addons_xml_path, "w", encoding="utf-8") as f:
            f.write(clean_xml)
            
        print(f"Successfully created {addons_xml_path}")
        return True

    except Exception as e:
        print(f"An error occurred during XML generation: {e}")
        return False

def generate_md5_checksum():
    """
    Calculates the MD5 checksum of addons.xml and writes it to addons.xml.md5.
    """
    print("--- Generating MD5 Checksum ---")
    addons_xml_path = os.path.join(REPO_FILES_DIR, "addons.xml")
    md5_path = os.path.join(REPO_FILES_DIR, "addons.xml.md5")
    
    if not os.path.exists(addons_xml_path):
        print(f"Error: addons.xml not found at {addons_xml_path}")
        return False
        
    try:
        hash_md5 = hashlib.md5()
        with open(addons_xml_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        checksum = hash_md5.hexdigest()
        
        with open(md5_path, "w") as f:
            f.write(checksum)
            
        print(f"Successfully created {md5_path} with checksum: {checksum}")
        return True
        
    except Exception as e:
        print(f"An error occurred during MD5 generation: {e}")
        return False

def main():
    """
    Main function to run the repository generation process.
    """
    # Ensure the repository files directory exists
    os.makedirs(REPO_FILES_DIR, exist_ok=True)
    
    if generate_addons_xml():
        generate_md5_checksum()
    
    print("--- Repository Generation Complete ---")

if __name__ == "__main__":
    main()
