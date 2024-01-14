# 持枪视角可视化
# 视频设置最多选择
# 饰品大多数
# 各类外设大多数

import json
from collections import defaultdict
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from shapely.geometry import Point

file_path = 'data.json'
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

# 选手国家分布
country_counts = defaultdict(int)

for player_data in data:
    country = player_data["info"]["Country"]
    country_counts[country] += 1

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world['Player_Count'] = world['name'].map(country_counts)

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
world.plot(column='Player_Count', ax=ax, legend=True,
           legend_kwds={'label': "Number of Players by Country",
                        'orientation': "horizontal"}, cmap='coolwarm')
# plt.show()
plt.savefig('pic/Number of Players by Country')

# 年龄散点图
ages = []
current_year = 2024

for player in data:
    try:
        birth_year = int(player["info"]["Birthday"].split(",")[-1])
        age = current_year - birth_year
        ages.append(age)
    except (ValueError, IndexError):
        pass

plt.figure(figsize=(10, 6))
plt.scatter(range(1, len(ages) + 1), ages, alpha=0.5, color='blue')

plt.title('Players Age Distribution')
plt.xlabel('Players Index')
plt.ylabel('Age')

# plt.show()
plt.savefig('pic/Players Age Distribution')


# 鼠标edpi范围
edpi_values = []

for player in data:
    try:
        edpi = int(player["mouse"]["eDPI"])
        edpi_values.append(edpi)
    except (ValueError, KeyError):
        # 处理无效数据或缺失键的情况
        pass

# 创建散点图
plt.figure(figsize=(10, 6))
plt.scatter(range(1, len(edpi_values) + 1), edpi_values, alpha=0.5, color='blue')

# 设置图表标题和轴标签
plt.title('eDPI Distribution')
plt.xlabel('Player Index')
plt.ylabel('eDPI')

# plt.show()
plt.savefig('pic/eDPI Distribution')

styles = {}

for player in data:
    try:
        style = player["crosshair"]["Style"]
        styles[style] = styles.get(style, 0) + 1
    except (KeyError):
        # 处理缺失键的情况
        pass

# 创建扇形图
plt.figure(figsize=(8, 8))
plt.pie(styles.values(), labels=styles.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Crosshair Style Distribution')

# plt.show()
plt.savefig('pic/Crosshair Style Distribution')

colors = {}

for player in data:
    try:
        red = int(player["crosshair"]["Red"])
        green = int(player["crosshair"]["Green"])
        blue = int(player["crosshair"]["Blue"])

        if red >= 0 and green >= 0 and blue >= 0:
            color_key = f'{red}-{green}-{blue}'
            colors[color_key] = colors.get(color_key, 0) + 1
    except (KeyError, ValueError):
        # 处理缺失键或无效值的情况
        pass
# print(colors)

plt.figure(figsize=(10, 10))
labels = list(colors.keys())
sizes = list(colors.values())

colors_list = [tuple(map(int, key.split('-'))) for key in labels]
# print(colors_list)
normalized_colors = [(r/255, g/255, b/255) for r, g, b in colors_list]

plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=normalized_colors)
plt.title('Crosshair Color Distribution')

circle = plt.Circle((0, 0), 1, color='black', fc='none', linewidth=3.25)
plt.gca().add_artist(circle)

# plt.show()
plt.savefig('pic/Crosshair Color Distribution')


# 统计每个视频设置选项中最多的选择
video_options_count = {}

for player in data:
    video_settings = player.get("video", {})
    for option, choice in video_settings.items():
        if option not in video_options_count:
            video_options_count[option] = {}

        if choice not in video_options_count[option]:
            video_options_count[option][choice] = 1
        else:
            video_options_count[option][choice] += 1

# 找出每个视频设置选项中最多的选择
max_choices = {}
for option, choices in video_options_count.items():
    max_choice = max(choices, key=choices.get)
    max_choices[option] = max_choice

# 统计最多选择的占比
total_players = len(data)
percentage_data = {option: choices[max_choice] / total_players * 100 for option, choices, max_choice in zip(video_options_count.keys(), video_options_count.values(), max_choices.values())}

# 绘制柱状图
options = list(percentage_data.keys())
percentages = list(percentage_data.values())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(options, percentages, color='blue')

# 在每个柱子上标注占比
for bar, percentage in zip(bars, percentages):
    height = bar.get_height()
    ax.annotate(f'{percentage:.2f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.title('Most Chosen Video Settings and their Percentages')
plt.xlabel('Video Setting Options')
plt.ylabel('Percentage')
plt.ylim(0, 100)
plt.xticks(rotation=45, ha='right')

# plt.show()
plt.savefig('pic/Most Chosen Video Settings and their Percentages')
