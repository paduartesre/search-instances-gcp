from google.cloud import compute_v1
from google.auth import default
import os
import uuid
import time
import click
import emoji
import datetime
import concurrent.futures
from colorama import Fore, Style
from jinja2 import Template
import warnings
from urllib3.exceptions import DependencyWarning
warnings.simplefilter(action="ignore", category=DependencyWarning)
import google.auth
from google.auth.transport.requests import Request
from google.cloud import compute_v1
import json

# Load gcloud credentials
creds, project = google.auth.default()

# Create a Compute Engine client using the loaded credentials
compute_client = compute_v1.InstancesClient(credentials=creds)

with open('data.json', 'r') as file:
    data = json.load(file)

# Search for registered projects in the variables listed in the data.json file
projects = data['projects']
zone_list_us_central = data['zone_list_us_central'] 
zone_list_us_east = data['zone_list_us_east'] 
zone_list_br = data['zone_list_br'] 
zone_list_us_south = data['zone_list_us_south'] 
zone_list_us_west = data['zone_list_us_west']

# Generate a unique ID for the HTML file
html_file_id = str(uuid.uuid4())

client = compute_v1.InstancesClient()
output_list = []

# Begin Process
output = """
------------------------------------------------------------
      \033[31m|\033[32m|\033[33m|\033[34m| \033[37m Search instances on Google Cloud \033[31m|\033[32m|\033[33m|\033[34m|
\033[37m------------------------------------------------------------
"""

# Show output
print(output)
time.sleep(1)

print("Projects inside of organization \033[1m'my-org.co'\033[0m  \n")

for i, project in enumerate(projects):
    print(f"{i+1}. {project['name']}")

# Ask the user if they want to search in all projects
search_all_projects = input("\nDo you want to search for instances in all projects? (S/N): ")
output = "\n-----------------------------------------------------------\n\n"
output += f"Do you want to search for instances in all projects? {search_all_projects}\n"

# Show the output
print(output)

# List all instances in all regions and zones defined in the variables
zone_list = zone_list_us_south + zone_list_br + zone_list_us_central + zone_list_us_east + zone_list_us_west

if search_all_projects.upper() == "S":
    msg1 = f"Locating resources in the projects..."
    text_em1 = f"\033[33m\u21A9\033[0m {msg1}"
    print(text_em1)
    print()
    for project in projects:
        project_id = project['id']
        for zone in zone_list:
            instances = client.list(request={"project": project_id, "zone": zone})
            if not instances:
                print(f"There are no instances to display in the project {project['name']} in the zone {zone}")
                continue
            for instance in instances:
                output_list.append(f"<strong>Instance name:</strong> {instance.name}")
                for interface in instance.network_interfaces:
                    output_list.append(f"<strong>Internal IP address:</strong> {interface.network_i_p}")
                    for access_config in interface.access_configs:
                        nat_ip = access_config.nat_i_p
                        if nat_ip:
                            output_list.append(f"<strong>External IP address:</strong> <span style='color:red'>{nat_ip}</span>")
                        else:
                            output_list.append(f"<strong>External IP address:</strong> {nat_ip}")           
                output_list.append(f"<strong>Zone:</strong> {os.path.basename(instance.zone)}")
                output_list.append(f"<strong>Project:</strong> {project['name']}")
                output_list.append("---------------------------------------------------------")
                output_list.append("")
                inst = f"{instance.name}"
                texto_inst = f"\033[32m\u2714\033[0m {inst}"
                print(texto_inst)
                time.sleep(1)

else:
    choice = int(input("Enter the project number: "))
    project_id = projects[choice-1]["id"]
    print()
    msg1 = f"Locating resources in the project {project_id}..."
    text_em1 = f"\033[33m\u21A9\033[0m {msg1} \n"
    print(text_em1)
    

    # Look for instances in the selected project
    output_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for zone in zone_list:
                futures.append(executor.submit(client.list, {"project": project_id, "zone": zone}))
            for future in concurrent.futures.as_completed(futures):
                instances = future.result()
                if not instances:
                    continue
                for instance in instances:
                    output_list.append(f"<strong>Instance name:</strong> {instance.name}")
                    for interface in instance.network_interfaces:
                        output_list.append(f"<strong>Internal IP address:</strong> {interface.network_i_p}")
                        for access_config in interface.access_configs:
                            nat_ip = access_config.nat_i_p
                            if nat_ip:
                                output_list.append(f"<strong>External IP address:</strong> <span style='color:red'>{nat_ip}</span>")
                            else:
                                output_list.append(f"<strong>External IP address:</strong> {nat_ip}")           
                    output_list.append(f"<strong>Zone:</strong> {os.path.basename(instance.zone)}")
                    output_list.append(f"<strong>Project:</strong> {project_id}")
                    output_list.append("---------------------------------------------------------")
                    output_list.append("")
                    time.sleep(1)
                    inst = f"{instance.name}"
                    texto_inst = f"\033[32m\u2714\033[0m {inst}"
                    print(texto_inst)

# Generate a unique ID for the HTML file
html_file_id = str(uuid.uuid4())

# Define the name of the HTML file
html_file_name = f"outputs/output_{project_id}_{html_file_id}.html"

now = datetime.datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")

# Generate the HTML content from the output list
marker = '<img src="../images/mark.png" alt="mark">'
worldwide = '<img src="../images/worldwide.png" alt="worldwide">'
ipexternal = '<img src="../images/ipexternal.png" alt="ipexternal">'
ipinternal = '<img src="../images/ipinternal.png" alt="ipinternal">'
project   = '<img src="../images/project.png" alt="project">'
logo      = '<img src="../images/logo.png" alt="logo">'      # Download your logo inside folder images with name logo.png
html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>GCE Instances</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>
    <div class="logo">
      <img src="../images/logo.png" alt="Logo" width="128">
    </div>
    <div class="title">
      <h1>Instances existing in the project {project_id}</h1>
      <p align="center">Date and time of file generation: {date_time}<br></p>
    </div>
  </header>
  <ul>
    {"".join([f"<li>{worldwide} {item}</li>" if 'Zone' in item else f"<li>{ipexternal} {item}</li>" if 'External IP address' in item else f"<li>{ipinternal} {item}</li>" if 'Internal IP address' in item else f"<li>{project} {item}</li>" if 'Project' in item else f"<li>{marker} {item}</li>" if 'Instance Name' in item else f"<li>{item}</li>" for item in output_list])}
  </ul>
</body>
</html>
"""

# Writing content HTML an a file
with open(html_file_name, "w") as f:
    f.write(html_content)

# Create a link from HTML file generated
html_file_link = f'{os.path.abspath(html_file_name)}'

# Print name file HTML generated as a link
print("\n-------------------- Verification complete ------------------- \n")
time.sleep(1)
msg = f"Final Report: {click.style(html_file_link, fg='green', underline=True, bold=True, blink=False, reverse=False)}"
text_em = f"\033[32m\u2714\033[0m {msg} \n"
click.echo(text_em)
print(" Completed! \n")