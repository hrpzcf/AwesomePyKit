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


class WorkDir(IntEnum):
    """云函数打包工具的‘工作目录’对应的枚举"""

    TmpDir = 0  # 使用临时目录
    Project = 1  # 使用项目目录
    Custom = 2  # 使用自定义目录


class DWMWINDOWATTRIBUTE(IntEnum):
    DWMWA_NCRENDERING_ENABLED = 0
    DWMWA_NCRENDERING_POLICY = 1
    DWMWA_TRANSITIONS_FORCEDISABLED = 2
    DWMWA_ALLOW_NCPAINT = 3
    DWMWA_CAPTION_BUTTON_BOUNDS = 4
    DWMWA_NONCLIENT_RTL_LAYOUT = 5
    DWMWA_FORCE_ICONIC_REPRESENTATION = 6
    DWMWA_FLIP3D_POLICY = 7
    DWMWA_EXTENDED_FRAME_BOUNDS = 8
    DWMWA_HAS_ICONIC_BITMAP = 9
    DWMWA_DISALLOW_PEEK = 10
    DWMWA_EXCLUDED_FROM_PEEK = 11
    DWMWA_CLOAK = 12
    DWMWA_CLOAKED = 13
    DWMWA_FREEZE_REPRESENTATION = 14
    DWMWA_PASSIVE_UPDATE_MODE = 15
    DWMWA_USE_HOSTBACKDROPBRUSH = 16
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_BORDER_COLOR = 31
    DWMWA_CAPTION_COLOR = 32
    DWMWA_TEXT_COLOR = 33
    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS = 34
    DWMWA_SYSTEMBACKDROP_TYPE = 35
    DWMWA_LAST = 36
