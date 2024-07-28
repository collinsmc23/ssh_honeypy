from flask import Flask
from flask import Flask, render_template, request, redirect, url_for


def ssh_honeypy_web_app():
    ssh_honeypy_web_app = Flask(__name__)

    @ssh_honeypy_web_app.route('/')
    
    def index():
        return render_template('dashboard.html')
    
    return ssh_honeypy_web_app

