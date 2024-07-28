import pytz
import argparse
import datetime
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
# from functools import lru_cache
from tabulate import tabulate


# Initialize
geolocator = Nominatim(user_agent='horoscope')
timezone_finder = TimezoneFinder()


# Constants
SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

PLANETS = [ swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
        swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO ]


def degree_to_sign(degree:float) -> str:
    """Convert degree to astrological sign."""
    sign_index = int(degree // 30)
    return SIGNS[sign_index]


# @lru_cache(maxsize=100)
def get_timezone_and_location(city: str):
    """Get timezone and location information for a given city."""
    location = geolocator.geocode(city)
    if not location:
        raise ValueError(f"Location '{city}' not found.")
    timezone = timezone_finder.timezone_at(lat=location.latitude, lng=location.longitude)
    if not timezone:
        raise ValueError(f"Timezone for location '{city}' not found.")
    return location, timezone


def get_utc_offset_on_date(timezone: str, date: datetime.datetime) -> float:
    """Get the UTC offset for a given date and timezone."""
    tz = pytz.timezone(timezone)
    date = tz.localize(date, is_dst=None)
    return date.utcoffset().total_seconds() / 3600


def get_planet_positions(julian_day: float):
    """Get positions of planets for a given Julian day."""
    planet_positions = {swe.get_planet_name(planet): swe.calc_ut(julian_day, planet)[0] for planet in PLANETS}
    return [[planet, f"{position[0] % 30:.2f}", degree_to_sign(position[0])] for planet, position in planet_positions.items()]


def get_houses(julian_day, latitude, longitude, house_system = b'P'):
    """Get house positions for a given Julian day, latitude, and longitude."""
    houses_info = swe.houses(julian_day, latitude, longitude, house_system)
    houses = houses_info[0]

    return [[index + 1, f"{position % 30:.2f}", degree_to_sign(position)] for index, position in enumerate(houses)]


def calculete_julian_day(timezone, year, month, day, hour: int = 0, minute: int = 0):
    """Convert date to Julian Day"""
    date = datetime.datetime(year, month, day, hour, minute)
    utc_offset = get_utc_offset_on_date(timezone, date)
    utc = date - datetime.timedelta(hours=utc_offset)

    return swe.julday(utc.year, utc.month,
            utc.day, utc.hour + utc.minute / 60.0)


def create_astrological_chart(city: str, year: int, month: int, day: int, hour: int = None, minute: int = None) -> dict:
    """Create an astrological chart for a given city, date, and time."""
    location, timezone = get_timezone_and_location(city)
    julian_day = calculete_julian_day(timezone, year, month, day, hour or 0, minute or 0)
    planet_list = get_planet_positions(julian_day)

    result = {
        'planets': planet_list,
        'houses': [],
    }

    if hour is not None and minute is not None:
        house_list = get_houses(julian_day, location.latitude, location.longitude)
        result['houses'] = house_list

    return result


def main():
    parser = argparse.ArgumentParser(description='Create an astrological chart.')
    parser.add_argument('city', type=str, help='City name')
    parser.add_argument('year', type=int, help='Year of birth')
    parser.add_argument('month', type=int, help='Month of birth')
    parser.add_argument('day', type=int, help='Day of birth')
    parser.add_argument('--time', type=str, help='Time of birth in HH:MM format (optional)')

    args = parser.parse_args()

    hour, minute = None, None
    if args.time:
        try:
            hour, minute = map(int, args.time.split(':'))
        except ValueError:
            print("Error: Time must be in HH:MM format")
            return

    try:
        result = create_astrological_chart(args.city, args.year, args.month,
                                        args.day, hour, minute)
        print("\n")
        print(tabulate(result['planets'], headers=["Planet", "Degree", "Sign"], tablefmt="github"))
        if result['houses']:
            print("\n")
            print(tabulate(result['houses'], headers=["House", "Degree", "Sign"], tablefmt="github"))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()