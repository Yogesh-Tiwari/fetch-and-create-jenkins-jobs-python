# Jenkins Job Manager

## Overview

This repository contains Python scripts designed to interact with Jenkins, a popular open-source automation server. The scripts allow you to retrieve, create Jenkins jobs and interact with plugins using the Jenkins REST API.

## Contents

- **scripts Directory**: Contains Python scripts for managing Jenkins jobs.
  - `get-jobs.py`: Retrieves jobs from Jenkins and saves their configuration as XML files.
  - `create-jobs.py`: Creates Jenkins jobs from XML configuration files.
  - `install-plugins.py`: Installs plugins in Jenkins.
- **Secrets Configuration**: The file `secrets/secret.json` contains sensitive configuration details such as Jenkins URL, username, password (or personal access token), and the folder name where job XML files are stored or created.

## Setup

1. **Install Dependencies**:

   Ensure you have the necessary Python package installed. This project uses `python-jenkins`, a Python wrapper for the Jenkins REST API. Install it using pip:

   pip install python-jenkins

2. **Configure Secrets**:

   Create a file named `secret.json` inside the `secrets` directory with the following structure:

   {
     "url": "http://your-jenkins-url",
     "username": "your-username",
     "password_or_token": "your-password-or-token",
     "config_folder": "path/to/jobs/folder",
     "plugins": ["plugin-name-01", "plugin-name-02", "plugin-name-n"]
   }

   Make sure to replace the placeholders with your actual Jenkins URL, credentials, and desired folder path.

## Usage

1. **Retrieve Jenkins Jobs**:

   To retrieve Jenkins jobs and save their XML configurations, run:

   `python scripts/get-jobs.py`


   This will fetch jobs from Jenkins and store the XML files in the folder specified in the `secret.json` file.

2. **Create Jenkins Jobs**:

   To create Jenkins jobs from existing XML files, use:


   `python scripts/create-jobs.py`


   The script will read XML files from the folder specified in `secret.json` and create jobs in Jenkins based on those configurations.

3. **Install Plugins**:

   To install plugins in Jenkins, use:

   `python scripts/install-plugins.py`


   This will install the plugins specified in `secret.json` on the Jenkins server.

4. **Skip SSL Verification**:

   If you want to skip SSL verification, you can do so by adding the following parameter to the `connect_to_jenkins` function:

   `server = connect_to_jenkins(config, skip_ssl_verification=True)`

   This will allow you to connect to Jenkins without verifying the SSL certificate.

## Known Issues:
   Error while installing plugins `(python-jenkins version 1.8.2)`:
   To resolve, edit the files specified in the PR to resolve the issue with installing plugins: https://review.opendev.org/c/jjb/python-jenkins/+/719059.
   To find the installed plugin path, we need to use the following command: "pip show python-jenkins" and refer to Location in the output.


## Git Bonus Tip

If you want to temporarily ignore changes to the `secret.json` file and avoid tracking its modifications in Git, use:

`git update-index --assume-unchanged secrets/secret.json`

To start tracking changes to the `secret.json` file again, run:

`git update-index --no-assume-unchanged secrets/secret.json`

## Contributing
If you have any suggestions or improvements for this project, feel free to submit a pull request or open an issue. Contributions and feedback are welcome!

Thank you for using Jenkins Job Manager. Happy coding!
