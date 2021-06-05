from pathlib import Path

from traitlets.config import Config
from traitlets import Unicode
import nbformat as nbf
# from nbconvert.exporters import PDFExporter
from nbconvert.exporters import MarkdownExporter
from nb2hugo.exporter import HugoExporter
from nb2hugo.writer import HugoWriter
from nb2hugo.preprocessors import (FrontMatterPreprocessor, FixLatexPreprocessor,
                                   ImagesPreprocessor, RawPreprocessor)
c = Config()



# Configure our tag removal
c.TagRemovePreprocessor.remove_cell_tags = ("pdf-ignore",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ('remove_output',)
c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)

# Configure figure extraction
# c.ExtractOutputPreprocessor.output_filename_template = Unicode(
#     "{unique_key}_{cell_index}_lol_{index}{extension}"
#     ).tag(config=True)
# c.ExtractOutputPreprocessor.output_filename_template = "{unique_key}_{cell_index}_lol_{index}{extension}"

# Configure and run out exporter
c.HugoExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor",
                                FrontMatterPreprocessor, FixLatexPreprocessor,
                                ImagesPreprocessor, RawPreprocessor]

# Ensure that we get markdown before html, since goldmark does not take html
c.NbConvertBase.display_data_priority = ['text/markdown',
                       'text/html',
                       'image/svg+xml',
                       'text/latex',
                       'image/png',
                       'image/jpeg',
                       'text/plain'
                       ]

# c.PDFExporter.preprocessors = ['nbconvert.preprocessors.ExtractOutputPreprocessor']

# import IPython
# ip = IPython.get_ipython()
# html_formatter = ip.display_formatter.formatters["text/html"]
# print(html_formatter)

exporter = HugoExporter(config=c)

writer = HugoWriter(config=c)

# filename = "test_export.ipynb"
filename = "bmw_analysis.ipynb"

output, resources = exporter.from_filename(filename)

site_dir = "/home/jens/gits/hugo-resume/"
section = "blog/bmw/"

writer._write_resources_images(resources, site_dir, section)
writer._write_markdown(output, resources, site_dir, section)

# print("Exported figures")
# print(sorted(resources['outputs']))

# # print("resources", resources)
# outfile = Path(filename).with_suffix(".md")
# if isinstance(output, bytes):
#     output_type = "wb"
# else:
#     output_type = "w"
    
# with open(outfile, output_type) as fil:
#     fil.write(output)
# print(outfile)
