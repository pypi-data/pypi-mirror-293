import os
from pathlib import Path
import shutil
import subprocess
from report_ranger.output_formatter.outputformatter import OutputFormatter, headeralias
import re
import jinja2
import mistune
from report_ranger.markdown_renderer.typstrenderer import TypstRenderer
from report_ranger.table import Table
import logging
from report_ranger.utils.jinja_helpers import log_jinja2_error
from report_ranger.utils.mdread import process_template


log = logging.getLogger(__name__)

class TypstFormatter(OutputFormatter):
    def __init__(self, templateheaders=dict(), timer=None, watcher=None):
        OutputFormatter.__init__(self, templateheaders, timer, watcher=watcher)
        self.figformat = "svg"
        self.env.set_static('table', self._register_table)
        log.debug(f"Typst init watcher: {self.watcher}")

    def escape(self, text):
        ''' Escape the given text based on the format we're working with

        :param text: a plain text message
        :return: the message escaped to appear correctly in Typst
        '''
        if type(text) is not str:
            log.warning(
                "escape function given {} which is not a string. Returning ''".format(text))
            return ""

        conv = {
            '&': r'\&',
            '"': r'\\"',
            '\'': r'\\\'',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '[': r'\[',
            ']': r'\]',
            '@': r'\@',
            '\\': r'\\'
        }
        regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(
            conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)
    
    def _register_table(self, *args, **kwargs):
        ca = self.env.get('ca')
        return ca._register_string(self.table(*args, **kwargs))

    def _translate_alignment(self, alignment):
        # Translates from 'l','c','r','j' to typst
        if alignment == 'l':
            return 'left'
        if alignment == 'r':
            return 'right'
        if alignment == 'c':
            return 'center'
        return 'left'

    def table(self, table, options={}, **tableargs):
        ''' This function formats the table in either latex or markdown, depending on the output. '''
        typst = ""

        t = Table(table, env=self.env, **tableargs)

        # If there's no actual table, warn and exit
        if t.width == 0:
            log.warn("Table is now empty. Printing an empty string.")
            return ""

        #TODO: Add banding

        columndef = ",".join(["auto" if cw == 0 else f"{cw}fr" for cw in t.colwidths])

        cells = []
        colors = self.colors.getcolors()

        for i in range(len(t.table)):
            for j in range(len(t.table[i])):
                parameters = []
                textparameters = []

                lr = mistune.create_markdown(renderer=TypstRenderer())

                # Process the typst text
                cell = lr(str(t.table[i][j]))

                style = self.tablestyles.getstyle(t.cellstyles[i][j])

                if t.colspan[i][j] < 1:  # This column is being overwritten in some way
                    continue
                elif t.colspan[i][j] > 1:
                    parameters.append(f"colspan: {t.colspan[i][j]}")
                if t.rowspan[i][j] < 1:  # This column is being overwritten in some way
                    continue
                elif t.rowspan[i][j] > 1:
                    parameters.append(f"rowspan: {t.rowspan[i][j]}")
                
                # cell alignment, first try cellalign, then style
                if t.cellalign[i][j] != '':
                    parameters.append(f"align: {self._translate_alignment(t.cellalign[i][j])}")
                elif style and style['alignment'] != '':
                    parameters.append(f"align: {self._translate_alignment(style['alignment'])}")
                elif len(t.colalign) > j and t.colalign[j] != '':
                    parameters.append(f"align: {self._translate_alignment(t.colalign[j])}")
                
                if style:
                    if style['color']:
                        color = style['color']
                        if color in colors:
                            color = colors[color]
                        textparameters.append(f'fill: rgb("{color}")')
                    if style['bgcolor']:
                        color = style['bgcolor']
                        if color in colors:
                            color = colors[color]
                        parameters.append(
                            f'fill: rgb("{color}")')
                    if style['bold']:
                        textparameters.append('weight: "bold"')
                    if style['italic']:
                        textparameters.append('style: "italic"')
                    if style['size']:
                        s = style['size']
                        sizes = {
                            'tiny': '0.5em',
                            'small': '0.8em',
                            'normal': '',
                            'large': '1.3em',
                            'Large': '1.7em',
                            'LARGE': '2em',
                            'huge': '3em',
                            'Huge': '4em'
                        }
                        if s in sizes:
                            textparameters.append(f'size: {sizes[s]}')

                if len(textparameters) > 0:
                    cell = f"#text({','.join(textparameters)})[{cell}]"
                if len(parameters) > 0:
                    cell = f"table.cell({','.join(parameters)})[{cell}]"
                else:
                    cell = f"[{cell}]"
                
                cells.append(cell)

        tablespan = ",\n".join(cells)
        
        typst = f'#table(columns: ({columndef}), {tablespan})'

        return typst

    def newsection(self):
        ca = self.env.get('ca')
        return ca._register_string("#new_section")

    def newpage(self):
        ca = self.env.get('ca')
        return ca._register_string("#pagebreak(weak: true)")
    
    def _build_markdown_headers(self, headers):
        return ''

    def headers(self):
        return ''

    def end(self):
        ca = self.env.get('ca')
        return ca._register_string("#last_page")

    def _build_markdown(self, templatemarkdown):
        # A giant string to put all the output markdown into
        markdown = ""

        log.debug("Outputting markdown")
        env = self.env.get_env()

        try:
            j2template = jinja2.Template(templatemarkdown)
            processedtemplate = j2template.render(env)
            markdown += processedtemplate

            self._warn_in_text(self.templateheaders, env, markdown)


        except jinja2.exceptions.TemplateSyntaxError as error:
            log.error(
                "Error in processing the final template: {}".format(error.message))
            log_jinja2_error(markdown, error)
            raise Exception("Error reading the final template: {} at lineno {} for file {}".format(
                error.message, error.lineno, error.filename))
        except jinja2.exceptions.TemplateError as error:
            log.error(
                "Error in processing the final template: {}".format(error.message))
            raise Exception("Error reading the final template: {}".format(
                error.message))

        return markdown
    
    def _join_path(self, root_dir, dir_name) -> Path:
        root_dir = Path(root_dir)
        joined_dir = root_dir / dir_name
        if root_dir in joined_dir.parents:
            return joined_dir
        raise Exception(f"{joined_dir} not a subdirectory of {root_dir}")
    
    def _copy_datadir(self, dir_name, dest='typst_template'):
        try:
            data_dir:Path = self._join_path(self.templateheaders['templatedir'], dir_name)
            dest_dir:Path = self._join_path(os.path.curdir, dest)
            
            if not dest_dir.exists():
                log.info(f"Copying Typst data directory '{data_dir}' to '{dest_dir}'")
                shutil.copytree(data_dir, dest_dir)
        except Exception as e:
            log.warn(f"Error copying Typst data directory: {e.args}")

    def _output_typst_var(self, variable):
        if type(variable) == str:
            return f'"{self.escape(variable)}"'
        if type(variable) == dict:
            vars = []
            for key, var in dict.items():
                new_key = re.sub(r'[^a-zA-Z0-9]', '', key)
                vars.append(f'{new_key}:{self._output_typst_var(var)}')
            return f"({','.join(vars)})"
        if type(variable) == list:
            vars = []
            for var in variable:
                vars.append(self._output_typst_var(var))
            return f"({','.join(vars)})"
        else:
            return f'"{str(variable)}"'
                            
    def output(self, markdown, outputfile=''):
        output = self._build_markdown(markdown)

        lr = mistune.create_markdown(renderer=TypstRenderer())

        # Process the typst text
        output = lr(output)

        # Get the template and data directory
        if 'typst' in self.templateheaders:
            if 'template' in self.templateheaders['typst']:
                templatefile = os.path.join(
                    self.templateheaders['templatedir'], self.templateheaders['typst']['template'])
                with open(templatefile) as tf:
                    output = tf.read() + output
            if 'data_dir' in self.templateheaders['typst']:
                data_dir = self.templateheaders['typst']['data_dir']
                log.info(f"Copying data dir {data_dir}")
                self._copy_datadir(data_dir, 'typst_template')
            if 'libs_dir' in self.templateheaders['typst']:
                self._copy_datadir(self.templateheaders['typst']['libs_dir'], 'libs')
            if 'template_variables' in self.templateheaders['typst']:
                # Add in env
                docenv = self.env.get_env()
                for var in self.templateheaders['typst']['template_variables']:
                    if var in docenv.keys():
                        output = f'#let {var} = {self._output_typst_var(docenv[var])}\n' + output
                    else:
                        output = f'#let {var} = none\n' + output


        # Content assistant parsing
        output = self.env.get('ca').parse_register(self, output)

        if self.docformat and self.docformat == 'pdf' and outputfile[-4:].lower() == '.pdf':
            outputfilebase = outputfile[:-4]
        elif outputfile[-4:].lower() == '.typ':
            outputfilebase = outputfile[:-4]
        else:
            outputfilebase = outputfile

        log.debug("Writing Typst")
        with open(f"{outputfilebase}.typ", 'w') as fh:
            fh.write(output)
            log.info("Finished writing Typst file")

        if self.docformat and self.docformat == 'pdf':
            log.debug("Writing PDF")
            log.debug(f"Typst file: {outputfilebase}.typ")
            # Use Typst to compile
            typst_arguments = ['typst', 'compile', f'{outputfilebase}.typ']
            process = subprocess.run(typst_arguments,
                                    input=output,
                                    universal_newlines=True)
            log.info("PDF file has been compiled.")

        return output
