#!/usr/bin/python
import argparse
import logging
import time
import sys

sys.path.insert(0, 'pogo/')

from custom_exceptions import GeneralPogoException

from api import PokeAuthSession
from location import Location

from inventory import items

def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('Line %(lineno)d,%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# Example functions
# Get profile
def getProfile(session):
        logging.info("Printing Profile:")
        profile = session.getProfile()
        logging.info(profile)


# Do Inventory stuff
def getInventory(session):
    logging.info("Get Inventory:")
    logging.info(session.getInventory())


# Basic solution to spinning all forts.
# Since traveling salesman problem, not
# true solution. But at least you get
# those step in
def sortCloseForts(session):
    # Sort nearest forts (pokestop)
    logging.info("Sorting Nearest Forts:")
    cells = session.getMapObjects()
    latitude, longitude, _ = session.getCoordinates()
    ordered_forts = []
    for cell in cells.map_cells:
        for fort in cell.forts:
            dist = Location.getDistance(
                latitude,
                longitude,
                fort.latitude,
                fort.longitude
            )
            if fort.type == 1:
                ordered_forts.append({'distance': dist, 'fort': fort})

    ordered_forts = sorted(ordered_forts, key=lambda k: k['distance'])
    return [instance['fort'] for instance in ordered_forts]


# Find the fort closest to user
def findClosestForts(session):
    # Find nearest fort (pokestop)
    logging.info("Finding Nearest Fort:")
    return sortCloseForts(session)


# Walk to fort and spin
def walkAndSpin(session, fort):
    # No fort, demo == over
    if fort:
        details = session.getFortDetails(fort)
        logging.info("Spinning the Fort \"%s\":" % details.name)

        # Walk over
        session.walkTo(fort.latitude, fort.longitude, step=3.2)
        # Give it a spin
        fortResponse = session.getFortSearch(fort)
        logging.info(fortResponse)


# Walk, spin pokestops and auto incubate eggs
def walkSpinAndIncubate(session, forts):
    inventory = session.checkInventory()
    cleanInventory(session)
    # Keep walking until you dont find pokestops
    for fort in forts:
        walkAndSpin(session, fort)
        km_walk = inventory.stats.km_walked
        trgt_km = inventory.incubators[0].target_km_walked
        
        #Displaying distance stats
        logging.info("KM Walked : %f " % km_walk)
        logging.info("Target KM : %f " % trgt_km)

        if (km_walk >= trgt_km):
            eggInfo = setEgg(session)
            logging.info(eggInfo)


# Set an egg to an incubator
def setEgg(session):
    inventory = session.checkInventory()
    incubator = inventory.incubators[0]

    # If no eggs, nothing we can do
    if len(inventory.eggs) == 0:
        return "NO EGGS"
    
    elif (incubator.target_km_walked != 0.0):
        logging.info(incubator.target_km_walked)
        return "INCUBATING"

    egg = inventory.eggs[0]
    return session.setEgg(incubator, egg)

# Clean up all frequent drop items
def cleanInventory(session):
    logging.info("Cleaning out Inventory...")
    bag = session.checkInventory().bag
    
    # Clear out all of a crtain type
    tossable = [items.POTION, items.SUPER_POTION, items.REVIVE]
    for toss in tossable:
        if toss in bag and bag[toss]:
            session.recycleItem(toss, bag[toss])

    # Limit a certain type
    limited = {
        items.POKE_BALL: 50,
        items.GREAT_BALL: 50,
        items.ULTRA_BALL: 100,
        items.RAZZ_BERRY: 25,
        items.HYPER_POTION: 25
    }
    for limit in limited:
        if limit in bag and bag[limit] > limited[limit]:
            session.recycleItem(limit, bag[limit] - limited[limit])


def initiatePokeBot(session):
    # Trying not to flood the servers
    cooldown = 1
    
    # Run the bot
    while True:
        forts = sortCloseForts(session)
        cleanInventory(session)
        try:
            for fort in forts:
                walkAndSpin(session, fort)
                eggInfo = setEgg(session)
                logging.info(eggInfo)

                cooldown = 1
                time.sleep(cooldown)

        except Exception as e:
            logging.critical('Exception raised: %s', e)
            session = poko_session.reauthenticate(session)
            time.sleep(cooldown)
            cooldown *= 2



# Entry point
# Start off authentication and bot
if __name__ == '__main__':
    setupLogger()
    logging.debug('Logger set up')

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="Auth Service", required=True)
    parser.add_argument("-u", "--username", help="Username", required=True)
    parser.add_argument("-p", "--password", help="Password", required=True)
    parser.add_argument("-l", "--location", help="Location")
    parser.add_argument("-g", "--geo_key", help="GEO API Secret")
    args = parser.parse_args()

    # Check service
    if args.auth not in ['ptc', 'google']:
        logging.error('Invalid auth service {}'.format(args.auth))
        sys.exit(-1)

    # Create PokoAuthObject
    poko_session = PokeAuthSession(
        args.username,
        args.password,
        args.auth,
        geo_key=args.geo_key
    )

    # Authenticate with a given location
    # Location is not inherent in authentication
    # But is important to session
    if args.location:
        session = poko_session.authenticate(locationLookup=args.location)
    else:
        session = poko_session.authenticate()

    # Time to show off what we can do
    if session:

        # General
        getProfile(session)
        getInventory(session)

        # Things we need GPS for
        if args.location:

            # Pokestop, eggs related
            initiatePokeBot(session)

    else:
        logging.critical('Session not created successfully')
