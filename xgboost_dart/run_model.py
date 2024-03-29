# encoding:utf-8
# -*- coding: UTF-8 -*-
import re
import pandas as pd
import multiprocessing

from sklearn.model_selection import KFold
from open_competition.tabular.model_fitter import XGBFitter, XGBOpt
from datetime import datetime


def run_model(fitter, param):
    kfold = KFold(n_splits=5)
    _, _, acc_result, _ = fitter.train_k_fold(kfold, df_train, df_test, param)
    print("acc result is " + ",".join([str(acc) for acc in acc_result]))
    return acc_result


train_path = "../data/train_onehot.csv"
test_path = "../data/test_onehot.csv"
df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)


def find_best_param(change_param, value_range, best_param, best_acc):
    acc_result_dict = {}
    change_value = None

    for change_value in value_range:
        param = best_param.copy()
        param[change_param] = change_value
        model = XGBFitter()
        start = datetime.now()
        acc_result = run_model(model, param)
        end = datetime.now()
        print("change_param is " + change_param + ", change_value is " + str(change_value))
        print("time spend is " + str((end - start).microseconds))
        acc_result_dict[change_value] = sum(acc_result) / 5

    tmp_best_acc = min(acc_result_dict.values())
    if tmp_best_acc <= best_acc:
        best_param[change_param] = [value for value in acc_result_dict.keys()
                                    if acc_result_dict.get(value) == tmp_best_acc][0]
        best_acc = tmp_best_acc

        return change_value, best_acc
    else:
        return best_param[change_param], best_acc


def save_process(change_param, best_acc, change_value):
    with open("find_process.csv", mode="a") as file:
        acc = str(best_acc)
        value = str(change_value)
        file.write(f"The best value for {change_param} is {value}, the acc is {acc}.\n")


cpu_count = multiprocessing.cpu_count()
best_acc = 1

# need change
best_param = XGBOpt.get_common_paarams().copy()
best_param["num_round"] = 1000
best_param["booster"] = "dart"
best_param["nthread"] = cpu_count

# need change
change_param = "eta"
value_range = [0.3]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "max_depth"
value_range = [4, 5, 6, 7, 8]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "rate_drop"
value_range = [0, 0.5, 1]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "subsample"
value_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "gamma"
value_range = [0, 1, 2, 3, 4, 5]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "colsample_bytree"
value_range = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "sample_type"
value_range = ["uniform", "weighted"]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "min_child_weight"
value_range = [0, 5, 10, 15]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)
