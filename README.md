# Miedema Crawler
A CSV crawler for http://www.entall.imim.pl/calculator/

## Crawl Steps
- loads all available elements
- sets mixing enthalpy mode
- for every element combination (in parallel, limited to cpu count):
  - sets both elements and clicks 'calculate'
  - parses canvas's cartesian graph retrieving x,y coords (from 0.1 to 0.9)
- saves to csv file (partially, unordered)

## Arguments
| arg | expanded | required | description                                                     |
|-----|----------|----------|-----------------------------------------------------------------|
| -o  | --out    | false    | output file (defaults to output.csv in current directory)       |
| -u  | --url    | false    | miedema url (defaults to http://www.entall.imim.pl/calculator/) |

## Deps
- python 3.10
- venv
- Selenium 4

### Installing deps using pip
```bash
# install venv
pip install venv

# Set your cwd to project's folder
cd miedema-crawler

# use virtual env
virtualenv -p $(which python3) .
source venv/bin/activate 

# install deps
pip install -r requirements.txt
```

## Running
```bash
# Set your cwd to project's folder
cd miedema-crawler

source venv/bin/activate

(venv) python3 main.py  # NOTE: may take a long time
```

## Example output
```csv
pair,0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99
AgAl,-0.237,-2.148,-3.813,-4.996,-5.701,-5.928,-5.682,-4.963,-3.775,-2.120,-0.233
...
```