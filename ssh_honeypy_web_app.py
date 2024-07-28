from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


log_file = 'creds_audits.log'

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
plt.savefig("/home/grant/projects/ssh-honeypot/templates/top10creds.png")

def ssh_honeypy_web_app():
    ssh_honeypy_web_app = Flask(__name__)

    @ssh_honeypy_web_app.route('/')
    
    def index():
        return render_template('dashboard.html')
    
    return ssh_honeypy_web_app

app = ssh_honeypy_web_app()
app.run()