# Import library dependencies.
import argparse
# Import project python file dependencies. This is the main file to interface with the honeypot with.
from ssh_honeypot import *
from web_honeypot import *
from dashboard_data_parser import *
from web_app import *

if __name__ == "__main__":
    # Create parser and add arguments.
    parser = argparse.ArgumentParser() 
    parser.add_argument('-a','--address', type=str, required=True)
    parser.add_argument('-p','--port', type=int, required=True)
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-w', '--password', type=str)
    parser.add_argument('-s', '--ssh', action="store_true")
    parser.add_argument('-t', '--tarpit', action="store_true")
    parser.add_argument('-wh', '--http', action="store_true")
    
    args = parser.parse_args()
    
    # Parse the arguments based on user-supplied argument.
    try:
        if args.ssh:
            print("[-] Running SSH Honeypot...")
            honeypot(args.address, args.port, args.username, args.password, args.tarpit)

        elif args.http:
            print('[-] Running HTTP Wordpress Honeypot...')
            #if args.nocountry:
                #pass_country_status(True)
            if not args.username:
                args.username = "admin"
                print("[-] Running with default username of admin...")
            if not args.password:
                args.password = "deeboodah"
                print("[-] Running with default password of deeboodah...")
            print(f"Port: {args.port} Username: {args.username} Password: {args.password}")
            run_app(args.port, args.username, args.password)
        else:
            print("[!] You can only choose SSH (-s) (-ssh) or HTTP (-h) (-http) when running script.")
    except KeyboardInterrupt:
        print("\nProgram exited.")
