#!/usr/bin/env python
import argparse
import simplekml
import util

__author__ = 'peter'

parser = argparse.ArgumentParser(epilog='Example usage: {0} "47 59 00N,38 45 00E" "47 59 59N,38 45 00E" "47 59 59N, 38 45 59E" "47 59 00N, 38 45 59E" out.kml'.format(__file__))
parser.add_argument('--name', '-n', help='The name for the kml file and the polygon, default is the same name as the outfile')
parser.add_argument('--colour', '-c', help='The colour of the polygon, given as a KML valid colour (for instance, 3fff0000 for blue)', default='3fff0000')
parser.add_argument('coords', nargs='+', help='Polygon coordinates, separated by a comma for lat/long, separated by a space for next coord. Can be given as degrees/minutes/seconds by using "48 51 29.1348N,2 17 40.8984E"')
parser.add_argument('outfile', help='The name of the output (kml) file')
args = parser.parse_args()

args, kml = util.parse_arguments(args)

p = kml.newpolygon(name=args.name)

coords = []

# Check if last coordinate is also first coordinate, to make the polygon closing
if not args.coords[0] == args.coords[-1]:
    args.coords.append(args.coords[0])
print u'Drawing polygon for coordinates {0}...'.format(args.coords)
for c in args.coords:
    try:
        lat, lon = c.split(',')
    except ValueError:
        print u'Could not split {0}, invalid coordinates!'
    if 'n' in lat.lower() or 's' in lat.lower():
        deg, min, sec = lat[:-1].split()
        if 's' in lat.lower():
            lat = -(float(deg) + (float(min) / 60) + (float(sec) / 3600))
        else:
            lat = float(deg) + (float(min) / 60) + (float(sec) / 3600)
    if 'e' in lon.lower() or 'w' in lon.lower():
        deg, min, sec = lon[:-1].split()
        if 'w' in lon.lower():
            lon = -(float(deg) + (float(min) / 60) + (float(sec) / 3600))
        else:
            lon = float(deg) + (float(min) / 60) + (float(sec) / 3600)
    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        print u'Could not convert {0} to floats!'.format((lat, lon))
    coords.append((lon, lat))

p.outerboundaryis = coords
print u'Setting colour...'
p.style.polystyle.color = args.colour
print u'Saving to {0}...'.format(args.outfile)
kml.save(args.outfile)
print u'Done!'
