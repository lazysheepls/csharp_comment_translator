import os  

def find_cs_files(directory):  
    # Validate if directory exists  
    if not os.path.exists(directory):  
        print(f"Error: Directory '{directory}' does not exist.")  
        return  
    
    cs_files = []  # List to store paths to .cs files  
    
    try:  
        # Walk through the directory  
        for root, _, files in os.walk(directory):  
            # Skip 'obj' folders  
            if 'obj' in os.path.normpath(root).split(os.sep):  
                continue  
                
            for file in files:  
                # Check if file ends with .cs and not with Designer.cs  
                if file.endswith('.cs') and not file.endswith('Designer.cs'):  
                    # Construct the full file path  
                    full_path = os.path.join(root, file)  
                    cs_files.append(full_path)  
                    print(full_path)  

        # Print the total number of .cs files found  
        print(f"\nTotal number of .cs files found: {len(cs_files)}")  
    
    except Exception as e:  
        print(f"An error occurred: {str(e)}")  

# Example usage:  
# Use raw string for Windows paths  
# path_to_search = r"C:\Your\Path\Here"  # Replace with your actual path  
# OR use forward slashes  
# path_to_search = "C:/Your/Path/Here" 
