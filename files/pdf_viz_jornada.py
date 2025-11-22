import os
import camelot
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#print(matplotlib.get_backend())

file_name = "corretora_jornada_de_dados (1)"

path = os.path.abspath(f"files/jornada/{file_name}.pdf")

tables = camelot.read_pdf(path,
                          pages="1-end",
                          flavor='stream',
                          table_areas=['65,558,500,303'],
                          columns=['70,106,157,219,285,337,383,448'],
                          strip_text=[" .\n"]
                          )
print(tables[0].parsing_report)

#camelot.plot(tables[0], kind="contour")
#plt.show()

print(tables[0].df)

print("Pause")

