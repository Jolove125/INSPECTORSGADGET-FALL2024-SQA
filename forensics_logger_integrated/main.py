import lint_engine
import constants
import time
import datetime
import os
import pandas as pd
import py_parser
import numpy as np
import myLogger

logObj = myLogger.giveMeLoggingObject()


def giveTimeStamp():
    tsObj = time.time()
    strToret = datetime.datetime.fromtimestamp(tsObj).strftime(constants.TIME_FORMAT)
    logObj.info(f"Timestamp generated: {strToret}")
    return strToret


def getCSVData(dic_, dir_repo):
    logObj.info(f"Generating CSV data for directory: {dir_repo}")
    temp_list = []
    for TEST_ML_SCRIPT in dic_:
        logObj.info(f"Analyzing script: {TEST_ML_SCRIPT}")
        data_load_counta = lint_engine.getDataLoadCount(TEST_ML_SCRIPT)
        data_load_countb = lint_engine.getDataLoadCountb(TEST_ML_SCRIPT)
        data_load_countc = lint_engine.getDataLoadCountc(TEST_ML_SCRIPT)
        model_load_counta = lint_engine.getModelLoadCounta(TEST_ML_SCRIPT)
        model_load_countb = lint_engine.getModelLoadCountb(TEST_ML_SCRIPT)
        model_load_countc = lint_engine.getModelLoadCountc(TEST_ML_SCRIPT)
        model_load_countd = lint_engine.getModelLoadCountd(TEST_ML_SCRIPT)
        data_download_counta = lint_engine.getDataDownLoadCount(TEST_ML_SCRIPT)
        data_download_countb = lint_engine.getDataDownLoadCountb(TEST_ML_SCRIPT)
        model_label_counta = lint_engine.getModelLabelCount(TEST_ML_SCRIPT)
        model_output_counta = lint_engine.getModelOutputCount(TEST_ML_SCRIPT)
        model_output_countb = lint_engine.getModelOutputCountb(TEST_ML_SCRIPT)
        data_pipeline_counta = lint_engine.getDataPipelineCount(TEST_ML_SCRIPT)
        data_pipeline_countb = lint_engine.getDataPipelineCountb(TEST_ML_SCRIPT)
        data_pipeline_countc = lint_engine.getDataPipelineCountc(TEST_ML_SCRIPT)
        environment_counta = lint_engine.getEnvironmentCount(TEST_ML_SCRIPT)
        state_observe_count = lint_engine.getStateObserveCount(TEST_ML_SCRIPT)

        data_load_count = data_load_counta + data_load_countb + data_load_countc
        model_load_count = model_load_counta + model_load_countb + model_load_countc + model_load_countd
        data_download_count = data_download_counta + data_download_countb
        model_label_count = model_label_counta
        model_output_count = model_output_counta + model_output_countb
        data_pipeline_count = data_pipeline_counta + data_pipeline_countb + data_pipeline_countc
        environment_count = environment_counta
        total_event_count = data_load_count + model_load_count + data_download_count + model_label_count + model_output_count + data_pipeline_count + environment_count + state_observe_count
        logObj.info(f"Total event count for {TEST_ML_SCRIPT}: {total_event_count}")

        the_tup = (dir_repo, TEST_ML_SCRIPT, data_load_count, model_load_count, data_download_count, model_label_count,
                   model_output_count, data_pipeline_count, environment_count, state_observe_count, total_event_count)
        temp_list.append(the_tup)
    logObj.info(f"CSV data generated for directory: {dir_repo}")
    return temp_list


def getAllPythonFilesinRepo(path2dir):
    logObj.info(f"Getting all Python files in repository: {path2dir}")
    valid_list = []
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_)
            if os.path.exists(full_path_file):
                if file_.endswith(constants.PY_FILE_EXTENSION) and py_parser.checkIfParsablePython(full_path_file):
                    valid_list.append(full_path_file)
    valid_list = np.unique(valid_list)
    logObj.info(f"Found {len(valid_list)} Python files.")
    return valid_list


def runFameML(inp_dir, csv_fil):
    logObj.info(f"Running FameML on directory: {inp_dir}")
    output_event_dict = {}
    df_list = []
    list_subfolders_with_paths = [f.path for f in os.scandir(inp_dir) if f.is_dir()]
    for subfolder in list_subfolders_with_paths:
        logObj.info(f"Processing subfolder: {subfolder}")
        events_with_dic = getAllPythonFilesinRepo(subfolder)
        if subfolder not in output_event_dict:
            output_event_dict[subfolder] = events_with_dic
        temp_list = getCSVData(events_with_dic, subfolder)
        df_list += temp_list
        logObj.info(f"Processed subfolder: {subfolder}")
    try:
        full_df = pd.DataFrame(df_list)
        full_df.to_csv(csv_fil, header=constants.CSV_HEADER, index=False, encoding=constants.UTF_ENCODING)
        logObj.info(f"Output saved to CSV file: {csv_fil}")
    except OSError:
        logObj.error("Error saving CSV file. Check directory")
    return output_event_dict


if __name__ == '__main__':

    command_line_flag = True
    t1 = time.time()
    print('Started at:', giveTimeStamp())
    print('*' * 100)

    if command_line_flag:
        dir_path = input(constants.ASK_INPUT_FROM_USER).strip()
        if os.path.exists(dir_path):
            repo_dir = dir_path
            output_file = dir_path.split('/')[-2]
            output_csv = f'/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/VulnStrategyMining/ForensicsinML/Output/V5_{output_file}.csv'
            full_dict = runFameML(repo_dir, output_csv)
    else:
        repo_dir = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/'
        output_csv = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/VulnStrategyMining/ForensicsinML/Output/V5_OUTPUT_GITHUB.csv'
        full_dict = runFameML(repo_dir, output_csv)

    print('*' * 100)
    print('Ended at:', giveTimeStamp())
    print('*' * 100)
    t2 = time.time()
    time_diff = round((t2 - t1) / 60, 5)
    print(f'Duration: {time_diff} minutes')
    print('*' * 100)