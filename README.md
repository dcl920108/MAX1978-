**TEC_ControlApp**

**Description**
A KivyMD-based GUI application for controlling a TEC (Thermo-Electric Cooler) via the MAX1978 controller and monitoring temperature with an AD7928-based sensor. Features include:

* Set target temperature using a slider.
* Emergency stop for the TEC controller (MAX1978).
* Real-time display of the current set temperature and actual temperature readings.
* Date and time display.
* Static logo display.

**Features**

* Temperature control via `MAX5144` DAC and `MAX1978` TEC controller.
* Temperature monitoring via `AD7928` temperature sensor.
* GUI components: buttons, slider, labels, and images using KivyMD.
* Periodic updates with Kivy `Clock` scheduling.
* Clean resource release on application exit.

**Dependencies**

* Python 3
* Kivy ≥ 2.1.0
* KivyMD latest
* RPi.GPIO
* KivyMD slider module
* Matplotlib (if extended for charting)

**Installation**

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev libgles2-mesa-dev libgl1-mesa-dev
pip3 install kivy kivymd RPi.GPIO
```

**Hardware Setup**

1. Connect MAX1978 enable pin to GPIO4 (BCM).
2. Connect SPI bus 1, device 1 to MAX5144 DAC, CS pin 17.
3. Connect AD7928 sensor to the I2C/SPI interface as per `ad7928_0917001` wiring.
4. Place the logo image at `/home/nero/NBUSA.jpg` or update the path accordingly.

**Usage**

```bash
python3 motor_control_app.py
```

* Use the slider to choose a temperature between 15°C and 99°C.
* Click "Set Temperature" to apply the target temperature.
* Observe actual temperature readings updating every 0.5s.
* Click "Stop MAX1978" to immediately disable the TEC heater.

**File Structure**

```
project_folder/
├── motor_control_app.py   # Main application
├── TEC_0602_2025.py       # TEC controller definitions
├── ad7928_0917001.py      # Temperature sensor definitions
├── README.md              # This file
└── NBUSA.jpg              # Logo image
```

**License**
MIT License

---

**TEC_ControlApp**

**项目描述**
一个基于 KivyMD 的 GUI 应用，用于通过 MAX1978 控制 TEC（热电制冷器），并使用基于 AD7928 的传感器监测温度。功能包括：

* 通过滑块设置目标温度。
* 紧急停止 TEC 控制器（MAX1978）。
* 实时显示当前设定温度和实际温度读数。
* 显示日期和时间。
* 静态 Logo 显示。

**主要功能**

* 通过 `MAX5144` DAC 和 `MAX1978` TEC 控制器进行温度控制。
* 通过 `AD7928` 温度传感器进行温度监测。
* 使用 KivyMD 构建按钮、滑块、标签和图像等 GUI 组件。
* 使用 Kivy `Clock` 定时更新。
* 应用退出时自动释放资源。

**依赖**

* Python 3
* Kivy ≥ 2.1.0
* KivyMD 最新版
* RPi.GPIO
* KivyMD 滑块模块
* Matplotlib（如需绘制图表）

**安装**

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev libgles2-mesa-dev libgl1-mesa-dev
pip3 install kivy kivymd RPi.GPIO
```

**硬件连接**

1. 将 MAX1978 启用引脚接到 GPIO4（BCM）。
2. 将 SPI 总线 1 设备 1 连接到 MAX5144 DAC，片选脚 17。
3. 按照 `ad7928_0917001` 接线将 AD7928 传感器连接到 I2C/SPI 接口。
4. 将 Logo 图片放置在 `/home/nero/NBUSA.jpg`，或相应更新路径。

**使用方法**

```bash
python3 motor_control_app.py
```

* 使用滑块选择 15°C 到 99°C 之间的温度。
* 点击“Set Temperature”应用目标温度。
* 实际温度每 0.5 秒更新一次。
* 点击“Stop MAX1978”立即关闭 TEC 加热。

**文件结构**

```
project_folder/
├── motor_control_app.py   # 主程序
├── TEC_0602_2025.py       # TEC 控制器定义
├── ad7928_0917001.py      # 温度传感器定义
├── README.md              # 本文件
└── NBUSA.jpg              # Logo 图片
```

**许可**
MIT 许可证
