import py_compile
import sys
try:
    py_compile.compile(r'c:\Users\Sanskardeep\OneDrive\Desktop\mentor\StudentGrowthPortal\app.py', doraise=True)
    print('✓ app.py syntax OK')
except py_compile.PyCompileError as e:
    print('✗ Syntax error:', e)
    sys.exit(1)
