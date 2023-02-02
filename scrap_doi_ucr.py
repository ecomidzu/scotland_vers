from pybliometrics.scopus import ScopusSearch
import pandas as pd

d = ScopusSearch(query='(KEY(sanctions) OR ABS(sanctions) OR TITLE(sanctions)) AND SUBJAREA(ECON)', subscriber=False)
new = pd.DataFrame(d.results)
new.to_excel('ukr_res.xlsx')