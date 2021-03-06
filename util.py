import simplekml

__author__ = 'peter'


def parse_arguments(args):
    if '--name' not in args or args['--name'] is None:
        args['--name'] = args['<outfile>']

    if not args['<outfile>'].endswith('.kml'):
        args['<outfile>'] += '.kml'

    kml = simplekml.Kml(name=args['--name'])
    return args, kml


def parse_latlon(c):
    try:
        lat, lon = c.split(',')
    except ValueError:
        print u'Could not split {0}, invalid coordinates!'
        raise

    if 'n' in lat.lower() or 's' in lat.lower():
        d, m, s = lat[:-1].split()
        if 's' in lat.lower():
            lat = -(float(d) + (float(m) / 60) + (float(s) / 3600))
        else:
            lat = float(d) + (float(m) / 60) + (float(s) / 3600)
    if 'e' in lon.lower() or 'w' in lon.lower():
        d, m, s = lon[:-1].split()
        if 'w' in lon.lower():
            lon = -(float(d) + (float(m) / 60) + (float(s) / 3600))
        else:
            lon = float(d) + (float(m) / 60) + (float(s) / 3600)
    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        print u'Could not convert {0} to floats!'.format((lat, lon))
        raise
    return lat, lon


def parse_color(color):
    return getattr(simplekml.Color, color, color)
