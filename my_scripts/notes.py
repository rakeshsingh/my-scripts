import argparse 
import os
import re
from datetime import datetime
from collections import OrderedDict

class NotesManager:
    """
    Note file format: YYYY-MM-DD_TYPE_detail_seq.txt 
    e.g. 2018-01-01-meeting-generic.txt
        2018-01-02_one-on-one_rohit.txt
        2018-01-02_interview_shiva-sundaram.txt
    """
    def __init__(self):
        self.BASEDIR='/Users/raksingh/WorkDocs/notes'
        self.default_category ='meeting'

    def create_file(self, filename):
        f=open(self.BASEDIR + "/"+ filename,"a+")
        f.close()

    def list(self, category=None):
        notes={}
        if category is None: 
            category = self.default_category 
        with os.scandir(self.BASEDIR) as it:
            for entry in it:
                if entry.is_file() and category in entry.name:
                    notes[entry.name] = entry.stat().st_ctime
                    #print(entry.name, entry.stat().st_ctime)
        sorted_notes = sorted(notes.items(), key=lambda x: x[1], reverse=True)
        for i in range(0, min(len(sorted_notes),10)):
            print(sorted_notes[i][0])

    def create(self, category, detail):
        if category is None:
            category='meeting'
        if detail is None:
            detail='self'
        now = datetime.now()
        date_string= datetime.today().strftime('%Y-%m-%d')
        self.create_file('_'.join([date_string, category, detail]) + '.md')
    
if __name__ =='__main__':
    nm = NotesManager()
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new", action="store_true", help="create a new note\n usage: notes.py -c category detail")
    parser.add_argument("-l", "--list", action="store_true", help="list most recent notes")
    parser.add_argument("-o", "--overwrite", action="store_true", help="overwrite previous note")
    parser.add_argument("-c", "--category", help="category of the notes, e.g. meeting, todo, oneonone")
    args = parser.parse_args()
    if args.list:
        nm.list(args.category)
    elif args.new:
        nm.create(args.category, args.detail)
        nm.list(args.category)
    else:
        nm.list(args.category)
