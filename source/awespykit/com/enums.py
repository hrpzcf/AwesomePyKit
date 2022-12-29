# coding: utf-8

from enum import Enum, IntEnum


class Accept(Enum):
    """
    供一些需要接收区分'文件'或'目录'参数的函数、方法使用
    """

    File = "file"  # 接受文件
    Dir = "dir"  # 接受目录
    Both = "both"  # 全都接受


class AppStyle(IntEnum):
    Fusion = 0  # Fusion 风格
    WindowsVista = 1  # 原生风格
    Windows = 2  # 经典风格


class Linkage(IntEnum):
    """枚举：输出窗口的哪一侧吸附在主窗口上"""

    NoLink = 0  # 子窗口没有吸附在主窗口上
    Top = 1  # 子窗口顶部吸附在主窗口底部
    Left = 2  # 子窗口左侧吸附在主窗口右侧
    Right = 3  # 子窗口右侧吸附在主窗口左侧


class QMode(IntEnum):
    """包管理器的查询面板查询模式设置"""

    NotSPCF = 0  # 未指定查询方式
    Pkg2Imp = 1  # 以包名查导入名
    Imp2Pkg = 2  # 以导入名查包名


class DataType(IntEnum):
    """ThemeData 类的 dtype 参数类型"""

    StyleSheet = 0x00000001  # 此 ThemeData 携带的是 QSS 样式表文本
    QtPreStyle = 0x00000002  # 此 ThemeData 携带的是 Qt 内置风格
    QDarkStyle = 0x00000004  # 此 ThemeData 携带的是 QDarkStyle 包样式表
    QtMaterial = 0x00000008  # 此 ThemeData 携带的是 qt_material 包样式信息
    ResetStyle = 0x00000010  # 重置界面风格为系统原生风格 AppStyle.WindowsVista
    ResetSheet = 0x00000020  # 应用基础样式表 base-stylesheet.qss
    # 以下两项影响此类主题：不设置 PlaceHolderText 颜色且没有写其样式
    DarkTheme = 0x00000040  # 表示此主题是深色类型的主题
    LightTheme = 0x00000080  # 表示此主题是浅色类型的主题


class RoleData(IntEnum):
    """供控件的 setData 方法和 utils.widgets.ItemDelegate 类使用"""

    Success = 0
    Failed = 1
    Warning = 3
    Unknown = 4
