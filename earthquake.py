import datetime
import logging
logger = logging.getLogger(__name__)

class Earthquake:
    earthquake_count = 0

    def __init__(self, id:str, magnitude:int, place:str, time, longitude: int, latitude: int)->None:
       self.id = id
       self.magnitude = magnitude
       self.place = place
       self.time = time
       self.longitude = longitude
       self.latitude = latitude
       Earthquake.earthquake_count += 1

    def category(self) -> None:
        if self.magnitude <= 2.9:
            logger.info('mini')
        elif self.magnitude >=3 and self.magnitude <=3.9:
            logger.info('minor')
        elif self.magnitude >=4 and self.magnitude<=4.9:
            logger.info('light')
        elif self.magnitude >=5 and self.magnitude<=5.9:
            logger.info('moderate')
        elif self.magnitude >=6 and self.magnitude<=6.9:
            logger.info('strong')
        elif self.magnitude >=7 and self.magnitude<=7.9:
            logger.info('major')
        elif self.magnitude >=8:
            logger.info('great')
        else:
            logger.info('Category is not defined.')



