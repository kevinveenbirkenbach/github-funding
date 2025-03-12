import os
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Copy FUNDING.yml into .github folders in all first-level subdirectories."
    )
    parser.add_argument(
        "target_directory",
        help="Path to the directory containing subfolders"
    )
    parser.add_argument(
        "funding_file",
        nargs="?",
        default=None,
        help="Path to the FUNDING.yml file to be copied. If not provided, the FUNDING.yml from the script's directory is used."
    )
    args = parser.parse_args()

    # Wenn kein FUNDING.yml-Pfad angegeben wurde, verwende den aus dem Skriptverzeichnis
    if args.funding_file is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.funding_file = os.path.join(script_dir, "FUNDING.yml")

    # Überprüfen, ob das FUNDING.yml File existiert
    if not os.path.isfile(args.funding_file):
        print(f"Error: {args.funding_file} does not exist or is not a file.")
        return

    # Iteriere über alle Einträge im Zielverzeichnis
    for entry in os.listdir(args.target_directory):
        full_path = os.path.join(args.target_directory, entry)
        if os.path.isdir(full_path):
            github_dir = os.path.join(full_path, ".github")
            os.makedirs(github_dir, exist_ok=True)
            destination = os.path.join(github_dir, "FUNDING.yml")
            try:
                shutil.copy2(args.funding_file, destination)
                print(f"Copied FUNDING.yml to {destination}")
            except Exception as e:
                print(f"Failed to copy to {destination}: {e}")

if __name__ == "__main__":
    main()
