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
pair,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9
AgBa,-7.554,-14.316,-20.119,-24.742,-27.895,-29.182,-28.051,-23.709,-14.974
AgBi,-0.035,-0.064,-0.087,-0.103,-0.112,-0.112,-0.103,-0.082,-0.048
AgC,-16.715,-26.937,-32.331,-34.038,-32.866,-29.404,-24.089,-17.254,-9.157
AgAu,-1.995,-3.546,-4.653,-5.316,-5.535,-5.312,-4.647,-3.539,-1.990
AgAs,-3.596,-6.454,-8.551,-9.866,-10.376,-10.058,-8.888,-6.839,-3.886
AgAl,-2.148,-3.813,-4.996,-5.701,-5.928,-5.682,-4.963,-3.775,-2.120
...
```