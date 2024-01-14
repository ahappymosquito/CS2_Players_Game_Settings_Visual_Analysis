# 选手国家分布,年龄散点图
# 鼠标edpi范围
# 准星颜色，动态
# 持枪视角可视化
# 视频设置最多选择
# 饰品大多数
# 各类外设大多数

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取包含国家和统计数据的CSV文件
data = pd.read_csv('data/910.csv')

# 读取世界地图的shapefile文件
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# 将数据与地图数据合并
merged_data = world.merge(data, how='left', left_on='name', right_on='Country')

# 绘制地图
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
sns.heatmap(merged_data['Your_Column'], cmap='YlGnBu', linewidths=0.5, ax=ax)

# 设置图表标题和颜色条
plt.title('World Map Distribution')
cbar = plt.colorbar()
cbar.set_label('Your Data')

# 显示地图
plt.show()
