"""
import os

# 获取当前脚本的完整路径
current_script_path = os.path.abspath(__file__)
print(current_script_path)

"""

import os
import ui
import clipboard

def copy_path(sender):
    # 获取输入框中的文本
    path = sender.superview['textfield'].text
    # 复制到剪贴板
    clipboard.set(path)
    # 显示提示信息
    sender.superview['label'].text = '路径已复制!'

def show_path_in_alert():
    # 获取当前脚本的完整路径
    current_script_path = os.path.abspath(__file__)

    # 创建一个视图,尺寸为全屏
    view = ui.View()
    view.name = '脚本路径'
    view.background_color = 'white'
    view.frame = (0, 0, ui.get_screen_size()[0], ui.get_screen_size()[1])

    # 创建并添加一个文本输入框,尺寸适合屏幕宽度
    textfield = ui.TextField(frame=(10, 10, view.width-20, 40), flex='W')
    textfield.name = 'textfield'
    textfield.text = current_script_path
    textfield.alignment = ui.ALIGN_LEFT
    textfield.content_mode = ui.CONTENT_LEFT  # 设置内容对齐方式
    view.add_subview(textfield)

    # 创建并添加一个标签,用于显示提示信息
    label = ui.Label(frame=(10, 60, view.width-20, 40), flex='W')
    label.name = 'label'
    label.text = ''
    view.add_subview(label)

    # 创建并添加一个复制按钮
    button = ui.Button(frame=(10, 110, view.width-20, 40), flex='W')
    button.title = '复制路径'
    button.action = copy_path
    view.add_subview(button)

    # 显示视图
    view.present('fullscreen')

# 调用函数显示弹窗
show_path_in_alert()

"""

import os
import clipboard

# 获取当前脚本的完整路径
current_script_path = os.path.abspath(__file__)

# 将路径复制到剪贴板
clipboard.set(current_script_path)

print("路径已复制到剪贴板:", current_script_path)
"""