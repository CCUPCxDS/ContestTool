# Contest Tool 

Version: `9`

## Description

Some useful tools for maintaining contests.

Specifically, this tool is designed to generate team information and accounts for the [DOMjudge](https://www.domjudge.org/) system.

After version `9` of this tool, we consider the user only use domjudge with version `9.0.0` or higher.

## Usage

First, you need to fill the info of `team.csv` (copy from `sample_team.csv`), the category row must be the external ID of specific category.

![](./category.png)

Because the tool will send http requests to the DOMjudge API, you need to install the `requests` library in advance.

```bash
pip install requests
```

Then, run the command

```bash
python setup.py -u <api_url> -a <account> -p <password> -f <file_path>
```

For `<api_url>`, you should keep it clean, like `ccupc.csie.io`
For `<account>`, you need to provide the account name of the DOMjudge API. (e.g. `admin`)
For `<password>`, you need to provide the password of the DOMjudge API. (e.g. `password`)
For `<file_path>`, you need to provide the path to the `team.csv` file. (e.g. `./team.csv`)

After running the command, the tool will generate team information and accounts for the DOMjudge system and import them into the system automatically.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
