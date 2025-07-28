from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.slider import MDSlider, MDSliderHandle, MDSliderValueLabel
from kivymd.uix.fitimage import FitImage
from kivy.clock import Clock
from datetime import datetime
import RPi.GPIO as GPIO
from TEC_0602_2025 import MAX5144, TECController    #注意TEC初始化版本 新 (TEC_1010) 旧 （TEC_0903） (TEC_0602_2025)
from ad7928_0917001 import TemperatureSensor  # 导入温度传感器类 注意热明电阻初始化版本 新 （ad7928_1010001） 旧 （ad7928_0917001）

class MotorControlApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tec_controller = TECController(MAX5144(spi_bus=1, spi_device=1, cs_pin=17))
        self.sensor = TemperatureSensor()  # 初始化温度传感器

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"

        screen = MDScreen(md_bg_color=(1, 1, 1, 1))  # 设置背景颜色为白色

        layout = MDFloatLayout()

        # 设置温度按钮
        set_temperature_button = MDButton(
            MDButtonIcon(icon="thermometer"),
            MDButtonText(text="Set Temperature"),
            style="elevated",
            pos_hint={"center_x": 0.3, "center_y": 0.8},  # 调整位置
        )

        # 停止MAX1978按钮
        stop_max1978_button = MDButton(
            MDButtonIcon(icon="power"),
            MDButtonText(text="Stop MAX1978"),
            style="elevated",
            pos_hint={"center_x": 0.7, "center_y": 0.8},  # 调整位置
        )

        # 当前设定温度显示标签
        self.current_temperature_label = MDLabel(
            text="Current Set Temperature: -- °C",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )

        # 当前实际温度显示标签
        self.actual_temperature_label = MDLabel(
            text="Current Actual Temperature: -- °C",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # 显示传感器读取的实际温度
        )

        # 温度调节滑块
        self.temperature_slider = MDSlider(
            MDSliderHandle(),
            MDSliderValueLabel(),
            min=15,  #最小温度改这里！！！！！！！
            max=99,
            value=50,
            step=1,
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )

        # 日期和时间标签
        self.date_time_label = MDLabel(
            text="YYYY-MM-DD HH:MM:SS",
            halign="left",
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={"x": 0, "y": 0},
        )

        # 右下角的LOGO
        logo = FitImage(
            source='/home/nero/NBUSA.jpg',
            size_hint=(None, None),
            size=(dp(300), dp(180)), #size=(dp(200), dp(80)),
            pos_hint={"right": 1, "bottom": 1},
        )

        # 添加控件到布局中
        layout.add_widget(set_temperature_button)
        layout.add_widget(stop_max1978_button)
        layout.add_widget(self.current_temperature_label)
        layout.add_widget(self.actual_temperature_label)  # 添加显示实际温度的标签
        layout.add_widget(self.temperature_slider)
        layout.add_widget(self.date_time_label)
        layout.add_widget(logo)

        screen.add_widget(layout)

        # 定时更新日期时间和温度
        Clock.schedule_interval(self.update_date_time, 1)
        Clock.schedule_interval(self.update_actual_temperature, 0.5)  # 每2秒更新实际温度

        # 绑定按钮事件
        set_temperature_button.bind(on_press=self.set_temperature)
        stop_max1978_button.bind(on_press=self.stop_max1978)
        self.temperature_slider.bind(value=self.update_temperature)

        return screen

    def update_date_time(self, dt):
        now = datetime.now()
        self.date_time_label.text = now.strftime("%Y-%m-%d %H:%M:%S")

    def set_temperature(self, instance):
        self.tec_controller.set_temperature(self.temperature_slider.value)

    def update_temperature(self, instance, value):
        self.current_temperature_label.text = f"Current Set Temperature: {value} °C"

    def update_actual_temperature(self, dt):
        # 读取实际温度并更新显示
        actual_temperature = self.sensor.read_temperature()
        self.actual_temperature_label.text = f"Current Actual Temperature: {actual_temperature} °C"

    def stop_max1978(self, instance):
        GPIO.output(4, GPIO.LOW)
        print("MAX1978 has been stopped.")

    def on_stop(self):
        self.tec_controller.cleanup()
        self.sensor.cleanup()  # 清理传感器资源

if __name__ == "__main__":
    MotorControlApp().run()


