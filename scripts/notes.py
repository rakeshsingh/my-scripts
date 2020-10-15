import argparse 
from datetime import datetime
import os
import re


class NotesManager:
    """
    Note file format: YYYY-MM-DD_TYPE_detail_seq.txt 
    e.g. 2018-01-01-meeting-generic.txt
        2018-01-02_one-on-one_rohit.txt
        2018-01-02_interview_shiva-sundaram.txt
    """
    def __init__(self):
        self.BASEDIR='./data/'


    def create_file(self, filename):
        f=open("./data/" + filename,"a+")
        f.close()

    def list(self, category=None):
        if category is None: 
            category = '' 
        for filename in os.listdir(self.BASEDIR):
            if category in filename:
                print(filename)

    
    def create(self, category, detail):
        if category is None:
            category='meeting'
        if detail is None:
            detail='self'
        now = datetime.now()
        date_string= datetime.today().strftime('%Y-%m-%d')
        self.create_file('_'.join([date_string, category, detail]) + '.txt')

    
if __name__ =='__main__':
    nm = NotesManager()
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new", action="store_true", help="create a new note\n usage: notes.py -c category detail")
    parser.add_argument("-l", "--list", action="store_true", help="list most recent notes")
    parser.add_argument("-o", "--overwrite", action="store_true", help="overwrite previous note")
    parser.add_argument("-c", "--category", help="category of the notes, e.g. meeting, todo, oneonone")
    parser.add_argument("-d", "--detail", help="additional details for the notes e.g. meeting subject, 1_1 person")
    args = parser.parse_args()
    if args.list:
        nm.list(args.category)
    elif args.new:
        nm.create(args.category, args.detail)
        nm.list(args.category)
    else:
        nm.list(args.category)