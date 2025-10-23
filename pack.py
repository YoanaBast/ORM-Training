import os
import zipfile
import datetime

def pack(folder_name):
    """
    Function adapted from Cvetan Tomov (h1n0t0r1)
    Packages selected project files into a zip archive,
    excluding virtual environments and unnecessary directories,
    added input option for folders as I will split my project into dirs.
    """
    # Remove old archives !
    for item in os.listdir(folder_name):
        if item.endswith(".zip"):
            file_path = os.path.join(folder_name, item)
            os.remove(file_path)

    dt = datetime.datetime.now().strftime('%H-%M_%d.%m.%y')
    output_zip = os.path.join(folder_name, f'submission-{dt}.zip')

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(os.getcwd()):
            # Skip unwanted directories (prevents descending into them)
            dirs[:] = [d for d in dirs if d not in ('venv', '.venv', '__pycache__', '.git', '.idea', '.vscode')]

            current_dir = os.path.basename(root)

            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, os.getcwd())

                # Only include specific files/folders
                if (
                    file in ['requirements.txt', 'manage.py', 'caller.py']
                    or current_dir in ['main_app', 'orm_skeleton', 'migrations']
                ):
                    zipf.write(file_path, archive_path)

    print('Submission created!')

if __name__ == '__main__':
    pack(input('Folder name: '))
