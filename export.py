from pathlib import Path

from traitlets.config import Config
from traitlets import Unicode
import nbformat as nbf
from nbconvert.exporters import PDFExporter

c = Config()



# Configure our tag removal
c.TagRemovePreprocessor.remove_cell_tags = ("no-export", "no-export-pdf",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ('remove_output',)
c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)

# Configure figure extraction
# c.ExtractOutputPreprocessor.output_filename_template = Unicode(
#     "{unique_key}_{cell_index}_lol_{index}{extension}"
#     ).tag(config=True)
c.ExtractOutputPreprocessor.output_filename_template = "{unique_key}_{cell_index}_lol_{index}{extension}"

# Configure and run out exporter
c.PDFExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

# c.PDFExporter.preprocessors = ['nbconvert.preprocessors.ExtractOutputPreprocessor']


exporter = PDFExporter(config=c)

# filename = "test_export.ipynb"
filename = "bmw_analysis.ipynb"

output, resources = exporter.from_filename(filename)

print("Exported figures")
print(sorted(resources['outputs']))

# print("resources", resources)
outfile = Path(filename).with_suffix(".pdf")
if isinstance(output, bytes):
    output_type = "wb"
else:
    output_type = "w"
    
with open(outfile, output_type) as fil:
    fil.write(output)
print(outfile)
