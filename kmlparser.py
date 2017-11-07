from pykml import parser


kml_file = path.join("geoData/cb_2016_us_state_20m/cb_2016_us_state_20m.kml")

with open(kml_file) as f:
    doc = parser.parse(f)
