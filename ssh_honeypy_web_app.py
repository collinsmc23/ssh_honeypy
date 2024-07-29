from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import seaborn as sns
import re
import requests
import matplotlib.pyplot as plt


log_file = '/home/grant/projects/ssh-honeypot/test_log_files/creds_audits.log'
cmd_log_file = '/home/grant/projects/ssh-honeypot/test_log_files/cmd_audits.log'

def top_to_credential_dashboard(log_file):

    data = []

    with open(log_file, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            ip_address  = parts[0]
            username = parts[1]
            password = parts[2]
            data.append([ip_address, username, password])

    df = pd.DataFrame(data, columns=["ip_address", "username", "password"])

    # Combine username and password into a single column
    df['user_pass'] = df['username'] + ' + ' + df['password']

    # Count the frequency of each username + password pair
    user_pass_counts = df['user_pass'].value_counts().reset_index()
    user_pass_counts.columns = ['user_pass', 'count']

    # Get the top 10 username + password pairs
    top_10_user_pass = user_pass_counts.head(10)

    sns.set_theme()

    plt.figure(figsize=(15, 6))
    sns.barplot(x='count', y='user_pass', data=top_10_user_pass)
    plt.xlabel('Count')
    plt.ylabel('Username + Password')
    plt.title('Top 10 Username + Password Pairs')
    #plt.show()
    return plt.savefig("/home/grant/projects/ssh-honeypot/templates/top10creds.png")

top_to_credential_dashboard(log_file)

def top_cmd_commands(log_file):

    data = []
    
    with open(log_file, 'r') as file:
        for line in file:
            lines = line.strip().split('\n')
    
            # Regular expression to extract IP address and command
            pattern = re.compile(r"Command b'([^']*)'executed by (\d+\.\d+\.\d+\.\d+)")
            
            for line in lines:
                match = pattern.search(line)
                if match:
                    command, ip = match.groups()
                    data.append({'IP Address': ip, 'Command': command})
    
    df = pd.DataFrame(data) 

    parse_df_commands = df['Command'].value_counts().reset_index()
    parse_df_commands.columns = ['commands', 'count']

    # # Get the top 10 username + password pairs
    top_10_commands = parse_df_commands.head(10)

    sns.set_theme()

    plt.figure(figsize=(15, 6))
    sns.barplot(x='count', y='commands', data=top_10_commands)
    plt.xlabel('Count')
    plt.ylabel('Commmands')
    plt.title('Top 10 Commands Entered')
    return plt.savefig("/home/grant/projects/ssh-honeypot/templates/top10cmd.png")

top_cmd_commands(cmd_log_file)

def top_10_country(log_file):
    # Step 1: Read IP addresses from the log file and create a DataFrame
    data = []
    
    with open(log_file, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            ip_address = parts[0]
            data.append([ip_address])

    df = pd.DataFrame(data, columns=["ip_address"])

    # Step 2: Define a function to get the country code from the API
    def get_country_code(ip):
        url = f"https://api.cleantalk.org/?method_name=ip_info&ip={ip}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                ip_data = data.get('data', {})
                country_info = ip_data.get(ip, {})
                print(country_info)
                return country_info.get('country_code')
            else:
                print(f"Error: Unable to retrieve data for IP {ip}. Status code: {response.status_code}")
                return 'Error'
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return 'Error'

    # Step 3: Apply the function to get country codes for each IP address
    df['Country_Code'] = df['ip_address'].apply(get_country_code)

    # Step 4: Print the DataFrame with the new column
    print(df)

top_10_country(log_file)

def ssh_honeypy_web_app():
    ssh_honeypy_web_app = Flask(__name__)

    @ssh_honeypy_web_app.route('/')
    
    def index():
        return render_template('dashboard.html')
    
    return ssh_honeypy_web_app

app = ssh_honeypy_web_app()