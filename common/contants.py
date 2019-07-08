import os
base_dir = os.path.dirname(os.path.dirname(__file__))

case_dir = os.path.join(base_dir,'data','pay_OMAtestcases.xlsx')

global_dir = os.path.join(base_dir,'config/global.cfg')

uat_dir = os.path.join(base_dir,'config/uat.cfg')

dev_dir = os.path.join(base_dir,'config/dev.cfg')
test_dir = os.path.join(base_dir,'config/test.cfg')
print(case_dir)