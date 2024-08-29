from typing import Dict, List, Union, Optional
try:
    from typing import Literal
except:
    from typing_extensions import Literal

import numpy as np
import pandas as pd
import os

from simba.utils.data import detect_bouts
from simba.utils.enums import Methods
from simba.utils.errors import ColumnNotFoundError, InvalidFileTypeError
from simba.utils.read_write import get_fn_ext, read_video_info, bento_file_reader, read_video_info_csv, find_files_of_filetypes_in_directory
from simba.utils.warnings import ThirdPartyAnnotationsInvalidFileFormatWarning
from simba.utils.checks import (check_valid_lst,
                                check_valid_dataframe,
                                check_all_file_names_are_represented_in_video_log,
                                check_str,
                                check_valid_boolean,
                                check_file_exist_and_readable,
                                check_if_dir_exists,
                                check_int)




def is_new_boris_version(pd_df: pd.DataFrame):
    """
    Check the format of a boris annotation file.

    In the new version, additional column names are present, while
    others have slightly different name. Here, we check for the presence
    of a column name present only in the newer version.

    :return: True if newer version
    """
    return "Media file name" in list(pd_df.columns)

def read_boris_file(file_path: Union[str, os.PathLike],
                    fps: Optional[int] = None):

    MEDIA_FILE_NAME = "Media file name"
    BEHAVIOR_TYPE = 'Behavior type'
    OBSERVATION_ID = "Observation id"
    TIME = "Time"
    BEHAVIOR = "Behavior"
    STATUS = "Status"
    MEDIA_FILE_PATH = "Media file path"

    check_file_exist_and_readable(file_path=file_path)
    if fps is not None:
        check_int(name=f'{read_boris_file.__name__} fps', min_value=1, value=fps)
    boris_df = pd.read_csv(file_path)
    if not is_new_boris_version(boris_df):
        expected_headers = [TIME, MEDIA_FILE_PATH, BEHAVIOR, STATUS]
        if not OBSERVATION_ID in boris_df.columns:
            raise InvalidFileTypeError(msg=f'{file_path} is not a valid BORIS file', source=read_boris_file.__name__)
        start_idx = boris_df[boris_df[OBSERVATION_ID] == TIME].index.values
        if len(start_idx) != 1:
            raise InvalidFileTypeError(msg=f'{file_path} is not a valid BORIS file', source=read_boris_file.__name__)
        df = pd.read_csv(file_path, skiprows=range(0, int(start_idx + 1)))
    else:
        MEDIA_FILE_PATH, STATUS = MEDIA_FILE_NAME, BEHAVIOR_TYPE
        expected_headers = [TIME, MEDIA_FILE_PATH, BEHAVIOR, STATUS]
        df = pd.read_csv(file_path)
    check_valid_dataframe(df=df, source=f'{read_boris_file.__name__} {file_path}', required_fields=expected_headers)
    _, video_base_name, _ = get_fn_ext(df.loc[0, MEDIA_FILE_PATH])
    df = df[expected_headers]
    df.drop(MEDIA_FILE_PATH, axis=1, inplace=True)
    df.columns = ["TIME", "BEHAVIOR", "EVENT"]

    types = set([type(x) for x in np.unique(df['TIME'].values)])
    print(types)

    #numeric_check = list(df['TIME'].apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all()))


    df["TIME"] = df["TIME"].astype(float)
    df = df.sort_values(by="TIME")
    print(df)




    #
    #
    #
    #
    #
    #
    #

    #
    #
    #



def read_boris_annotation_files(data_paths: Union[List[str], str, os.PathLike],
                                video_info_df: Union[str, os.PathLike, pd.DataFrame],
                                error_setting: Literal[Union[None, Methods.ERROR.value, Methods.WARNING.value]] = None,
                                log_setting: Optional[bool] = False) -> Dict[str, pd.DataFrame]:


    if error_setting is not None:
        check_str(name=f'{read_boris_annotation_files.__name__} error_setting', value=error_setting, options=(Methods.ERROR.value, Methods.WARNING.value))
    check_valid_boolean(value=log_setting, source=f'{read_boris_annotation_files.__name__} log_setting')
    raise_error = False
    if error_setting == Methods.ERROR.value:
        raise_error = True
    if isinstance(video_info_df, str):
        check_file_exist_and_readable(file_path=video_info_df)
        video_info_df = read_video_info_csv(file_path=video_info_df)
    if isinstance(data_paths, list):
        check_valid_lst(data=data_paths, source=f'{read_boris_annotation_files.__name__} data_paths', min_len=1, valid_dtypes=(str,))
    elif isinstance(data_paths, str):
        check_if_dir_exists(in_dir=data_paths, source=f'{read_boris_annotation_files.__name__} data_paths')
        data_paths = find_files_of_filetypes_in_directory(directory=data_paths, extensions=['.csv'], raise_error=True)
    check_all_file_names_are_represented_in_video_log(video_info_df=video_info_df, data_paths=data_paths)
    check_valid_dataframe(df=video_info_df, source=read_boris_annotation_files.__name__)
    dfs = {}
    for file_cnt, file_path in enumerate(data_paths):
        _, video_name, _ = get_fn_ext(file_path)
        _, _, fps = read_video_info(vid_info_df=video_info_df, video_name=video_name)
        read_boris_file(file_path=file_path, fps=fps)






    #     boris_df = pd.read_csv(file_path)
    #     try:
    #         if not is_new_boris_version(boris_df):
    #             expected_headers = [TIME, MEDIA_FILE_PATH, BEHAVIOR, STATUS]
    #             start_idx = boris_df[boris_df[OBSERVATION_ID] == TIME].index.values
    #             df = pd.read_csv(file_path, skiprows=range(0, int(start_idx + 1)))[
    #                 expected_headers
    #             ]
    #         else:
    #             # Adjust column names to newer BORIS annotation format
    #             MEDIA_FILE_PATH = "Media file name"
    #             STATUS = "Behavior type"
    #             expected_headers = [TIME, MEDIA_FILE_PATH, BEHAVIOR, STATUS]
    #             df = pd.read_csv(file_path)[expected_headers]
    #         _, video_base_name, _ = get_fn_ext(df.loc[0, MEDIA_FILE_PATH])
    #         df.drop(MEDIA_FILE_PATH, axis=1, inplace=True)
    #         df.columns = ["TIME", "BEHAVIOR", "EVENT"]
    #         df["TIME"] = df["TIME"].astype(float)
    #         dfs[video_base_name] = df.sort_values(by="TIME")
    #     except Exception as e:
    #         print(e)
    #         if error_setting == Methods.WARNING.value:
    #             ThirdPartyAnnotationsInvalidFileFormatWarning(
    #                 annotation_app="BORIS", file_path=file_path, log_status=log_setting
    #             )
    #         elif error_setting == Methods.ERROR.value:
    #             raise InvalidFileTypeError(
    #                 msg=f"{file_path} is not a valid BORIS file. See the docs for expected file format."
    #             )
    #         else:
    #             pass
    # for video_name, video_df in dfs.items():
    #     _, _, fps = read_video_info(vid_info_df=video_info_df, video_name=video_name)
    #     video_df["FRAME"] = (video_df["TIME"] * fps).astype(int)
    #     video_df.drop("TIME", axis=1, inplace=True)
    # return dfs


# video_info_df = read_video_info_csv(file_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/logs/video_info.csv')
#
df = read_boris_annotation_files(data_paths=[r"C:\troubleshooting\boris_test\project_folder\boris_files\c_oxt23_190816_132617_s_trimmcropped.csv"],
                                 error_setting='WARNING',
                                 log_setting=False,
                                 video_info_df=r"C:\troubleshooting\boris_test\project_folder\logs\video_info.csv")