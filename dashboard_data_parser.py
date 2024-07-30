import pandas as pd
import re
import requests

creds_audits_log_file = '/home/grant/projects/ssh-honeypot/test_log_files/creds_audits.log'
cmd_log_file = '/home/grant/projects/ssh-honeypot/test_log_files/cmd_audits.log'
http_log_file = "/home/grant/projects/ssh-honeypot/test_log_files/http_audit.log"

def parse_creds_audits_log(creds_audits_log_file):
    data = []

    with open(creds_audits_log_file, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            ip_address  = parts[0]
            username = parts[1]
            password = parts[2]
            data.append([ip_address, username, password])

    df = pd.DataFrame(data, columns=["ip_address", "username", "password"])
    return df

creds_audits_log_df = parse_creds_audits_log('/home/grant/projects/ssh-honeypot/test_log_files/creds_audits.log')

def parse_cmd_audits_log(cmd_audits_log_file):

    data = []
    
    with open(cmd_audits_log_file, 'r') as file:
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

    return df

cmd_audits_log_df = parse_cmd_audits_log('/home/grant/projects/ssh-honeypot/test_log_files/cmd_audits.log')

def top_10_calculator(dataframe, column):

    for col in dataframe.columns:
        if col == column:
            top_10_df = dataframe[column].value_counts().reset_index().head(10)
            top_10_df.columns = [column, "count"]

    return top_10_df


def get_country_code(ip):

    data_list = []

    url = f"https://api.cleantalk.org/?method_name=ip_info&ip={ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ip_data = data.get('data', {})
            country_info = ip_data.get(ip, {})
            data_list.append({'IP Address': ip, 'Country_Code': country_info.get('country_code')})
            #return country_info.get('country_code')
        else:
            print(f"Error: Unable to retrieve data for IP {ip}. Status code: {response.status_code}")
        #df = pd.DataFrame(data_list)
    except requests.RequestException as e:
        print(f"Request failed: {e}")


    return data_list


#top_ip_address = top_10_calculator(creds_audits_log_df, "ip_address")

def ip_to_country_code(dataframe):

    data = []

    for ip in dataframe['ip_address']:
        get_country = get_country_code(ip)
        parse_get_country = get_country[0]["Country_Code"]
        data.append({"IP Address": ip, "Country_Code": parse_get_country})
    
    df = pd.DataFrame(data)
    return df

# get_ip_to_country = ip_to_country_code(creds_audits_log_df)

# top_country = top_10_calculator(get_ip_to_country, "Country_Code")
# print(top_country)