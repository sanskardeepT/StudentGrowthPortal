from jinja2 import Environment, FileSystemLoader
import sys
path = r'c:\Users\Sanskardeep\OneDrive\Desktop\mentor\StudentGrowthPortal\templates'
try:
    env = Environment(loader=FileSystemLoader(path))
    env.get_template('mentor_dashboard.html')
    print('TEMPLATE OK')
except Exception as e:
    print('ERROR')
    print(e)
    sys.exit(1)
