#AutoScriptForGF
该脚本基于opencv和adb实现。
是一个拿来拖尸的普通脚本（确信）。
目前仅完成了VV-UZI的换打手13-4拖尸以及一个用于2.0版本的GUI（懒，而且过一阵子就要重构成C++项目（前提是我不摸））

##安装要求

opencv=4.5.3.56（pyinstaller不支持4.6.0）
Pyqt5=5.15.7
python=3.9.12


##安装步骤
安装能正常使用的opencv,Pyqt5即可（目前确定能使用的最低版本为4.4.0.42）
adb为模拟器自带

##打包
批处理文件以及写好了，修改一下spec文件以及确保pyinstaller能正常使用即可
