import argparse
import os
import pathlib
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e", "--ext", help="File media extension", default='png')
# parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
# parser.add_argument("-B", "--block-size", help="checksum blocksize")
# parser.add_argument("--ignore-existing", action="store_true", help="skip files that exist")
# parser.add_argument("--exclude", help="files to exclude")
parser.add_argument("-s", "--src_dir", help="Source directory with media files", required=True)
# parser.add_argument("-d", "--dest_html_file", help="Destination screenshot report html file output", required=True)
args = parser.parse_args()


def render_html(path_dir: str, file_media_ext: str):
    # path = "/Users/duong/Desktop"
    user_dir = pathlib.Path(path_dir)
    png_files = user_dir.rglob(f"*.{file_media_ext}")

    test_cases_dict = {}

    for file in png_files:
        if file.is_file():
            file_name = pathlib.Path(file).name
            file_name_without_ext = pathlib.Path(file).stem

            # print(f'{file_name} {file_name_without_ext}')

            last_index = file_name_without_ext.rindex('_')
            if last_index >= 0:
                test_case_name = file_name_without_ext[0:last_index]
                lang = file_name_without_ext[last_index + 1:]
                # print(f'{test_case_name} {lang}')

                if test_case_name in test_cases_dict:
                    test_case = test_cases_dict[test_case_name]
                    test_case[lang] = file_name
                else:
                    test_case = {
                        lang: file_name,
                    }
                    test_cases_dict[test_case_name] = test_case

    test_cases = []
    for key, value in test_cases_dict.items():
        test_cases.append({
            'name': key,
            'vi_image_path': value['vi'],
            'en_image_path': value['en'],
        })

    # TODO remove test case info hard code here
    report = {
        'request_id': '20193812903',
        'requested_at': '2023-09-11 10:12',
        'customer_code': 'C091081018',
        'unit_code': 'U-0909',
        'test_cases': test_cases
    }

    if len(test_cases) > 0:
        e = Environment(loader=FileSystemLoader('templates/'))
        template = e.get_template("screenshot_report.html")

        output_html = template.render(report=report)
        path_output_html = os.path.join(path_dir, 'index.html')
        with open(path_output_html, "w") as report_page:
            report_page.write(output_html)


if __name__ == '__main__':
    render_html(path_dir=args.src_dir, file_media_ext=args.ext)
