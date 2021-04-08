import argparse
import pathlib
import datetime

from exif import Image


def main(search: pathlib.Path, target: pathlib.Path, recursive=True, print_progress=False, verbose=False):
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
    for k, d in dates.items():
        for i, p in enumerate(d):
            file_name = (f'{k.year:02}{k.month:02}{k.day:02}',
                         f'{k.hour:02}{k.minute:02}{k.second:02}',
                         f'{i+1:02}.JPG')
            file_name = '_'.join(file_name)
            new_path = target / file_name
            p.rename(new_path)


if __name__ == '__main__':
    prsr = argparse.ArgumentParser()
    prsr.add_argument('search')
    prsr.add_argument('target')
    prsr.add_argument('-r', '--recursive', action='store_true')
    prsr.add_argument('-p', '--progress', action='store_true')
    prsr.add_argument('-v', '--verbose', action='store_true')
    args = prsr.parse_args()

    arg_search = pathlib.Path(args.search)
    arg_target = pathlib.Path(args.target)
    main(arg_search, arg_target,
         recursive=args.recursive,
         print_progress=args.progress,
         verbose=args.verbose)
