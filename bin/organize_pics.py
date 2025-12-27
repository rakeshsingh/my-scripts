#!/usr/bin/python
import exifread
import re
import sys
from datetime import datetime
from my_scripts.logger import setup_logger

logger = setup_logger()


def read_metadata(filename):
    """
    Read image file and get the exif attributes
    """
    logger.info('Came here with: ' , filename)
    # Open image file for reading (binary mode)
    f = open(filename, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)
    return tags

def get_creation_date(tags):
    """
    Read the exif tags and get the creation date of an image
    """
    """
    Key: EXIF DateTimeOriginal, value 2016:03:22 14:35:07
    Key: EXIF DateTimeDigitized, value 2016:03:22 14:35:07
    Key: GPS GPSDate, value 2016:03:82
    Key: Image DateTime, value 2016:03:22 14:35:07
    """
    date_tags=['EXIF DateTimeOriginal', 'EXIF DateTimeDigitize', 'GPS GPSDate', 'Image DateTime']
    available_dates=[]
    date_with_time_pattern='\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}'
    date_pattern='\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}'

    for tag in date_tags:
        if tag in tags.keys():
            #print(tag, tags[tag], type(tags[tag]))
            if re.match(date_with_time_pattern,str(tags[tag])):
               available_dates.append(datetime.strptime(str(tags[tag]), '%Y:%m:%d %H:%M:%S'))
            elif re.match(date_pattern,str(tags[tag])):
               available_dates.append(datetime.strptime(str(tags[tag]), '%Y:%m:%d'))
            else:
                """ Time is not in the valid format """
                pass

    # get the minimum date from available dates as 
    # the first creation date of image
    return min(date for date in available_dates)

def rename_directory():
    pass


if __name__ == '__main__':
    """ Execution Starts here """
    for line in sys.stdin:
        filename=line.rstrip()
        logger.info(filename)
        metadata = read_metadata(filename)
        logger.info('creation_date: ', get_creation_date(metadata))
