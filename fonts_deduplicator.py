import os

def function_caller(directory):
    path_to_files = os.path.abspath(directory)

    if not os.path.isdir(path_to_files):
        print(f"Error: {path_to_files} is not a valid directory.")
        return

    # list to iterate, set for O(1) existence checks
    file_list = os.listdir(path_to_files)
    files_present = set(file_list)

    for file_name in file_list:
        # Skip if the file was already deleted/renamed in a previous iteration
        if file_name not in files_present:
            continue

        for i in range(1, 9):
            target = f"({i})"
            cleanup_and_rebase_fonts(target, file_name, files_present, path_to_files)

        target = " "
        cleanup_and_rebase_fonts(target, file_name, files_present, path_to_files)

def cleanup_and_rebase_fonts(target, file_name, files_present, path_to_files):
    if target in file_name:
        clean_name = file_name.replace(target, "")
                
        # Logic: If original exists, delete duplicate. Else, rename to original.
        if clean_name in files_present:
            if clean_name != file_name:
                try:
                    os.remove(os.path.join(path_to_files, file_name))
                    files_present.discard(file_name)
                    print(f"Deleted duplicate: {file_name}")
                except OSError as e:
                    print(f"Error deleting {file_name}: {e}")
        else:
            try:
                old_path = os.path.join(path_to_files, file_name)
                new_path = os.path.join(path_to_files, clean_name)
                os.rename(old_path, new_path)
                        
                # Update the set so (i+1) files find this as the "original"
                files_present.discard(file_name)
                files_present.add(clean_name)
                print(f"Renamed {file_name} -> {clean_name}")
            except OSError as e:
                print(f"Error renaming {file_name}: {e}")



def main():
    target_dir = "../../allFonts"
    print(f"Processing directory: {os.path.abspath(target_dir)}")
    function_caller(target_dir)
    print("Task finished.")

if __name__ == "__main__":
    main()