# coding: utf-8

# 将 QtDesigner 生成的 .ui 文件批量转换为 .py 文件

import os
import sys

compile_cmd = "pyuic5 -o {} {}"
ui_dir_path = "source/awespykit/ui"


def compile_ui(any_path):
    current_dir = os.getcwd()
    try:
        os.chdir(any_path)
        ui_list = [f for f in os.listdir() if f.endswith(".ui")]
    except Exception:
        print(f"读取 <{any_path}> 目录失败，程序退出...")
        sys.exit(-1)

    ui_name_max = max(len(ui) for ui in ui_list)

    for ui_name in ui_list:
        src_name = os.path.splitext(ui_name)[0] + ".py"
        print(f"转换目标：<{ui_name:<{ui_name_max}}>")
        try:
            os.system(compile_cmd.format(src_name, ui_name))
            print(f"转换完成...\n")
        except Exception:
            print(f"文件 <{ui_name}> 转换失败，请检查是否已安装 PyQt5...\n")
            break
    print("转换结束...")
    os.chdir(current_dir)


if __name__ == "__main__":
    compile_ui(ui_dir_path)
