#!python3

'''
这个小部件脚本显示了一个快捷按钮网格，当点击这些按钮时会启动 URL。

 快捷方式标题/URL 和网格布局可以使用 SHORTCUTS、COLS、ROWS 变量进行配置。
'''

import appex, ui
import os
from math import ceil, floor

# 注意：ROWS 变量确定“紧凑”模式下的行数。 在展开模式下，小部件显示所有快捷方式。
COLS = 3
ROWS = 2

#每个快捷方式都应该是一个至少带有“title”和“url”键的字典。  “颜色”和“图标”是可选的。 如果设置，'icon':'iow:icon_social_google_plus_256'应该是内置图像的名称。{'title':'sgf','url':'frontlinewatcher://','color':'red'}

SHORTCUTS = [
{'title': '积分导数', 'url': 'pythonista3://WeijiFen.py?a=123', 'color': '#F65CFF', 'icon': 'iow:ios7_recording_32'},{"title": "复数运算", "url": "pythonista3://complex.py?a=123", 'color': "#c40000", "icon": 'iow:ios7_location_24'},{'title': '逻辑代数', 'url': 'pythonista3://logic.py?a=123', 'color': '#FF2121','icon':'iow:chatbubble_24'},{'title': '图表分析', 'url': 'pythonista3://Graph_plt.py?a=123', 'color': '#1E90FF','icon':'iow:ios7_keypad_outline_24'},{'title': '因式分解', 'url': 'pythonista3://factorization.py?a=123', 'color': '#45d3e8', 'icon': 'iow:earth_32'},{'title': '微积分', 'url': 'pythonista3://limit.py?a=123', 'color': '#FF2121','icon':'iow:connection_bars_32'},
{'title':'Quan-X','url':'quantumult-x://','color':'#b51eff','icon':'iob:nuclear_24'},

{'title': 'Github', 'url': 'https://github.com/bigmom2012/surge4', 'color': '#392F41','icon':'iow:social_github_32'},
{'title': 'Fileball', 'url': 'filebox://', 'color': '#D9B611','icon':'iow:ios7_folder_32'},
{'title': '阿里云盘', 'url': 'aliyundrive://', 'color': '#4B5CC4','icon':'iow:ios7_cloudy_32'},
{'title': '微信扫码', 'url': 'weixin://scanqrcode', 'color': '#40DE5A','icon':'iow:ios7_camera_32'},
{'title':'支付宝', 'url': 'alipay://', 'color':'#0074ff','icon':'iow:social_bitcoin_24'},{'title': '蓝奏云', 'url': 'https://pc.woozooo.com/mydisk.php', 'color': '#ff8e13','icon':'iow:ios7_cloud_24'},{'title':' W3school','url':'https://www.w3school.com.cn/','color':'ff0092','icon':'iow:social_wordpress_24'},{'title':'路由器','url':'http://192.168.0.1/index.html','color':'#177CB0','icon':'iow:wifi_24'},{'title':'翻译', 'url':'googletranslate://','color':'#801DAE','icon':'iow:icon_social_google_plus_32'},{'title':'计算器🧮','url':'pythonista://Calculator.py?a=123','color':'#06c33c','icon':'iow:calculator_32'},{'title':'钉钉打卡','url':'dingtalk://wfmdingtalk-hw.gaiaworkforce.com/?companyCode=highpower&state=dd&version=20220818135#/signin','color':'#21a0ff','icon':'iow:social_twitter_outline_32'},
]

class LauncherView (ui.View):
	def __init__(self, shortcuts, *args, **kwargs):
		row_height = 110 / ROWS
		super().__init__(self, frame=(0, 0, 400, ceil(len(shortcuts) / COLS) * row_height), *args, **kwargs)
		self.buttons = []
		# 将每个按钮功能进行添加至UI控件中
		# 如果之前icon不设置，那默认采用有compass_24图标；color字段也一样
		for s in shortcuts:
			btn = ui.Button(title=' ' + s['title'], image=ui.Image(s.get('icon', 'iow:ios7_heart_32')), name=s['url'], action=self.button_action, bg_color=s.get('color', '#ff0808'), tint_color='#fffbf7', corner_radius=20)
			self.add_subview(btn)
			self.buttons.append(btn)
	
	# 界面按钮大小布局
	def layout(self):
		bw = self.width / COLS
		bh = floor(self.height / ROWS) if self.height <= 130 else floor(110 / ROWS)
		for i, btn in enumerate(self.buttons):
			btn.frame = ui.Rect(i%COLS * bw, i//COLS * bh, bw, bh).inset(3, 2)
			btn.alpha = 1 if btn.frame.max_y < self.height else 0
	# 按钮点击关联的功能
	def button_action(self, sender):
		import shortcuts
		shortcuts.open_url(sender.name)

def main():
	widget_name = __file__ + str(os.stat(__file__).st_mtime)
	v = appex.get_widget_view()
	# 优化：如果小部件已经显示启动器，则不要创建新视图。
	if v is None or v.name != widget_name:
		v = LauncherView(SHORTCUTS)
		v.name = widget_name
		appex.set_widget_view(v)

if __name__ == '__main__':
	main()