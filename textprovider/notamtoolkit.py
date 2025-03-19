import logging
import re
from datetime import datetime
from decimal import Decimal
from bs4 import BeautifulSoup
from requests import get

logger = logging.getLogger(__name__)

def dms_to_dd(dms):

    direction = dms[-1]
    dms_fx = str(float(dms[:-1]))

    degrees = Decimal(dms_fx[:2])
    minutes = Decimal(dms_fx[2:4])
    seconds = Decimal(dms_fx[4:])

    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)

    if direction in ['W', 'S']:
        return -decimal_degrees
    return decimal_degrees

def validate_notam(notam : str):
    if not all(key in notam for key in ('E)','CREATED:','SOURCE:')) or notam.startswith(('Q)', 'A)', 'B)', 'C)', 'D)', 'E)', 'F)', 'G)')):
        return False
    return True

def notam_parser(notam : str):
    notam = notam.strip()
    if not validate_notam(notam):
        raise ValueError('Notam Invalid!')
    
    sections = ['', 'Q', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'CREATED:', 'SOURCE:']
    parsed_notam = dict()
    pattern = r'(.+?)(?:Q\)(.+?))?(?:A\)(.+?))?(?:B\)(.+?))?(?:C\)(.+?))?(?:D\)(.+?))?(?:E\)(.+?))?(?:F\)(.+?))?(?:G\)(.+?))?CREATED:(.+)SOURCE:(.+)'
    match = re.search(pattern, notam, re.DOTALL)
    if not match:
        raise ValueError('Parsing failed.')
    for sec in sections:
        grouped = match.group(sections.index(sec) + 1)
        parsed_notam[sec] = grouped.strip() if grouped else grouped

    coordinates = re.findall(r'(\d[\d\.]{5,10}[NS]).*?(\d[\d\.]{5,10}[EW])', notam, re.DOTALL)
    coordinates = [(dms_to_dd(lat),dms_to_dd(long)) for lat,long in coordinates]
    parsed_notam['coordinates'] = coordinates
            
    return parsed_notam

def pars_part(notam : str) -> str:
    if not validate_notam(notam):
        raise ValueError('Notam Invalid!')
    match = re.search(r'(.+?)[QABCDE]\)(?:.*?A\)(.+?)[QABCDEF]\))?',notam, re.DOTALL)
    if match:
        identifier = match.group(1).strip()
        a_sec = str(match.group(2)).strip()
        return identifier + ' ' + a_sec


def scrap_notams(notam_link: str):
    html_text = get(notam_link).text
    soup = BeautifulSoup(html_text,'lxml')

    notams = soup.find_all(
                    'td',
                    class_="textBlack12",
                    valign="top",
                    width=None
                    )
    find_non = soup.find(
                    'td',
                    class_="textRed12",
                    align=None,
                    height=None
                    )
    if find_non:
        number_of_notams = int(re.search(r'Number of NOTAMs:\s*?(\d+)',find_non.text).group(1))
    else :
        raise AttributeError('Failed to verify the number of Notams!')
    
    logger.info(f'Number of scrapped notams : {number_of_notams}')
    

    if number_of_notams != len(notams):
        raise ValueError('Failed to scrap all the Notams.')
    notams_text = [notam.text for notam in notams]
    return notams_text

def convert_time_standard(time : str):
    time_format = r"%d %b %Y %H:%M:%S"
    time_obj = datetime.strptime(time.strip(),time_format)
    return time_obj

