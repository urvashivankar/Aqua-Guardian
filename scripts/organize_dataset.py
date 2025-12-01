import os
import shutil
from pathlib import Path

def organize_dataset():
    # Define source and target directories
    base_dir = Path(r"C:\Users\Urvashi\OneDrive\Desktop\AQUA_guardian_project\data")
    source_dir = base_dir / "dataset_raw"
    target_dir = base_dir / "dataset"

    # Define category mappings (source folder name -> target folder name)
    # This handles renaming and mapping multiple sources to one target
    category_mapping = {
        "clean water": "clean",
        "oil spill": "oil_spill",
        "plastic": "plastic",
        "sewage": "sewage"
    }

    # Create target directory if it doesn't exist
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print(f"Created target directory: {target_dir}")

    # Create target category directories
    for category in category_mapping.values():
        (target_dir / category).mkdir(exist_ok=True)

    # Walk through the source directory
    for item in source_dir.iterdir():
        if item.is_dir():
            source_category = item.name
            
            # Determine target category
            target_category = category_mapping.get(source_category)
            if not target_category:
                print(f"Skipping unknown category folder: {source_category}")
                continue

            target_category_path = target_dir / target_category
            print(f"Processing {source_category} -> {target_category}...")

            # Walk through files in the source category folder (recursively)
            for root, _, files in os.walk(item):
                for file in files:
                    source_file_path = Path(root) / file
                    
                    # Skip non-image files if necessary (optional, but good practice)
                    if file.lower().endswith(('.ds_store', '.ini', '.txt')): # Add extensions to ignore
                         continue

                    # Handle duplicate filenames
                    target_file_path = target_category_path / file
                    counter = 1
                    while target_file_path.exists():
                        name_stem = Path(file).stem
                        suffix = Path(file).suffix
                        target_file_path = target_category_path / f"{name_stem}_{counter}{suffix}"
                        counter += 1
                    
                    # Copy the file
                    try:
                        shutil.copy2(source_file_path, target_file_path)
                        # print(f"Copied: {source_file_path.name} -> {target_file_path.name}")
                    except Exception as e:
                        print(f"Error copying {source_file_path}: {e}")
            
            print(f"Finished processing {source_category}")

    print("\nDataset organization complete!")
    print(f"New dataset location: {target_dir}")

    # Print summary
    print("\nSummary of files in new dataset:")
    for category in category_mapping.values():
        count = len(list((target_dir / category).glob('*')))
        print(f"  {category}: {count} files")

if __name__ == "__main__":
    organize_dataset()
