Please be aware that this is a general guide, and your environment may require additional steps or configurations. 

## Prerequisites

- A Linux environment
- Python 3.6 or newer installed
- Google Cloud SDK installed
- pip (Python package installer) installed
- An account on Google Cloud Platform with necessary permissions
- A Google Cloud Project with Compute Engine API enabled
- A Service Account key file

## Steps to Deploy and Execute

1. **Clone the repository** 
   
   Open a terminal and navigate to the directory where you want to clone the repository. Use the `git clone` command followed by the URL of the repository. For example:
   
   ```
   git clone https://github.com/paduartesre/search-instances-gcp.git
   ```
   
2. **Navigate to the project directory**
   
   After the repository is cloned, navigate to the project directory. Replace `search-instances-gcp` with the name of your repository, if changed.
   
   ```
   cd your_repository or search-instances-gcp
   ```

3. **Install the required Python packages**

   This script requires several Python packages. Install them using the `pip install` command. 

   ```
   pip install -r requirements.txt
   ```
   
4. **Set up Google Cloud authentication**

   You need to authenticate your Google Cloud SDK with Google Cloud. Use the `gcloud auth login` and `gcloud auth application-default login` command and follow the instructions. Before need to install Google Cloud SDK with the command `curl https://sdk.cloud.google.com | bash`.

   ``` 
   gcloud auth login
   gcloud auth application-default login
   ```

5. **Set the Google Cloud project**

   Set the Google Cloud project to the one where you want to run this script. Replace `your-gcp-project-id` with your actual project ID.

   ```
   gcloud config set project your-gcp-project-id
   ```

6. **Execute the Python script**

   Run the Python script using the `python` or `python3` command followed by the name of the Python script file. Replace `your-python-script.py` with the name of your Python script file.

   ```
   python3 scripts/search-instances.py
   ```

That's it! You have deployed and executed the Python script in your local Linux environment.

## Troubleshooting

- If you have both Python 2 and Python 3 installed, you may need to use `python3` and `pip3` instead of `python` and `pip`.
- If you get a permission error when running `pip install`, try using `pip install --user` to install the packages for the current user only, or use `sudo pip install` to install packages system-wide (not recommended for most users).
- If the Python script does not run, check if the execution permission is set. Use `chmod +x search-instances.py` to add execution permission.

## Contributing

Contributions are welcome! Please read the [contributing guide](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE.md).