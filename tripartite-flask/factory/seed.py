# Seed the database by calling the imported data generators
from user_tenant_factory import *
from class_factory import *

# Function calls
print("## RUNNING ##")
print('generating user types..')
generate_user_types()
print('generating tenants...')
generate_tenants()
print('generating teachers')
generate_teachers()
print('generating students with parents...')
generate_parent_student()
print('generating random students...')
generate_random_students()
print('generating subjects...')
generate_subjects()
print('generating classes...')
generate_classes()
print('generating assignments...')
generate_assignments()
print('generating submissions... ')
generate_submissions()