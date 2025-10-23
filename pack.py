import os
import zipfile
import datetime

def pack(folder_name):
    """
    Packages selected project files into a zip archive,
    excluding virtual environments and unnecessary directories,
    only inside the specified folder.
    """
    # Remove old archives in the folder
    for item in os.listdir(folder_name):
        if item.endswith(".zip"):
            os.remove(os.path.join(folder_name, item))

    dt = datetime.datetime.now().strftime('%H-%M_%d.%m.%y')
    output_zip = os.path.join(folder_name, f'submission-{dt}.zip')

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_name):
            # Skip unwanted directories inside the folder
            dirs[:] = [d for d in dirs if d not in ('venv', '.venv', '__pycache__', '.git', '.idea', '.vscode')]

            current_dir = os.path.basename(root)

            for file in files:
                file_path = os.path.join(root, file)
                # Make archive path relative to the folder_name, so the zip structure is correct
                archive_path = os.path.relpath(file_path, folder_name)

                # Only include specific files/folders
                if (
                    file in ['requirements.txt', 'manage.py', 'caller.py']
                    or current_dir in ['main_app', 'orm_skeleton', 'migrations']
                ):
                    zipf.write(file_path, archive_path)

    print('Submission created!')

if __name__ == '__main__':
    folder = input('Folder name: ')
    pack(folder)
