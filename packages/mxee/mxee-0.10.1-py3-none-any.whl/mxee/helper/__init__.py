import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from rich.pretty import pprint as PP
import subprocess



def finder_expose(filename_or_path):
    subprocess.call("""/bin/bash -c 'open -R "%s"'""" % filename_or_path, shell=True)


def xlsx_out(filename:str, sheets:dict):
    """Simple Excel Writer.


    mxee.helper.xlsx_out(
        "test2.xlsx",
        sheets={
            'blatt1': {
                'data': [['A', 'B', 'C'],['120']],
                'cw':{'A': 50}
            }
        }
    )
"""
    try:
        with pd.ExcelWriter(filename) as ew:

            for k in sheets.keys():
                dat = sheets[k]['data']

                dfc = pd.DataFrame(dat) # dataframe current
                dfc.to_excel(ew, sheet_name=k, index=False, header=False)
            
                col_widths = {}
                if 'cw' in sheets[k].keys():
                    col_widths = sheets[k]['cw']

                for wdef_k in col_widths.keys():
                    ew.sheets[k].column_dimensions[wdef_k].width = col_widths[wdef_k]

                for header0_idx in range(0, len(dat[0])):
                    column_letter = get_column_letter(header0_idx+1)
                    ew.sheets[k][column_letter + "1"].font = Font(bold=True)
                
                ew.sheets[k].freeze_panes = ew.sheets[k]['A2']

    except Exception as e:
        import os
        os.unlink(filename)
        PP(e)
