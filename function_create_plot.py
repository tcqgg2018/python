import ui
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify
import io
import os
from datetime import datetime

# 全局变量用于存储图像缓存
image_buffer = None

def create_plot(image_view, expression, plot_type, data_input):
    plt.clf()
    x = symbols('x')

    try:
        if plot_type == 'function':
            x_vals = np.linspace(-10, 10, 400)
            func = lambdify(x, expression, modules=['numpy'])
            y_vals = func(x_vals)
            plt.plot(x_vals, y_vals, label=f'{expression} (line)')
            plt.axhline(0, color='black', linewidth=0.5)  # x 轴
            plt.axvline(0, color='black', linewidth=0.5)  # y 轴
            plt.grid(True)

        elif plot_type == 'data':
            data = [float(num) for num in data_input.split(',')]
            plt.bar(range(len(data)), data)

        # 保存图像到字节流
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300)
        buffer.seek(0)
        image_view.image = ui.Image.from_data(buffer.read())
        global image_buffer
        image_buffer = buffer
    except Exception as e:
        print(f'Error: {e}')

def button_action(sender):
    plot_type = 'function' if sender.title == 'Function Plot' else 'data'
    expression_input = sender.superview['expression_input'].text
    data_input = sender.superview['data_input'].text
    image_view = sender.superview['scroll_view']['image_view']
    create_plot(image_view, expression_input, plot_type, data_input)

def save_action(sender):
    global image_buffer
    print("Save action triggered.")

    if image_buffer is None:
        print("Image buffer is empty.")
        return

    folder_path = os.path.join(os.path.expanduser('~'), 'Documents', '图表文件夹')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取当前时间并格式化为字符串
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(folder_path, f'Image_{current_time}.png')
    
    if 'image_buffer' in globals():
        with open(filename, 'wb') as file:
            file.write(image_buffer.getvalue())
        print(f"Image saved to {filename}")
    else:
        print("No image to save.")

def create_ui():
    main_view = ui.View()
    main_view.name = 'Plot Viewer'
    main_view.background_color = 'white'

    expression_input = ui.TextField(frame=(10, 10, 300, 40), placeholder='Enter function expression')
    expression_input.name = 'expression_input'
    main_view.add_subview(expression_input)

    data_input = ui.TextField(frame=(10, 60, 300, 40), placeholder='Enter data (comma separated)')
    data_input.name = 'data_input'
    main_view.add_subview(data_input)

    function_button = ui.Button(title='Function Plot', frame=(10, 110, 200, 40), action=button_action)
    main_view.add_subview(function_button)

    data_button = ui.Button(title='Data Plot', frame=(220, 110, 200, 40), action=button_action)
    main_view.add_subview(data_button)

    save_button = ui.Button(title='Save Image', frame=(10, 150, 200, 40), action=save_action)
    main_view.add_subview(save_button)

    screen_width, screen_height = ui.get_screen_size()

    scroll_view = ui.ScrollView(frame=(10, 190, screen_width - 20, screen_height - 200))
    scroll_view.shows_horizontal_scroll_indicator = True
    scroll_view.shows_vertical_scroll_indicator = True
    scroll_view.name = 'scroll_view'

    image_view = ui.ImageView(frame=(0, 0, 2 * screen_width, 2 * screen_height))
    image_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
    image_view.name = 'image_view'
    scroll_view.add_subview(image_view)
    scroll_view.content_size = (2 * screen_width, 2 * screen_height)
    main_view.add_subview(scroll_view)

  
    main_view.present('fullscreen')

create_ui()