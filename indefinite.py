import ui
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, diff, integrate, sympify, limit, oo, Abs, Function, dsolve, Eq
import numpy as np
import math
import clipboard  # 导入剪贴板模块,用于复制文本


# 动作函数:粘贴文本到输入框
def paste_action(sender, func_input):
    text = clipboard.get()  # 从剪贴板获取文本
    func_input.text += text  # 将文本添加到输入框
# 动作函数:复制结果标签的文本
def copy_action(sender, result_label):
    if result_label.text:
        clipboard.set(result_label.text)  # 将结果标签的文本复制到剪贴板
    else:
        print("没有可复制的内容")
# 动作函数:清空函数输入框的内容
def clear_action(sender, func_input):
    func_input.text = ''
    
x = sp.symbols('x')

def calculate_derivative(expression):
    """计算给定表达式的导数."""
    parsed_expr = parse_expr(expression)
    derivative = sp.diff(parsed_expr, x)
    return derivative

def calculate_definite_integral(expression, lower_limit, upper_limit):
    """计算定积分."""
    parsed_expr = parse_expr(expression)
    lower_limit = sp.sympify(lower_limit) if lower_limit in ['oo', '-oo'] else float(lower_limit)
    upper_limit = sp.sympify(upper_limit) if upper_limit in ['oo', '-oo'] else float(upper_limit)
    return sp.integrate(parsed_expr, (x, lower_limit, upper_limit))

def calculate_indefinite_integral(expression):
    """计算不定积分."""
    C = sp.symbols('C')
    parsed_expr = parse_expr(expression)
    return sp.integrate(parsed_expr, x) + C

# 计算极限
def calculate_limit(expression, point, direction='+'):
    parsed_expr = parse_expr(expression)

    if point.endswith('-'):
        point_value = sp.sympify(point[:-1])  # 去除方向符号并解析为数值
        direction = '-'
    elif point.endswith('+'):
        point_value = sp.sympify(point[:-1])  # 去除方向符号并解析为数值
    else:
        point_value = sp.sympify(point)
    
    return limit(parsed_expr, x, point_value, dir=direction)

def calculate_and_display_result(calculation_func):
    try:
        result = calculation_func()
        result_label.text = str(result)
    except Exception as e:
        result_label.text = f"错误: {e}"

def button_action(sender):
    expression = func_input.text
    upper_limit = upper_limit_input.text
    lower_limit = lower_limit_input.text
    title = sender.title
    # 单独处理复制操作
    if title in ['x', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')', 'log', 'ln', 'sin', 'cos', 'tan', 'cot', 'sec', 'csc']:
        func_input.text += title
    elif  title == 'Copy':
        copy_action(sender, result_label)
    elif title == 'Clear':  # 清除
            func_input.text = ''
    elif title == 'Paste':
        paste_action(sender, func_input)
    elif title == 'Delete':
        func_input.text = func_input.text[:-1]
    else:
        # 进行实际的计算
        
      try:
        if  title == '导数':
            result = calculate_derivative(expression)
        elif title == '不定积分':
            result = calculate_indefinite_integral(expression)
        elif title == '定积分':
            result = calculate_definite_integral(expression, lower_limit, upper_limit)
        elif title == '极限':
            result = calculate_limit(expression, upper_limit)
        elif title == '微分方程':
            # 调用求解微分方程的函数
            result = calculate_differential_eq(func_input.text)
            
        
        else:
            result_label.text = '未知操作'
            return

        result_label.text = str(result)

      except Exception as e:
        print(f"错误详情: {e}")  # 打印错误详情
        result_label.text = "计算错误,请检查输入"
        
# 创建按钮并添加到视图的代码保持不变
        
# 创建 UI 视图
view = ui.View()
view.name = '微积分计算器'
view.background_color = 'white'

# 获取屏幕尺寸
screen_width, screen_height = ui.get_screen_size()

# 创建输入框和标签
func_input = ui.TextField(frame=(10, 10, screen_width - 20, 40), border_style='rounded', placeholder='输入函数表达式')
upper_limit_input = ui.TextField(frame=(10, 60, screen_width - 20, 40), border_style='rounded', placeholder='输入趋近点或定积分上限')
lower_limit_input = ui.TextField(frame=(10, 110, screen_width - 20, 40), border_style='rounded', placeholder='输入定积分下限')
result_label = ui.Label(frame=(10, 160, screen_width - 20, 40), border_color='black', border_width=1, alignment=ui.ALIGN_CENTER)

view.add_subview(func_input)
view.add_subview(upper_limit_input)
view.add_subview(lower_limit_input)
view.add_subview(result_label)


# 定义按钮的标题
button_titles = ['Clear', 'Delete', '导数', '不定积分', '定积分', '极限','x', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '+', '-', '*', '/', 'log', 'ln', 'sin', 'cos', 'tan', 'cot', 'sec', 'csc','Copy','Paste']

#button_titles.append()


layout_x, layout_y = 10, 210  # 开始放置按钮的初始位置
button_width = 55  # 增大按钮尺寸
button_height = 55
button_spacing = 5

for i, title in enumerate(button_titles):
    button = ui.Button(title=title)
    button.frame = (layout_x, layout_y, button_width, button_height)
    button.action = button_action
    # 设置按钮样式
    button.border_width = 1
    button.border_color = '#19d13b'
    button.corner_radius = 5
    button.background_color = '#ee0000'  # 蓝色背景
    button.tint_color = 'white'  # 文本颜色为白色
    view.add_subview(button)
    layout_x += button_width + button_spacing
    if layout_x > screen_width - button_width:
        layout_x = 10
        layout_y += button_height + button_spacing
# 显示视图
view.present('fullscreen')





