source = '''from django import core
import fiasko_bro, django
import fiasko_bro, django
import flask
import bs4
'''

imported_modules = []

def find_import_modules(imported_modules):
    for line in source.split('\n'):
        if not line.strip():
            continue
        if line.startswith('from') or line.startswith('import'):
            if line.startswith('import'):
                imported_modules += [l.strip() for l in line[7:].split(',')]
            elif line.startswith('from'):
                from_module = line[5:].split(',')
                from_module = from_module[0]
                from_module = from_module.split(' ')
                from_module = from_module[0]
                imported_modules.append(from_module)
            else:
                break

def delete_doubled_assignments(imported_modules):
    list_modules = set(imported_modules)
    list_modules = list(list_modules)
    return list_modules

def print_modules(list_modules):
    print(list_modules)


find_import_modules(imported_modules)
list_modules = delete_doubled_assignments(imported_modules)
print_modules(list_modules)