import os
import sys
import shutil

def process_input(input_str: str) -> list[str]:
    """
    Resolves the multi-line inputs from GitHub Actions
    """
    if not input_str:
        return []
    # filters empty lines, strips the spaces for every lines
    return [line.strip() for line in input_str.splitlines() if line.strip()]

def get_target_path(source_path: str, build_path: str) -> str:
    """
    Get the target path for copying a file or directory.
    
    Args:
        source_path: The source file or directory path
        build_path: The base build path where files will be copied
        
    Returns:
        The target path where the source should be copied
    """
    if os.path.isdir(source_path):
        # For directories, normalize the path to ensure basename works correctly
        # even with trailing slashes
        # Remove both forward and backward slashes
        normalized_path = source_path.rstrip('/\\')
        dir_name = os.path.basename(normalized_path)
        return os.path.join(build_path, dir_name)
    else:
        # For files, copy directly to the build path
        return build_path

def main():
    try:
        build_path = os.environ['BUILD_PATH']
        included_files_str = os.environ.get('INCLUDED_FILES', '')
        entry_file = os.environ['PYSTAND_ENTRY_FILE']
        app_name = os.environ['APPLICATION_NAME']
        print("=== Debug: All environment variables accessed successfully ===")
    except KeyError as e:
        print("Environment variable missing: ", e)
        sys.exit(1)

    items_to_copy = process_input(included_files_str)

    print("=== Processed Items ===")
    for item in items_to_copy:
        print(f'Item: "{item}"')
    print("=== End Processed Items ===")

    try:
        for item in items_to_copy:
            print(f"Processing: {item}")
            if not os.path.exists(item):
                print(f"::warning file={item}::Item does not exist, skipped.")
                continue

            target_path = get_target_path(item, build_path)
            if os.path.isdir(item):
                # Copies the source directory 'item' to the directory under the build dir with the name name.
                # For example, copies 'src/assets' to 'build_path/assets/'
                print(f"Copying directory '{item}' to '{target_path}'")
                shutil.copytree(item, target_path, dirs_exist_ok=True)
            elif os.path.isfile(item):
                print(f"Copying file '{item}' to '{target_path}'")
                shutil.copy2(item, target_path)
            else:
                print(f"::warning file={item}::Item is not a regular file or directory, skipped.")

        # copy and rename PyStand entry file
        entry_dest = os.path.join(build_path, f"{app_name}.py")
        print(f"Copying entry file '{entry_file}' to '{entry_dest}'")
        shutil.copy2(entry_file, entry_dest)

        print("=== All items processed successfully! ===")
    except Exception as e:
        print(f"::error::An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
