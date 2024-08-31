import os


files_to_create = [
    'setup.py',
    'README.md',
    'requirements.txt',
    'test/',
    'src/helloworld_by_Shaukat/__init__.py',
    'src/helloworld_by_Shaukat/helloworld.py'
]


for filepath in files_to_create:
    dirname, filename = os.path.split(filepath)

    if dirname != "":
        os.makedirs(dirname, exist_ok=True)
        print(f"Created directory: {dirname}")
    
    if filename != "":
        with open(filepath, 'w'):
            pass
        print(f"Created file: {filepath}")

print("Done")