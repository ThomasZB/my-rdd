# 道路故障实时检测
注：项目基于[hiroyamaeda](https://github.com/sekilab/RoadDamageDetector)提供的模型和训练集，代码实现了将RoadDamageDetector项目的模型应用于tensorflow2.0，可以在tensorflow2.0的基础上进行输出某些层进行迁移学习。

项目代码前面添加了中值滤波，能在同一个地方静止的条件下滤除运动物体，便于项目在固定地点进行实时的道路故障检测

## 启动
调用GUI_A.py可以直接运行程序，程序会完成识别并显示结果，road_damage_detective.py为预测函数存放的地方，其他相关函数放在function里面，启用前确保安装了Tensorflow2.0,wxPython,numpy,matplot等库
