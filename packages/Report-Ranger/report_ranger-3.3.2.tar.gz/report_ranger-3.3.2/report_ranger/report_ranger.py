import time
from report_ranger.imports import vulnerability
from report_ranger.config import get_config  # Configuration settings within report ranger
from report_ranger.errors import InputError
from report_ranger.report import Report
from report_ranger.template import Template
from report_ranger.templatemapper import process_templatemapper
import os
import jinja2
import logging
from watchdog.observers import Observer
from report_ranger.watcher import Watcher
import argparse

from report_ranger.utils.jinja_helpers import log_jinja2_error

log = logging.getLogger(__name__)

version = "3.3.1"

def main():
    parser = argparse.ArgumentParser(
        description=f"Report Ranger collects together a bunch of markdown files to create a master markdown file that is suitable to use with Pandoc and Latex to build a PDF file. Version {version}.")
    parser.add_argument('-i', '--input', type=str,
                        help='The main report file to process')
    parser.add_argument('-o', '--output', type=str,
                        help='The file to output the final markdown to. If given a directory, the filename will be whatever is suggested by the report or template.')
    parser.add_argument('-f', '--format', type=str,
                        default='', help='The format to target (options are "latex", "pdf-latex", "pdf-typst", "docx", "typst"). Defaults to whatever the extension tells us.')
    parser.add_argument('-w', '--watch', action='store_true', default=False,
                        help='Watch files for changes and recompile if they are identified')
    parser.add_argument('--watch_mode', type=str, default='',
                        help='Watch file mode, can be set to "os" or "modified"')
    parser.add_argument('-m', '--templatemapper', type=str, default='',
                        help='A template mapper file which holds a YAML mapping from a template name to a related file.')
    parser.add_argument('-c', '--config', type=str, default='',
                        help='The location of a config file in YAML format.')
    parser.add_argument('-t', '--template', type=str, default='',
                        help='The template file. Associated images should be in the same directory. Defaults to what is set in the report.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help=f'Turn on verbose mode.')
    parser.add_argument('--version', action='store_true',
                        help=f'Print the version and exit.')

    args = parser.parse_args()

    if args.version:
        print(f"Report Ranger version {version}")
        return

    # Turn on verbose mode
    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s',
                            level=logging.WARNING)

    config = get_config(args.config)

    input = args.input if args.input else config['default_input_file'] if 'default_input_file' in config else None
    if input == None or input == '':
        log.warn("Report Ranger needs a file as input. Please use the -i flag to set an input file.")
        return
    output_file = args.output if args.output else None

    parentdir = os.path.dirname(os.path.join(os.path.curdir, input))

    # Sort out command line format
    default_format = config['default_format'] if 'default_format' in config else None
    format = args.format if args.format else None

    # We need to change the current working directory to the directory of the template otherwise relative
    # paths inside the template won't work. For instance you won't be able to include executivesummary.md
    rr_parent_folder = os.path.abspath(os.path.curdir)

    ctm = config['templatemapper'] if 'templatemapper' in config else {}        
    ctms = config['templatemappers'] if 'templatemappers' in config else []

    templatemapper = process_templatemapper(args.templatemapper, ctm, ctms)

    if args.template:
        if args.template in templatemapper:
            templatefile = templatemapper[args.template]
        else:
            templatefile = os.path.abspath(args.template)
    else:
        templatefile = ''

    os.chdir(parentdir)
    parentdir = '.'
    mdfile = os.path.basename(input)

    # Initialise the report
    try:
        report = Report(
            mdfile,
            templatefile=templatefile,
            templatemapper=templatemapper,
            default_template=config['default_template'])
    except Exception as e:
        log.warn(f"Could not initialise report: {e.args}")
        return
    except:
        log.warn("Could not initialise report.")
        return

    # Pandoc does not support PDF output to stdout, so we need to hack it by
    # making a symlink to /dev/stdout and outputting to that file
    stdout_link = None
    if format == 'pdf' and output_file == '-':
        stdout_link = '/tmp/stdout.pdf'
        os.symlink('/dev/stdout', stdout_link)
        output_file = stdout_link

    # Convert output file path into full path if relative path is given
    if output_file and output_file[0] != '/':
        output_file = os.path.join(rr_parent_folder, output_file)

    if args.watch:
        log.debug("Starting watch")
        try:
            watcher = Watcher(log.debug, "Callback")
            watcher.set_callback(report.process_file, mdfile, format=format, default_format=default_format, output = output_file, default_output_file=config.get('default_output_file'), watcher=watcher)
            watcher.set_watch_mode(args.watch_mode)
            output = report.process_file(mdfile, format=format, default_format=default_format, output = output_file, default_output_file=config.get('default_output_file'), watcher=watcher)
            if args.watch_mode != "modified":
                log.info("Setting watch mode to os")
                observer = Observer()
                observer.schedule(watcher, parentdir, recursive=True)
                observer.start()
                try:
                    while True:
                        time.sleep(5)
                        watcher.run()
                finally:
                    observer.stop()
                    observer.join()
            else:
                log.info("Setting watch mode to modification time")
                while True:
                    try:
                        time.sleep(5)
                        watcher.run()
                    except InputError as ie:
                        log.error("Input Error: {}".format(ie.message))
                        exit()
                    except jinja2.exceptions.TemplateSyntaxError as error:
                        log.error("Final report processing Jinja2 error: {} at lineno {} for file {}".format(
                            error.message, error.lineno, error.filename))
                        log_jinja2_error(mdfile, error)
                        exit()

        except InputError as ie:
            log.error("Input Error: {}".format(ie.message))
        except jinja2.exceptions.TemplateSyntaxError as error:
            log.error("Final report processing Jinja2 error: {} at lineno {} for file {}".format(
                error.message, error.lineno, error.filename))
            log_jinja2_error(mdfile, error)
    else:
        try:
            output = report.process_file(mdfile, format=format, default_format=default_format, output = output_file, default_output_file=config.get('default_output_file'))
        except InputError as ie:
            log.error("Input Error: {}".format(ie.message))
            exit()
        except jinja2.exceptions.TemplateSyntaxError as error:
            log.error("Final report processing Jinja2 error: {} at lineno {} for file {}".format(
                error.message, error.lineno, error.filename))
            log_jinja2_error(mdfile, error)
            exit()

        # If we're outputting to stdout, remove the link
        if stdout_link and os.path.exists(stdout_link):
            os.remove(stdout_link)
