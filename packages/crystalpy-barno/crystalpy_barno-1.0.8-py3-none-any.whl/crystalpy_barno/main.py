import os
from datetime import datetime
from ReportsClasses import *

# Set database connection details externally
DatabaseConnectionHelper.set_connection_details(
    server_name="NjmsReport",
    database_name="Nishka",
    user_id="sa",
    password="nimbus@123"
)

voucher_no = "2425SOPDKNB0158"
pdf_dir = os.path.join(cwd, 'pdf')
pdf_dir_sales = os.path.join(pdf_dir, 'sales')
pdf_filepath_sale = os.path.join(pdf_dir_sales, f"{voucher_no}.pdf")
pdf_dir = os.path.join(cwd, 'pdf')
pdf_dir_reports = os.path.join(pdf_dir, 'reports')
pdf_filepath_stock = os.path.join(pdf_dir_reports, f"Stock_Report.pdf")

if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

if not os.path.exists(pdf_dir_sales):
    os.makedirs(pdf_dir_sales)

if not os.path.exists(pdf_dir_reports):
    os.makedirs(pdf_dir_reports)

params = {
    "source_no": "2425SOEDKNB1981",
    "voucher_no": voucher_no,
    "le_code": "AJPL",
    "user_code": "NIM",
    "s_inc_mak": True,
    "s_emp_name": "emp_name_value",
    "le_name": "le_name_value",
    "wh_name": "wh_name_value",
    "wh1": "wh1_value",
    "wh2": "wh2_value",
    "whp1": "whp1_value",
    "whp2": "whp2_value",
    "s_print_hdr": True,
}

SaleSnippet.SaleMemo(
    report_filename=os.path.join(cwd, 'rpt/Sale_Memo_IncludeMaking.rpt'),
    output_path=pdf_filepath_sale,
    params=params
)

params = {
    "s_from_date": '08/21/2024',
    "s_to_date": '08/21/2024',
    "s_product": '',
    "cn": '',
    "add": '',
    "city": '',
    "coun": '',
    "s_check": str(2),
    "s_from_date_formula": datetime.strptime('08/21/2024', '%m/%d/%Y'),
    "s_to_date_formula": datetime.strptime('08/21/2024', '%m/%d/%Y'),
    "s_purity": '',
    "s_size": '',
    "s_cut": '',
    "s_color": '',
    "s_style": '',
    "s_batch": '',
    "s_le_code": 'AJPL',
    "s_wh": '',
    "s_article": '',
    "s_compl": '',
    "s_mnf": '',
    "s_hierarchy": '',
    "s_ex_chk": 1,
    "s_sku_type": str(0),
    "s_ex_old": False,
    "s_bk_type": str(0),
    "s_user": '',
    "s_whn": '',
    "s_repair": False,
    "s_department": ''
}

StockSnippet.SummaryClosing(
    report_filename=os.path.join(cwd, 'rpt/Summary_Closing_Report.rpt'),
    output_path=pdf_filepath_stock,
    params=params
)

# pip install pythonnet

