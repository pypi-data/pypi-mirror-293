from argparse import ArgumentParser

from pylegs.tap import DEFAULT_CATALOG_COLUMNS, download_catalog


def handle_dlcat(args):
  exclude = {'PSF', 'REX', 'DEV', 'EXP', 'SER'} - set([s.upper() for s in args.types])
  download_catalog(
    save_path=args.output,
    columns=args.cols,
    ra_min=args.ra[0],
    ra_max=args.ra[1],
    delta_ra=args.delta,
    table=args.table,
    exclude_types=exclude,
    magr_min=args.r[0],
    magr_max=args.r[1],
    dec_min=args.dec[0],
    dec_max=args.dec[1],
    brick_primary=not args.noprimary,
    overwrite=args.overwrite,
    workers=args.workers,
    tmp_folder=args.tmp,
    overwrite_tmp=args.otmp,
  )


def entrypoint():
  parser = ArgumentParser(
    prog='pylegs', 
    description='Python client for accessing Legacy Survey data'
  )
  
  subparser = parser.add_subparsers(dest='subprog')
  dlcat = subparser.add_parser(
    'dlcat', help='Tool for download Legacy Survey catalog based on square area'
  )
  dlcat.add_argument(
    'output', action='store', type=str, help='Path of the output table'
  )
  dlcat.add_argument(
    '--ra', action='store', nargs=2, type=float, default=[0, 360], 
    help='Two values specifying the RA range in degrees. Default: 0 360'
  )
  dlcat.add_argument(
    '--delta', action='store', default='10 arcmin',
    help=('The value of the angle interval that the ra axis will be divided. '
          'The unit must be specified. E.g: 1.2 deg, 20 arcmin, 14 arcsec. '
          'Default: 10 arcmin')
  )
  dlcat.add_argument(
    '--dec', action='store', nargs=2, type=float, default=[-90, 90], 
    help='Two values specifying the DEC range in degrees. Default: -90 90'
  )
  dlcat.add_argument(
    '--cols', action='store', nargs='+', default=None,
    help=f'Column names to retrieve. Default: {" ".join(DEFAULT_CATALOG_COLUMNS)}'
  )
  dlcat.add_argument(
    '--table', action='store', default='ls_dr10.tractor',
    help='Fully qualified table name following the format: <schema_name>.<table_name>. Default: ls_dr10.tractor'
  )
  dlcat.add_argument(
    '--types', action='store', nargs='+', default=['REX', 'DEV', 'EXP', 'SER'],
    choices=['PSF', 'REX', 'DEV', 'EXP', 'SER'],
    help=('Morphological types to allow in final table.'
          'By default, only PSF type (stars) are removed. '
          'Possible values: PSF, REX, DEV, EXP, SER. Default: REX DEV EXP SER')
  )
  dlcat.add_argument(
    '--r', action='store', type=float, nargs=2, default=[10, 21],
    help='The magnitude range in band r. Default: 10 21'
  )
  dlcat.add_argument(
    '--noprimary', action='store_true', 
    help='Include no primary objects. By default, only primary objects are included.'
  )
  dlcat.add_argument(
    '--overwrite', action='store_true', 
    help='Use this flag to overwrite the destinaton path if the file exists'
  )
  dlcat.add_argument(
    '--workers', action='store', type=int, default=7,
    help='Number of parallel queries that will be sent to server. Default: 7'
  )
  dlcat.add_argument(
    '--tmp', action='store', default=None,
    help='Temp folder to store partial tables. Default: none'
  )
  dlcat.add_argument(
    '--otmp', action='store_true',
    help='Set this flag to overwrite partial tables in temp folder, if exists'
  )
  
  args = parser.parse_args()
  
  if args.subprog == 'dlcat':
    handle_dlcat(args)
  else:
    parser.print_help()
  

if __name__ == '__main__':
  entrypoint()