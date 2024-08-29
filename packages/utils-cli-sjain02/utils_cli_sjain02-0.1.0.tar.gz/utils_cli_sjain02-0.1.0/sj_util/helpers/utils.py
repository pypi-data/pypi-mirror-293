import argparse
import csv

LOG_FILE='util-cli.log'
LOG_CATEGORY="UTILS_CLI"

# Utility functions shared acrossed

def write_log(category:str,message:str,log_file:str=LOG_FILE)->None:
    with open(log_file,'a') as f:
        print("{}: {}".format(category,message),file=f, end='\n')

def write_csv_data(csv_file_path,data):
    with open(csv_file_path,'a') as f:
        csv_h=csv.writer(f)
        csv_h.writerows(data)

def open_browser(url:str=None,search:str=None)->None:
    import webbrowser
    if url!=None and search==None:
        webbrowser.open_new_tab(url)
    elif url==None and search!=None:
        # Will loop through the JSON and open all search terms
        # webbrowser.open_new_tab(url)
        print("TODO.....")
    else:
        message="Can't open a new tab, neither URL nor search term provided"
        print(message)
        write_log(category=LOG_CATEGORY,message=message)

# def parse(xml_file_path:str,job_name:str=None):
#     print("Will parse clarity XML {} {}".format(xml_file_path,job_name))

# def cli_entry_point():
#     parser=argparse.ArgumentParser()
#     subparsers=parser.add_subparsers(dest="command")

#     parser_hello=subparsers.add_parser('hello',help="Print Hello MSG!")
#     log_parser=subparsers.add_parser('log',help="Write log message to cli log file",description="Write logs of CLI",)
#     log_parser.add_argument('-f','--filename',help="Path to logfile",required=True)
#     log_parser.add_argument('-c','--category',help="Log Category eg. clarity-cli or util-cli",required=True)
#     log_parser.add_argument('-m','--message',help="Log message",required=True)

#     web_parser=subparsers.add_parser("web",help="Open the new tab in default browser with provided URL.")
#     web_parser.add_argument("-u","--url",help="URL to open",required=False)
#     web_parser.add_argument("-s","--search",help="Search terms",required=False)

#     args=parser.parse_args()

#     if args.command=='hello':
#         hello()
#     elif args.command=="log":
#         write_log(log_file=args.filename,category=args.category,message=args.message)
#     elif args.command=='web':
#         open_browser(url=args.url,search=args.search)
#     else:
#         parser.print_help()

