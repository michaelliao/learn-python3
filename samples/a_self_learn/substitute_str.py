import re, os

lg_name = 'mydph0310.hpeswlab.net'
f = open(r'C:\GitHub\LT-LR-QA\app\HPE.PerfCoreTests\HPE.PerfCoreTests.Controller\TestData\TruClientLoad.properties', 'r+')
f_content = f.read()
print('Properties before change: \n' + f_content)

f_content = re.sub(r'\nhost_name=mydph\d{4}\.hpeswlab\.net\n', '\nhost_name=' + lg_name + '\n', f_content)
f.seek(0)
f.truncate()
f.write(f_content)
print('Properties after change: \n' + f_content)
f.close()
