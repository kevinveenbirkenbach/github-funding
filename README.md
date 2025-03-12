# GitHub Funding 💰✨

A Python script that automates GitHub Sponsoring setup by creating a `.github` folder and deploying a `FUNDING.yml` file into every first-level subdirectory of a target directory. This enables GitHub Sponsoring for each repository in that folder. 🚀📁

## Installation 🔧

You can install this tool using [Kevin's Package Manager](https://github.com/kevinveenbirkenbach/package-manager) under the alias `gihufu`. ⚙️💻

## Usage 🎯

This script is contained in `main.py` and accepts the following parameters:

- **target_directory**:  
  The directory containing all your GitHub repositories (each repository should be located in its own first-level subfolder).  
  _Example:_ `/path/to/your/repos` 📂

- **funding_file** (optional):  
  The path to the `FUNDING.yml` file you want to deploy. If not provided, the script will use the `FUNDING.yml` from the same directory where the script is located.  
  _Example:_ `/path/to/your/FUNDING.yml` 📝

### Example Command 🏃‍♂️

```bash
python main.py /path/to/target_directory /path/to/FUNDING.yml
```

If you omit the `funding_file` argument, the script defaults to the `FUNDING.yml` in its own directory. 🔄

## Assumptions 🤔

- It is assumed that **all GitHub repositories are in the same subfolder**. The script will deploy the `FUNDING.yml` file into the `.github` folder of each repository on the first level of the given target directory, setting up GitHub Sponsoring for each. 🔍📥

## Author 👨‍💻

Developed by [Kevin Veen-Birkenbach](https://www.veen.world/) 🌐✨

## License 📜

This project is licensed under the MIT License. 🆓

## Acknowledgments 🙏

This script was created with the help of [ChatGPT](https://chat.openai.com/) 🤖💡  
For more context, please refer to the [conversation that led to its creation](https://chatgpt.com/share/67d1d6b8-b828-800f-936c-9e8b5b79dbd9). 💬
