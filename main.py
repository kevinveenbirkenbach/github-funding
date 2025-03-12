#!/usr/bin/env python3
import os
import shutil
import argparse

def parse_funding_yaml(file_path):
    """
    Parse a simple FUNDING.yml file with key: value entries.
    Returns a dictionary.
    """
    funding = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                # Skip empty lines and comments
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                    funding[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return funding

def generate_badges(funding):
    """
    Generate a list of badge markdown strings based on funding entries.
    """
    badges = []
    if "github" in funding:
        badges.append({
            "badge": f"[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/{funding['github']})",
            "identifier": "github.com/sponsors"
        })
    if "patreon" in funding:
        badges.append({
            "badge": f"[![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/{funding['patreon']})",
            "identifier": "patreon.com"
        })
    if "buy_me_a_coffee" in funding:
        badges.append({
            "badge": f"[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/{funding['buy_me_a_coffee']})",
            "identifier": "buymeacoffee.com"
        })
    if "custom" in funding:
        custom_link = funding["custom"]
        if "paypal" in custom_link.lower():
            badges.append({
                "badge": f"[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)]({custom_link})",
                "identifier": "paypal"
            })
        else:
            badges.append({
                "badge": f"[![Custom](https://img.shields.io/badge/Donate-Custom-lightgrey)]({custom_link})",
                "identifier": custom_link
            })
    return badges

def update_readme(repo_path, badge_entries):
    """
    Update (or create) the README.md file in the repository.
    Missing badges will be inserted right after the first H1 (# Title) line.
    Each badge is checked individually by its identifier.
    """
    readme_path = os.path.join(repo_path, "README.md")
    missing_badges = []

    # Read existing README.md content if it exists
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = ""

    # Check each badge if its identifier is present in the README content
    for entry in badge_entries:
        if entry["identifier"].lower() not in content.lower():
            missing_badges.append(entry["badge"])

    # If no missing badges, nothing to do
    if not missing_badges:
        return

    badges_str = " ".join(missing_badges) + "\n\n"
    new_content = []

    # If README exists, insert missing badges after first H1 header
    if content:
        lines = content.splitlines(keepends=True)
        header_found = False
        for line in lines:
            new_content.append(line)
            if not header_found and line.lstrip().startswith("# "):
                new_content.append(badges_str)
                header_found = True
        # If no header is found, prepend a default header and the badges.
        if not header_found:
            new_content.insert(0, f"# Repository\n{badges_str}\n")
    else:
        # Create a new README.md with default title and badges.
        repo_name = os.path.basename(os.path.abspath(repo_path))
        new_content = [f"# {repo_name}\n\n", badges_str]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("".join(new_content))
    
    print(f"Updated README.md in {repo_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Copy FUNDING.yml into .github folders in all first-level subdirectories and optionally update README.md with funding badges."
    )
    parser.add_argument(
        "target_directory",
        help="Path to the directory containing subfolders (each subfolder is a repository)"
    )
    parser.add_argument(
        "funding_file",
        nargs="?",
        default=None,
        help="Path to the FUNDING.yml file to be copied. If not provided, the FUNDING.yml from the script's directory is used."
    )
    parser.add_argument(
        "-b", "--badges",
        action="store_true",
        help="Generate and update README.md with funding badges."
    )
    args = parser.parse_args()

    # Use FUNDING.yml from the script's directory if not provided
    if args.funding_file is None:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        args.funding_file = os.path.join(script_dir, "FUNDING.yml")

    # Check if the FUNDING.yml file exists
    if not os.path.isfile(args.funding_file):
        print(f"Error: {args.funding_file} does not exist or is not a file.")
        return

    # If badges flag is set, parse FUNDING.yml to generate badge entries.
    badge_entries = []
    if args.badges:
        funding_data = parse_funding_yaml(args.funding_file)
        badge_entries = generate_badges(funding_data)

    # Iterate over all first-level subdirectories in target_directory
    for entry in os.listdir(args.target_directory):
        repo_path = os.path.join(args.target_directory, entry)
        if os.path.isdir(repo_path):
            # Create .github directory and copy FUNDING.yml
            github_dir = os.path.join(repo_path, ".github")
            os.makedirs(github_dir, exist_ok=True)
            destination = os.path.join(github_dir, "FUNDING.yml")
            try:
                shutil.copy2(args.funding_file, destination)
                print(f"Copied FUNDING.yml to {destination}")
            except Exception as e:
                print(f"Failed to copy to {destination}: {e}")
            
            # Update README.md with missing badges if the flag is set.
            if args.badges:
                update_readme(repo_path, badge_entries)

if __name__ == "__main__":
    main()
