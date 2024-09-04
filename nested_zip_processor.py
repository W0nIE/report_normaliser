import os
import zipfile

def extract_zip(zip_path, extract_to):
    """
    Extracts a zip file to a specified directory.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Extracted: {zip_path} to {extract_to}")
    except zipfile.BadZipFile:
        print(f"Error: Bad ZIP file {zip_path}")
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")

def add_prefix_to_csv_files(directory):
    """
    Adds a prefix to all .csv files in the given directory based on the folder name one level above.
    """
    for root, _, files in os.walk(directory):
        # Get the parent folder name for each .csv file
        parent_folder = os.path.basename(root)  # This is the direct parent of the .csv file
        grandparent_folder = os.path.basename(os.path.dirname(root))  # Get the grandparent folder (one level above)

        for file in files:
            if file.endswith('.csv'):
                old_path = os.path.join(root, file)
                # Add the grandparent folder name as a prefix to the file name
                new_name = f"{parent_folder}-{file}"  # Prefixing with the direct parent folder name
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed {old_path} to {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

def process_directory(directory):
    """
    Recursively processes the directory to extract nested zip files and add prefixes to .csv files.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if zipfile.is_zipfile(file_path):
                extract_to = root  # Extract in the current directory
                extract_zip(file_path, extract_to)
                try:
                    os.remove(file_path)  # Delete the original zip file after extraction
                    print(f"Deleted ZIP file: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    # After all zips are processed, add prefixes to CSV files
    add_prefix_to_csv_files(directory)

def main():
    # Request the directory path from the user as a command line argument
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory>")
        return

    directory = sys.argv[1]

    if not os.path.exists(directory):
        print(f"Error: The directory {directory} does not exist.")
        return

    if not os.path.isdir(directory):
        print(f"Error: The path {directory} is not a directory.")
        return

    # Process the directory recursively to extract nested zips, rename CSVs, and delete zips
    process_directory(directory)

if __name__ == "__main__":
    main()

