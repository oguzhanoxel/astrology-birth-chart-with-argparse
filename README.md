# Horoscope Chart Generator

This project generates an astrological birth chart for a specified date and location. The chart includes the positions of planets and houses. It is built using Python and leverages libraries such as Swiss Ephemeris, Geopy, TimezoneFinder, and Tabulate.

## Requirements

You can install these libraries using pip:

```sh
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

Or you can install these libraries using `pipenv`:

```sh
pip install pipenv

pipenv install

pipenv shell
```

## Usage

This command-line tool calculates the positions of planets and houses for a given city and date.

### Command Line Usage

```sh
python main.py city year month day [--time HH:MM]
```

### Arguments

- 'city' (str): City name
- 'year' (int): Year of birth
- 'month' (int): Month of birth
- 'day' (int): Day of birth
- '--time' (str, optional): Time of birth in HH
format

<details><summary><strong>Example Usage 1</strong></summary>
<p> 

```sh
python main.py "istanbul" 1996 11 13 --time 6:30
```

#### Output

```sh
| Planet   |   Degree | Sign        |
|----------|----------|-------------|
| Sun      |    21.08 | scorpio     |
| Moon     |    16.9  | sagittarius |
| Mercury  |    27.66 | scorpio     |
| Venus    |    17.86 | libra       |
| Mars     |     7.52 | virgo       |
| Jupiter  |    14.88 | capricorn   |
| Saturn   |     0.97 | aries       |
| Uranus   |     1.13 | aquarius    |
| Neptune  |    25.37 | capricorn   |
| Pluto    |     2.53 | sagittarius |


|   House |   Degree | Sign        |
|---------|----------|-------------|
|       1 |    16.39 | scorpio     |
|       2 |    16.06 | sagittarius |
|       3 |    20.62 | capricorn   |
|       4 |    26.91 | aquarius    |
|       5 |    29.15 | pisces      |
|       6 |    25.23 | aries       |
|       7 |    16.39 | taurus      |
|       8 |    16.06 | gemini      |
|       9 |    20.62 | cancer      |
|      10 |    26.91 | leo         |
|      11 |    29.15 | virgo       |
|      12 |    25.23 | libra       |
```
</p>
</details>

<details><summary><strong>Example Usage 2</strong></summary>
<p> 

```sh
python main.py "New York" 1990 5 15
```

#### Output

```sh
| Planet   |   Degree | Sign      |
|----------|----------|-----------|
| Sun      |    24.07 | taurus    |
| Moon     |    23.06 | capricorn |
| Mercury  |     8.06 | taurus    |
| Venus    |    12.44 | aries     |
| Mars     |    18.09 | pisces    |
| Jupiter  |     9.48 | cancer    |
| Saturn   |    25.25 | capricorn |
| Uranus   |     9.19 | capricorn |
| Neptune  |    14.36 | capricorn |
| Pluto    |    16.18 | scorpio   |
```
</p>
</details>