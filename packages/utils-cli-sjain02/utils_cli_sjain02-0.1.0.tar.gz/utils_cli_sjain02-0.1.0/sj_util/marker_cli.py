import sqlite3
from urltitle import URLTitleReader, URLTitleError
import argparse
from sj_util.helpers.decorators import pprint
from sj_util.helpers.utils import write_csv_data


def get_db_connection():
  
    db_connection=sqlite3.connect('app.db')
    return db_connection

def execute_query(query,fetch:str=None):
    connection=get_db_connection()
    cursor=connection.cursor()
    result=None
    if fetch=="all":
        cursor=connection.execute(query)
        result=cursor.fetchall()
    elif fetch=="one":
        cursor=connection.execute(query)
        result=cursor.fetchone()
    else:
        result=connection.execute(query)
    connection.commit()
    connection.close()
    return result
    
def initialize_db():
    bookmark_query="""
Create table if not exists bookmark(
id integer primary key autoincrement,
title text not null,
url text not null unique
)
"""
    execute_query(bookmark_query)

def insert_bookmark(url,explict_title=None):
    reader=URLTitleReader(verify_ssl=False)
    title=None
    try:
        title=reader.title(url)
    except URLTitleError:
        title=url
    if explict_title!=None:
        title=explict_title
    insert_query="""insert or ignore into bookmark(title,url) values('{}','{}')""".format(title,url)
    result=execute_query(insert_query)
    if result.lastrowid==0:
        pprint("No record inserted. Either it exist or URL is malformed")
    else:
        pprint("The recorded added with id: {}".format(result.lastrowid))

def export():
    result=get_bookmarks(fetch=True)
    write_csv_data('bookmark.csv',result)
    pprint("The bookmarks are exported to bookmark.csv")


def get_bookmarks(fetch=False):
    select_query="""select * from bookmark"""
    result=execute_query(select_query,fetch="all")
    if fetch==True:
        return result
    else:
         pprint(result)

def search_bookmark(search_term):
    formatted_search=["title like '%"+search+"%'" for search in search_term]
    search_string=" or ".join(formatted_search)
    select_query="""select title, url from bookmark where ({})""".format(search_string)
    result=execute_query(select_query,fetch="all")
    pprint(result)

def cli_entry_point():
    print("Marker CLI interface provding utility function for Bookmark.")
    parser=argparse.ArgumentParser()
    subparsers=parser.add_subparsers(dest="command")

    app_parser=subparsers.add_parser('init',help="Initialized Bookmark DB.")
    app_parser=subparsers.add_parser('add',help="Add URL to Bookmark table.")
    app_parser.add_argument('-u','--url',help="URL to bookmark",required=True)
    app_parser.add_argument('-t','--title',help="Title for the URL, to overwrite decoded Title from URL",required=False)
    app_parser=subparsers.add_parser('search',help="Search all bookmarks matching search term/s.")
    app_parser.add_argument('-s','--searchterm',type=str,help="Search terms,Comma separated.",required=True)
    app_parser=subparsers.add_parser('get',help="Get all bookmark")
    app_parser=subparsers.add_parser('export',help="Export bookmarks to bookmark.csv")

    args=parser.parse_args()
    
    if args.command=="init":
        initialize_db()
    elif args.command=="add":
        insert_bookmark(args.url,args.title)
    elif args.command=="search":
        search_string=args.searchterm.split(',')
        print()
        search_bookmark(search_string)
    elif args.command=="get":
        get_bookmarks()
    elif args.command=="export":
        export()
    else:
        parser.print_help()

# initialize_db()
# insert_bookmark("https://medium.com/analytics-vidhya/sqlite-database-crud-operations-using-python-3774929eb799")
# insert_bookmark("https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/release-announcements/CA-PPM-Release-and-Support-Lifecycle-Dates/5894","CA PPM Release and Support Lifecycle Dates")
# insert_bookmark("https://knowledge.broadcom.com/external/article?articleId=9783")
# insert_bookmark("https://knowledge.broadcom.com/external/article/214504/operation-not-permitted-error-while-star.html")
# app-cli add -u https://knowledge.broadcom.com/external/article/200076
# app-cli add -u https://knowledge.broadcom.com/external/article/375684
# get_bookmarks()
# # search_bookmark("cycle")
# search_bookmark(["clarity","portal"])

if __name__=="__main__":
    # search_bookmark()
    pass

