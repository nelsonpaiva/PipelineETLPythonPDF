import os
import camelot
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#print(matplotlib.get_backend())

file_name = "Redrex - Fatura (1)"

path = os.path.abspath(f"files/redrex/{file_name}.pdf")

tables = camelot.read_pdf(path,
                          pages="1-end",
                          flavor='stream',
                          )
print(tables[0].parsing_report)

camelot.plot(tables[0], kind="contour")
plt.show()

print("Pause")

