import unittest
import os

from scripts.notes import NotesManager

class TestNotesManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.nm=NotesManager()
        self.filename='testfile.txt'
        self.category='meeting'
        self.detail='self'
        self.meeting_file='2018-08-14_meeting_self.txt'

    def test_truth(self):
        self.assertEqual('foo'.upper(), 'FOO')


    def test_init(self):
        self.assertEqual('./data/', self.nm.BASEDIR)


    def test_create_file(self):
        self.nm.create_file(self.filename)
        self.assertEqual(os.path.exists(self.nm.BASEDIR + self.filename), True)
   

    def test_create_notes(self):
        self.nm.create(self.category, self.detail)
        self.assertEqual(os.path.exists(self.nm.BASEDIR + self.meeting_file), True)
    
    @classmethod
    def tearDownClass(self):
        """ 
        Delete the testfiles
        """
        os.remove(self.nm.BASEDIR + self.filename)
