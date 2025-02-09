from celery import shared_task
from .scrapper import scrap_notams, notam_parser, pars_part, convert_time_standard
from django.conf import settings
from django.db import transaction
from textprovider.models import Notams, ParsedNotams, Coordinates
from django.utils import timezone

@shared_task
def update_saved_notams():
    notams : list[str] = []
    base_url : str = settings.SCRAPPING_URL
    locations : list = settings.SCRAPPING_LOCATIONS

    #Webscrapping notams
    for location in locations:
        try:
            scrapped = scrap_notams(base_url.replace(r'{LOCATION_ID}',location))
            notams.extend(scrapped)
        except Exception as error:
            print(f'Exception occurred when scrapping from web (location = {location}): \n{error}')
            continue
      
    notam_objects = []
    parsed_notam_objects = []
    coordinate_objects = []
    
    #Saving notams in db
    stripped_notams = {notam.strip() for notam in notams}
    for notam_text in stripped_notams:
        try:
            part = pars_part(notam_text)
        except Exception as error:
            print(f'Parsing process failed when using "pars_part": {error}')
            continue

        notam = Notams(notam_text = notam_text, part=part )
        notam_objects.append(notam)
    try:
        Notams.objects.bulk_create(notam_objects, ignore_conflicts=True)
    except Exception as error:
        print(f'Exception occurred when saving in Notams : {error}')

    #clearing outdated notams
    cleared = []
    treshold = timezone.now()-timezone.timedelta(hours=2)
    required_clearing_fields = ('id','notam_text','part')
    notams_in_db = Notams.objects.select_related('parsed_notams').filter(parsed_notams__created__lt=treshold).only(*required_clearing_fields).values(*required_clearing_fields)
    for notam in notams_in_db:
        if notam['notam_text'] not in stripped_notams:
            Notams.objects.filter(pk=notam['id']).delete()
            cleared.append(notam['part'])
    print(f'{cleared=}')


    with transaction.atomic():
        #Saving parsed notams
        not_parsed_notams = Notams.objects.filter(parsed_notams__isnull=True)
        for not_parsed_notam in not_parsed_notams:
            try:
                parsed = notam_parser(not_parsed_notam.notam_text)
            except Exception as error:
                print(f'Parsing process failed when using "notam_parser" :\n{error}\tid : {not_parsed_notam.part}')
                continue      
            parsed_notam_obj = ParsedNotams(
                                    notam = not_parsed_notam,
                                    identifier = parsed[''],
                                    sec_q = parsed['Q'],
                                    sec_a = parsed['A'],
                                    sec_b = parsed['B'],
                                    sec_c = parsed['C'],
                                    sec_d = parsed['D'],
                                    sec_e = parsed['E'],
                                    sec_f = parsed['F'],
                                    created = timezone.make_aware(convert_time_standard(parsed['CREATED:'])),
                                    source = parsed['SOURCE:']
                                    )
            parsed_notam_objects.append(parsed_notam_obj)
            
            #Saving coordinates related to notams
            coordinates = parsed['coordinates']
            for raw_coordinate in coordinates:
                coordinate = Coordinates(
                                    notam = not_parsed_notam,
                                    latitude = raw_coordinate[0],
                                    longitude = raw_coordinate[1]
                                    )
                coordinate_objects.append(coordinate)
        print(f'parsed notams to be saved : {len(parsed_notam_objects)}')
        print(f'coordinates to be saved : {len(coordinate_objects)}')
        try:
            ParsedNotams.objects.bulk_create(parsed_notam_objects, ignore_conflicts=True)
            Coordinates.objects.bulk_create(coordinate_objects, ignore_conflicts=True)
        except Exception as error:
            print(f'Exception occurred when saving parsed_notams or coordinates : {error}')
        