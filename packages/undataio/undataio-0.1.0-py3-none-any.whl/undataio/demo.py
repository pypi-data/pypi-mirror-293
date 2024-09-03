from undata import upload, parser

# file = r'Z:\xll\pdftest\test8'
#
# res = upload(token='1a785b15b8374e358e722a484c7b0dfa', file_lir_path=file)
#
# print(res)

res = parser(token='1a785b15b8374e358e722a484c7b0dfa', file_name='短期谨慎主动杠杆产品安全垫品种交易型基金周报20140915.pdf,漩涡中的信用衍生产品.pdf')

print(res)
