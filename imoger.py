#!/usr/bin/env python3
import pathlib
import datetime
import shutil

try:
    from exif import Image
except ImportError:
    import sys
    sys.stderr.write('exif not available. Install with ')
    exit(1)


def main(search: pathlib.Path, target: pathlib.Path,
         recursive=True, print_progress=False,
         date_dirs=False,
         move=False, verbose=False):
    search_string = None
    if recursive:
        search_string = '**/*.JPG'
    else:
        search_string = '*.JPG'

    dates = {}
    images = list(search.glob(search_string))
    n_images = len(images)
    steps = [int(x * (n_images / 10)) for x in range(10)]
    for i, image in enumerate(images):
        if i in steps and print_progress:
            print(f'{((i / n_images) * 100)}%')

        try:
            if verbose:
                print(str(image.resolve()))

            with image.resolve().open('rb') as f:
                exif_image = Image(f)
                date, time = exif_image.datetime_original.split(' ')
                year, month, day = map(int, date.split(':'))
                hour, minute, second = map(int, time.split(':'))
                dt = datetime.datetime(year=int(year),
                                       month=int(month),
                                       day=int(day),
                                       hour=int(hour),
                                       minute=int(minute),
                                       second=int(second))

                if dt not in dates:
                    dates[dt] = list()
                dates[dt].append(image.resolve())
        except KeyError:
            print(f'No exif: {image.resolve()}')

    print('Start copying')
    for date, file_list in dates.items():
        for i, path in enumerate(file_list):
            file_name = (f'{date.year:02}{date.month:02}{date.day:02}',
                         f'{date.hour:02}{date.minute:02}{date.second:02}',
                         f'{i+1:02}.JPG')
            file_name = '_'.join(file_name)

            new_path = target
            if date_dirs:
                new_path = new_path / \
                           f'{date.year:04}' / \
                           f'{date.month:02}' / \
                           f'{date.day:02}'
                if not new_path.exists():
                    new_path.mkdir(parents=True)
            new_path = new_path / file_name
            if verbose:
                print(f'Copy {path} -> {new_path}')
            if move:
                path.rename(new_path)
            else:
                shutil.copyfile(path, new_path)


if __name__ == '__main__':
    import argparse
    prsr = argparse.ArgumentParser()
    prsr.add_argument('search', help='Path to search in')
    prsr.add_argument('target', help='Files will be transfered to this location')
    prsr.add_argument('-r', '--recursive', action='store_true',
                      help='Search recursive')
    prsr.add_argument('-p', '--progress', action='store_true',
                      help='Show progress')
    prsr.add_argument('-m', '--move', action='store_true',
                      help='Instead of copying move the files')
    prsr.add_argument('-v', '--verbose', action='store_true',
                      help='Print more information')
    prsr.add_argument('-d', '--dir', action='store_true',
                      help='Maintain directory structure YYYY/MM/DD/file.JPG')
    args = prsr.parse_args()

    arg_search = pathlib.Path(args.search)
    arg_target = pathlib.Path(args.target)
    main(arg_search, arg_target,
         move=args.move,
         date_dirs=args.dir,
         recursive=args.recursive,
         print_progress=args.progress,
         verbose=args.verbose)
