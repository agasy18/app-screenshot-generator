from argparse import ArgumentParser
import os
from subprocess import check_call, check_output

parser = ArgumentParser()
parser.add_argument('--screenshots', type=str, default='screenshots')
parser.add_argument('--output', type=str, default='output')
parser.add_argument('--sizes', type=str, action='append', default=[
    'phone6.7=1290x2796',
    'phone5.5=1242x2208',
    'ipad6=2732x2048',
])
parser.add_argument('--fill_color', type=str, default='auto', help='auto, srgb(255,255,255), #ffffff, white, etc.')
parser.add_argument('--auto_color_pixel', type=str, default='1,1')
parser.add_argument('--supported_formats', type=str, action='append', default='png,jpg,jpeg')


def parse_sizes(sizes):
    result = {}
    for size in sizes:
        name, dimensions = size.split('=')
        dimensions = [tuple(map(int, d.split('x'))) for d in dimensions.split(',')]
        result[name] = dimensions
    return result

def get_screenshots(screenshots, supported_formats):
    return list(filter(lambda x: x.split('.')[-1].lower() in supported_formats, os.listdir(screenshots)))


def generate(screenshot, size, dimension, args):
    input_path = os.path.join(args.screenshots, screenshot)
    output_path = os.path.join(args.output, size, screenshot.replace('.', f'_{dimension[0]}x{dimension[1]}.'))
    print(f'Generating {output_path}')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if args.fill_color == 'auto':
        # get edge color
        fill = check_output(['convert', input_path, '-format', f'%[pixel:u.p{{{args.auto_color_pixel}}}]', 'info:']).decode('utf-8').strip()
    else:
        fill = f'"{args.fill_color}"'
    print(f'Filling with {fill}')


    original_dimension = check_output(['identify', '-format', '%wx%h', input_path]).decode('utf-8').strip().split('x')

    scale = min(dimension[0] / int(original_dimension[0]), dimension[1] / int(original_dimension[1]))
    print(f'Scaling by {scale}')
    # scale the image without filling
    check_call(['convert', input_path, '-resize', f'{int(scale * 100)}%', output_path])
    # fill the image

    check_call(['convert', output_path, '-gravity', 'center', '-background', fill, '-extent', f'{dimension[0]}x{dimension[1]}', output_path])




def main(args):
    print(f'Generating screenshots from {args.screenshots} to {args.output}')
    check_call(['rm', '-r', args.output])
    sizes = parse_sizes(args.sizes)
    print(f'Using sizes: {sizes}')
    screenshots = get_screenshots(args.screenshots, args.supported_formats.split(','))
    print(f'Found screenshots: {screenshots}')
    for screenshot in screenshots:
        print(f'Generating {screenshot}')
        for size, dimensions in sizes.items():
            print(f'Generating {size}')
            for dimension in dimensions:
                print(f'Generating {dimension}')
                generate(screenshot, size, dimension, args)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)