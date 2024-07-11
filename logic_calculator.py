#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#__author__ = 'TAN' 2024-01-07 22:32
# 优化界面 2024-01-08 17:12
#增加时钟⏰ 2024-01-10 19:25
#增加文件保存记录 2024-01-10 20:29

from sympy import symbols, simplify_logic
from sympy.parsing.sympy_parser import parse_expr
import ui,datetime,threading,os
import clipboard  # 剪贴板模块


# 粘贴文本到输入框
def paste_action(sender, input_field):
    text = clipboard.get()  # 从剪贴板获取文本
    input_field.text += text  # 将文本添加到输入框

def copy_action(sender, output_field):
    if output_field.text:
        clipboard.set(output_field.text)  # 将输出框的文本复制到剪贴板
    else:
        print("没有可复制的内容")

def simplify_logic_expression(expression):
     # 使用大写字母 A-Z 作为逻辑变量
    symbols_dict = {chr(i): symbols(chr(i)) for i in range(65, 91)}  # A-Z
    expr_symbols = {symbol: symbols_dict[symbol] for symbol in set(expression) if symbol.isalpha()}

    # 将字符串表达式转换为 SymPy 表达式
    parsed_expr = parse_expr(expression, local_dict=expr_symbols)

    # 简化逻辑表达式
    simplified_expr = simplify_logic(parsed_expr)
    return simplified_expr

#验证函数
def check_equivalence(expr1, expr2):
    try:
        # 使用大写字母 A-Z 作为逻辑变量
        symbols_dict = {chr(i): symbols(chr(i)) for i in range(65, 91)}  # A-Z
        expr_symbols = {symbol: symbols_dict[symbol] for symbol in set(expr1 + expr2) if symbol.isalpha()}

        # 将字符串表达式转换为 SymPy 表达式
        parsed_expr1 = parse_expr(expr1, local_dict=expr_symbols)
        parsed_expr2 = parse_expr(expr2, local_dict=expr_symbols)

        # 检查两个表达式是否等价
        return simplify_logic(parsed_expr1) == simplify_logic(parsed_expr2)
    except Exception as e:
        return f"错误: {e}"

# 您可以在 UI 中添加一个新的按钮来调用这个函数,或者修改现有的逻辑来处理两个表达式的比较。
#打印错误

def calculate_and_display_result(calculation_func):
    try:
        result = calculation_func()
        result_label.text = str(result)
    except Exception as e:
        result_label.text = f"错误: {e}"
        
 #Time
def update_time(label):
    while True:
        # 获取当前时间
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        # 更新标签
        label.text = current_time
        # 暂停一秒
        threading.Event().wait(1)

def button_tapped(sender):
    #global input_field
    # 根据按钮来执行的操作
    title = sender.title
  
    
    if title in ['&', '|', '~', '^', 'XNOR','(',')', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:  # 操作符和变量
        input_field.text += title
        
        
        
    elif title == 'Calculate':
        try:
            result = simplify_logic_expression(input_field.text)
            output_field.text = str(result)  # 显示结果在 输出框
            save_calculation(input_field.text, str(result))  # 保存计算
            # 电路图绘制程序
           # os.startfile('logic_circuit_drawer.py', 'input_field.text')
        except Exception as e:
            
            output_field.text = f"错误: {e}"
    elif title == 'Clear':
        input_field.text = ''
    elif title == 'Delete':
        input_field.text = input_field.text[:-1]
        
    # 对于复制和粘贴按钮的操作
    elif title == 'Copy':
        copy_action(sender, output_field)  # 复制输出框的内容
    elif title == 'Paste':
        paste_action(sender, input_field)  # 粘贴到输入框
    elif title == '验证':
        expressions = input_field.text.split(';')  # 假设两个表达式由分号分隔
        if len(expressions) == 2:
            is_equivalent = check_equivalence(expressions[0], expressions[1])
            output_field.text = f"等价: {is_equivalent}"  # 显示结果
        else:
            output_field.text = "请输入两个用分号分隔的表达式"
    else:
        input_field.text += sender.title
        print(f"错误详情: {e}")  # 打印错误详情
        
# 获取屏幕尺寸
screen_width, screen_height = ui.get_screen_size()

# 创建视图
view = ui.View()
view.name = 'Logic Calculator'
view.background_color = '#e8ecff'
view.frame = (0, 0, screen_width, screen_height) #全屏

# 创建输入框
input_field = ui.TextField(frame=(10, 10, screen_width - 120, 40), border_style='rounded', placeholder='请输入表达式,如果要验证,输入两个表达式以分号(;)隔开') #输入框样式
view.add_subview(input_field) #显示

# 创建输出框
output_field = ui.TextField(frame=(10, 60, screen_width - 20, 40), border_style='rounded', editable=False)  # 设置为不可编辑
view.add_subview(output_field)

# 显示时间
time_label = ui.Label(frame=(screen_width-105, 0, 200, 40))
time_label.font = ('<system>', 24)
view.add_subview(time_label)
# 启动一个线程来更新时间
threading.Thread(target=update_time, args=(time_label,), daemon=True).start()

def save_calculation(input_text, output_text):
    # 设置保存文件的路径
    filename = os.path.join(os.path.expanduser('~'), 'Documents', '逻辑代数计算保存记录.txt')
    
    # 获取当前日期和时间
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # 构建要保存的文本
    record = f"{timestamp}\nInput: {input_text}\nOutput: {output_text}\n\n"

    # 写入文件
    with open(filename, 'a') as file:
        file.write(record)

# 添加操作符按钮
buttons = ['Clear',  'Paste','Copy','&', '|', '~', '(',')','Delete', 'Calculate','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','验证']
x, y = 10, 110 #按钮的位置
button_width = 70  # 按钮尺寸
button_height = 70
button_spacing = 5 #按钮间隙

#将buttons里面的元素遍历到每个按钮上
for button_title in buttons:
    
    button = ui.Button(title=button_title)
    button.frame = (x, y, button_width, button_height)
    #当按钮被点击时
    button.action = button_tapped 

    # 根据按钮标题设置颜色
    if button_title == 'Clear':
        button.background_color = '#ff0000'  # 红色背景
        button.tint_color = 'white'  # 白色文本
    elif button_title == 'Delete':
        button.background_color = '#ff1f5c'  # 绿色背景
        button.tint_color = 'black'  # 黑色文本
    elif button_title == 'Paste':
        button.background_color = '#ff7c9f'  # 蓝色背景
        button.tint_color = 'white'  # 白
    elif button_title == 'Calculate':
        button.background_color = '#ea17ff'  # 橙色背景
        button.tint_color = 'white'  # 白色文本
    elif button_title == 'Copy':
        button.background_color = '#00ff00'  # 绿色背景
        button.tint_color = 'black'  # 黑色文本
    elif button_title == '&':
        button.background_color = '#FF8C00'  # 蓝色背景
        button.tint_color = 'white'  # 白
         # 设置按钮的字体和大小
        button.font = ('<system>', 30)  # 使用系统字体,大小为30
    elif button_title == '|':
        button.background_color = '#ff9900'  # 橙色背景
        button.tint_color = 'white'  # 白色文本
         # 设置按钮的字体和大小
        button.font = ('<system>', 30)  # 使用系统字体,大小为30
    elif button_title == '~':
        button.background_color = '#FF8C00'  # 绿色背景
        button.tint_color = '#ffffff'  # 黑色文本
        button.font = ('<system>', 30)  # 使用系统字体,大小为30
    elif button_title == '^':
        button.background_color = '#FF8C00'  # 背景颜色
        button.tint_color = 'white'  # 文本颜色
         # 设置按钮的字体和大小
        button.font = ('<system>', 30)  # 使用系统字体,大小为30
    elif button_title == 'XNOR':
        button.background_color = '#ff9900'  # 背景
        button.tint_color = 'white'  # 白色文本
         # 设置按钮的字体和大小
        button.font = ('<system>', 20)  # 使用系统字体,大小为30
    elif button_title == '(':
        button.background_color = '#ffca8b'  # 背景
        button.tint_color = 'white'  # 白
         # 设置按钮的字体和大小
        button.font = ('<system>', 30)  # 使用系统字体,大小为30
    elif button_title == ')':
        button.background_color = '#ffc784'  # 背景
        button.tint_color = 'white'  # 文本
         # 设置按钮的字体和大小
        button.font = ('<system>', 30)  # 使用系统字体,大小为30
    elif button_title == '验证':
        button.background_color = '#ff0909'  # 绿色背景
        button.tint_color = '#bfffd5'  # 黑色文本
        button.font = ('<system>', 25)  # 使用系统字体
    else:
        # 对于不在列表中的其他按钮,可以设置一个默认颜色
        button.background_color = '#4432ee'  # 背景颜色
        button.tint_color = '#ffffff'  # 文本颜色
         # 设置按钮的字体和大小
        button.font = ('<system>', 25)  # 使用系统字体
    # 设置按钮样式
    button.border_width = 3 #边框
    button.border_color = '#06bc59'
    button.corner_radius = 20 #边角圆润
    #调整按钮布局
    view.add_subview(button)
    x += button_width + button_spacing
    if x > screen_width - button_width:
        x = 10
        y += button_height + button_spacing

# 显示视图
view.present('fullscreen')



