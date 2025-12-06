import zipfile
import os

pptx_file = r'c:\Users\kevin\Documents\Python\Level_30_erreicht\Level 30 erreicht -xml.pptx'
extract_path = r'c:\Users\kevin\Documents\Python\Level_30_erreicht\pptx_extracted'

# Extract the PPTX file
zipfile.ZipFile(pptx_file).extractall(extract_path)

# List all extracted files
for root, dirs, files in os.walk(extract_path):
    for file in sorted(files):
        print(os.path.relpath(os.path.join(root, file), extract_path))
