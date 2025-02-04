import re
from requests import get
from bs4 import BeautifulSoup
from time import strftime, strptime
from decimal import Decimal


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
        raise ValueError(f'Notam Invalid!')
    
    sections = ['', 'Q', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'CREATED:', 'SOURCE:']
    parsed_notam = dict()
    notam = notam.replace('\n',' ')
    pattern = r'{}(.+?)(?:{}\)(.+?))?(?:{}\)(.+?))?(?:{}\)(.+?))?(?:{}\)(.+?))?(?:{}\)(.+?))?(?:{}\)(.+?))?(?:{}\)(.+?))?(?:{}\)(.+?))?{}(.+){}(.+)'
    match = re.search(pattern.format(*sections), notam)
    if not match:
        raise ValueError(f'Parsing failed.')
    for sec in sections:
        grouped = match.group(sections.index(sec) + 1)
        parsed_notam[sec] = grouped.strip() if grouped else grouped

    coordinates = re.findall(r'(\d[\d\.]{5,10}[NS]).*?(\d[\d\.]{5,10}[EW])', notam)
    coordinates = [(dms_to_dd(lat),dms_to_dd(long)) for lat,long in coordinates]
    parsed_notam['coordinates'] = coordinates
            
    return parsed_notam

def pars_part(notam : str) -> str:
    notam = notam.replace('\n',' ')
    if not validate_notam(notam):
        raise ValueError(f'Notam Invalid!')
    match = re.search(r'(.+?)[QABCDE]\)(?:.*?A\)(.+?)[QABCDEF]\))?',notam)
    if match:
        identifier = match.group(1)
        a_sec = str(match.group(2))
        return identifier + ' ' + a_sec


def scrap_notams(notam_link: str):
    html_text = get(notam_link).text
    soup = BeautifulSoup(html_text,'lxml')

    notams = soup.find_all(
                    'td',
                    class_="textBlack12",
                    valign="top",
                    width=''
                    )
    find_non = soup.find(
                    'td',
                    class_="textRed12",
                    align="",
                    height=""
                    ).text
    
    number_of_notams = int(re.search(r'Number of NOTAMs:\s*?(\d+)',find_non).group(1))
    print(f'Number of scrapped notams : {number_of_notams}')
    

    if number_of_notams != len(notams):
        raise ValueError("Failed to scrap all the Notams.")
    notams_text = [notam.text for notam in notams]
    return notams_text

def convert_time_standard(time : str):
    time_format = "%d %b %Y %H:%M:%S"
    standard_time_format = "%Y-%m-%d %H:%M:%S"
    time_obj = strptime(time.strip(),time_format)
    return time_obj

