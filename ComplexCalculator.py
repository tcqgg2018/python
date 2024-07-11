#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#__author__ = 'TAN' 2024-01-13 21:16

import ui,io,clipboard,cmath, math,os
import matplotlib.pyplot as plt


class ComplexCalculator(ui.View):
    # 初始化方法
    def __init__(self):
    	   #绘图用
        self.last_operation = None
        
        self.background_color = 'white'
        self.name = '复数的计算器'
        #获取屏幕尺寸
        self.screen_width, self.screen_height = ui.get_screen_size()
        # 当前活动的输入框
        self.active_field = None  
        self.setup_ui()
        self.present('sheet')

    # 设置用户界面
    def setup_ui(self):
        # 创建输入框和按钮
        self.create_input_fields()
        self.create_buttons()

    # 创建输入框及其对应的输出框
    def create_input_fields(self):
        # 第一个复数的输入框
        self.complex1_field = ui.TextField(frame=(10, 10, self.screen_width / 2 - 15, 32), border_style='rounded', placeholder='输入复数1')
        self.complex1_field.delegate = self
        self.add_subview(self.complex1_field)

        # 第一个复数的转换后输出框
        self.complex1_converted = ui.TextField(frame=(10, 50, self.screen_width / 2 - 15, 32), border_style='rounded', editable=False, placeholder='上面复数转换后')
        self.add_subview(self.complex1_converted)

        # 第二个复数的输入框
        self.complex2_field = ui.TextField(frame=(self.screen_width / 2 + 5, 10, self.screen_width / 2 - 15, 32), border_style='rounded', placeholder='输入复数2')
        self.complex2_field.delegate = self
        self.add_subview(self.complex2_field)

        # 第二个复数的转换后输出框
        self.complex2_converted = ui.TextField(frame=(self.screen_width / 2 + 5, 50, self.screen_width / 2 - 15, 32), border_style='rounded', editable=False, placeholder='上面转换后')
        self.add_subview(self.complex2_converted)

        # 结果输出框
        self.result_field = ui.TextField(frame=(10, 90, self.screen_width - 20, 32), border_style='rounded', editable=False, placeholder='结果')
        self.add_subview(self.result_field)

    # 当输入框开始编辑时,设置为当前活动的输入框
    def textfield_did_begin_editing(self, textfield):
        self.active_field = textfield

    # 创建按钮
    def create_buttons(self):
        # 按钮的标题
        button_titles = ['加', '减', '乘', '除', '清空', '删除', '复制', '粘贴', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','∠','j' ,'(', ')', '+', '-', '*', '/'] 
        
        # 按钮布局的起始位置
        layout_x, layout_y = 10, 130
        button_width, button_height, button_spacing = 60, 55, 1
        
        # 循环创建并设置按钮
        for title in button_titles:
            button = ui.Button(title=title)
            self.set_button_style(button, title)
            button.action = self.button_action
            button.frame = (layout_x, layout_y, button_width, button_height)
            self.add_subview(button)

            # 更新下一个按钮的位置
            layout_x += button_width + button_spacing
            if layout_x > self.screen_width - button_width:
                layout_x = 10
                layout_y += button_height + button_spacing

    # 设置按钮样式
    def set_button_style(self, button, title):
        # 按钮颜色设置
        colors = {'∠':'#ff08d2', 'j': '#ff1f5c', '加': '#2c17ff', '减': '#2c17ff', '乘': '#2c17ff', '除': '#2c17ff', '清空': '#ff0000', '删除': '#ff1f5c', '复制': '#00ff00', '粘贴': '#ff7c9f', '计算': '#ea17ff'}
        default_color = '#2b5555'
        button.background_color = colors.get(title, default_color)
        button.tint_color = 'white' if title in colors else 'white'
        button.font = ('<system>', 20)
        button.border_width = 3
        button.border_color = '#06bc59'
        button.corner_radius = 10


    # 按钮点击事件处理
    def button_action(self, sender):
        title = sender.title
        # 根据按钮标题判断操作
        if title in [str(i) for i in range(10)]+['∠', '+', '-', '*', '/', '(', ')', 'j'] :
            # 如果当前有激活的输入框,添加字符到输入框
            if self.active_field:
                self.active_field.text += title
        elif title in ['加', '减', '乘', '除']:
            # 执行复数运算
            self.perform_operation(title)
        elif title == '删除':
            # 删除输入框中的最后一个字符
            if self.active_field:
                self.active_field.text = self.active_field.text[:-1]
        elif title == '清空':
            # 清空当前激活输入框的内容
            if self.active_field:
                self.active_field.text = ''
        elif title == '复制':
            # 复制结果框中的内容到剪贴板
            if self.result_field.text:
                clipboard.set(self.result_field.text)
        elif title == '粘贴':
            # 将剪贴板内容粘贴到当前激活输入框
            if self.active_field:
                self.active_field.text += clipboard.get()
        elif title == '制图':
    # 重新计算并绘制复数图像
            self.perform_operation(self.last_operation)
    # 执行复数运算
    def perform_operation(self, op):
        self.last_operation = op
        # 解析输入框中的复数
        complex1 = self.parse_complex(self.complex1_field.text, self.complex1_converted)
        complex2 = self.parse_complex(self.complex2_field.text, self.complex2_converted)

        # 检查复数是否有效
        if complex1 is None or complex2 is None:
            self.result_field.text = "无法进行运算:无效的输入"
            return

        try:
            # 根据运算符执行对应的复数运算
            if op == '加':
                result = complex1 + complex2
            elif op == '减':
                result = complex1 - complex2
            elif op == '乘':
                result = complex1 * complex2
            elif op == '除':
                result = complex1 / complex2
            else:
                result = "未知操作"
                self.result_field.text = str(result)
                return


        # 格式化输出结果
            r, theta_rad = cmath.polar(result)
            theta_deg = math.degrees(theta_rad)
            algebraic_form = f"{result.real:.2f} + {result.imag:.2f}j"
            polar_form = f"{r:.2f}∠{theta_deg:.2f}°"
            self.plot_complex_numbers(complex1, complex2, result)
            # 显示两种形式的结果
            self.result_field.text = f"代数式: {algebraic_form}, 极坐标: {polar_form}"
        except Exception as e:
            self.result_field.text = f'错误: {e}'
    
        
    # 解析输入的复数字符串
    def parse_complex(self, expression, output_field):
        try:
        # 首先尝试直接解析代数形式
            complex_result = complex(eval(expression.replace('i', 'j')))
            # 将复数转换为极坐标形式
            r, theta_rad = cmath.polar(complex_result)
            theta_deg = math.degrees(theta_rad)
            # 显示转换后的极坐标形式
            # 使用 math.degrees 而不是 cmath.degrees
            output_field.text = f"{r:.2f}∠{theta_deg:.2f}"  # 转换为极坐标式
            return complex_result
        except SyntaxError as e:
        # 仅当遇到语法错误时尝试解析极坐标形式
            try:
                r, theta = map(float, expression.split('∠'))
                theta_rad = cmath.pi * theta / 180 # 将极坐标转换为代数形式
                #绘图用
                complex_result = cmath.rect(r, theta_rad)
                # 显示转换后的代数形式
                output_field.text = f"{complex_result.real:.2f} + {complex_result.imag:.2f}j"  # 转换为代数式
                return complex_result
            except Exception as e2:
                output_field.text = "解析错误: " + str(e2)
                # 如果极坐标解析也失败,显示错误信息
                return None
        except Exception as e:
        # 处理其他类型的错误
            output_field.text = "解析错误: " + str(e)
            return None
            
            
            
            
    
        
    def plot_complex_numbers(self, complex1, complex2, result):
    #在复数坐标系中绘制复数,并在幅值尾端显示代数式
        if not (complex1 and complex2 and result):
            print("无法绘制,复数值无效")
            return

        fig, ax = plt.subplots()
        colors = ['green', 'blue', 'red']
        numbers = [complex1, complex2, result]
        labels = ['c1: ', 'c2:', 'result: ']

        max_magnitude = max(cmath.polar(c)[0] for c in numbers) * 1.1

        for c, color, label in zip(numbers, colors, labels):
            ax.plot([0, c.real], [0, c.imag], color=color, marker='o')
            ax.text(c.real, c.imag, f'{label}{c.real:.2f} + {c.imag:.2f}i', fontsize=12, ha='right')

        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axvline(x=0, color='black', linewidth=0.5)
        ax.set_xlim(-max_magnitude, max_magnitude)
        ax.set_ylim(-max_magnitude, max_magnitude)
        ax.set_xlabel('Real')
        ax.set_ylabel('Imaginary')
        ax.set_title('Complex Number Plot')
        ax.grid(True)
        plt.show()
       
         

# 创建并展示计算器界面
ComplexCalculator()