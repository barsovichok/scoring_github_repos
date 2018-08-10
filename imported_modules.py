source = '''from django import core
import fiasko_bro, django
import fiasko_bro, django
import flask
import bs4
'''


def find_import_modules(files):
    imported_modules = []
    for file in files:
        file = open(file, 'r')
        for line in file:
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
                    from_module = from_module.lower()
                    imported_modules.append(from_module)
                else:
                    file.close()
                    break
    return imported_modules


def delete_doubled_assignments(imported_modules):
    list_modules = set(imported_modules)
    list_modules = list(list_modules)
    return list_modules


def print_modules(list_modules):
    print(list_modules)


if __name__ == '__main__':
    imported_modules = find_import_modules(source)
    list_modules = delete_doubled_assignments(imported_modules)
    print_modules(list_modules)
