import datetime
from pathlib import Path

from labnas.remote.imaging import ImagingNas


def delete_if_empty(folder: Path, nas: ImagingNas, trash: Path) -> None:
    if nas.is_empty(folder):
        trash_name = "_".join(folder.parts)
        trash_target = trash / trash_name
        nas.move_folder(folder, trash_target)
        print(f"{folder} deleted.")


def get_date_from_folder(folder: Path) -> datetime.date:
    date_string = folder.name
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    date = date.date()
    return date




def check_eyetracking(recording_folder: Path, nas: ImagingNas) -> None:
    files, folders = nas.list_files_and_folders(recording_folder)
    has_right = False
    has_left = False
    right_size = None
    left_size = None
    for folder in folders:
        if folder.name == "right_eye":
            has_right = True
        elif folder.name == "left_eye":
            has_left = True
        sub_files, sub_folders = nas.list_files_and_folders(folder)
        for file in sub_files:
            # print(file)
            pass
        for f in sub_folders:
            print(f)
    if not has_right:
        raise FileNotFoundError(f"{recording_folder / 'right_eye'} does not exist.")
    if not has_left:
        raise FileNotFoundError(f"{recording_folder / 'left_eye'} does not exist.")
