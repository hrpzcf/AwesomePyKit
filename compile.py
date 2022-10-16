# coding: utf-8

__doc__ = "将 QtDesigner 生成的 ui 文件批量编译为 py 文件。"

import os
import sys

ui_dir_path = "./source/ui"
compile_cmd = "pyuic5 {} -o {}"


def compile_ui(any_path):
    """将 any_path 目录中所有 ui 文件编译为 py 文件。"""
    current_dir = os.getcwd()
    try:
        # 切换工作目录的原因是防止生成的 py 文件注释中出现 ui 文件的相对或完整路径
        os.chdir(any_path)
        ui_list = [f for f in os.listdir() if f.endswith(".ui")]
    except Exception:
        print(f"读取 <{any_path}> 目录失败，程序退出...")
        sys.exit(-1)

    ui_name_max = max(len(ui) for ui in ui_list)

    for ui_name in ui_list:
        src_name = os.path.splitext(ui_name)[0] + ".py"
        print(f"编译目标：<{ui_name:<{ui_name_max}}>")
        try:
            os.system(compile_cmd.format(ui_name, src_name))
            print(f"编译完成...\n")
        except Exception:
            print(f"文件 <{ui_name}> 编译失败，请检查是否已安装 PyQt5...\n")
            break
    print("编译结束...")
    os.chdir(current_dir)


if __name__ == "__main__":
    compile_ui(ui_dir_path)
