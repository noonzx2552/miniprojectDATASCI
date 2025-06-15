import pandas as pd  # นำเข้าไลบรารี pandas เพื่อจัดการข้อมูลในรูปแบบ DataFrame
import matplotlib.pyplot as plt  # นำเข้า matplotlib.pyplot สำหรับวาดกราฟ
import matplotlib.gridspec as gridspec  # นำเข้า GridSpec เพื่อจัดโครงร่าง subplot หลายกราฟในหน้าเดียว

"""
Variables & Units:
- time_spent_alone: Hours spent alone daily (0–11).
- stage_fear: Presence of stage fright (Yes/No).
- social_event_attendance: Frequency of social events (0–10).
- going_outside: Frequency of going outside (0–7).
- drained_after_socializing: Feeling drained after socializing (Yes/No).
- friends_circle_size: Number of close friends (0–15).
- post_frequency: Social media post frequency (0–10).
- personality: Target variable (Extrovert/Introvert).
"""
# บันทึกคำอธิบายตัวแปรและหน่วยวัดไว้ใน docstring เพื่อความเข้าใจ

# 1. Load & clean data
df = pd.read_csv("personality_datasert.csv")  # โหลดข้อมูลจากไฟล์ CSV เข้ามาเป็น DataFrame ชื่อ df
df.drop_duplicates(inplace=True)               # ลบแถวที่ซ้ำกันออก เพื่อหลีกเลี่ยงข้อมูลซ้ำซ้อน
df.dropna(inplace=True)                        # ลบแถวที่มีค่า NaN เพื่อให้ข้อมูลสมบูรณ์
df.columns = [                                   # ปรับชื่อคอลัมน์ให้เป็นมาตรฐาน
    col.strip()                                  #   - ตัดช่องว่างทั้งสองด้านออก
    .lower()                                     #   - เปลี่ยนเป็นตัวพิมพ์เล็กทั้งหมด
    .replace(" ", "_")                           #   - แทนที่เว้นวรรคด้วยขีดล่าง
    for col in df.columns
]

# Round numeric columns
numeric_cols = df.select_dtypes(include="number").columns  # หาคอลัมน์ที่เป็นตัวเลขทั้งหมด
df[numeric_cols] = df[numeric_cols].round(1)               # ปัดทศนิยมให้เหลือ 1 ตำแหน่ง

# Remove decimals from friends_circle_size
if "friends_circle_size" in df.columns:            # ตรวจสอบว่ามีคอลัมน์ friends_circle_size หรือไม่
    df["friends_circle_size"] = (               # ถ้ามี ให้ปัดทศนิยมแล้วแปลงเป็นจำนวนเต็ม
        df["friends_circle_size"].round().astype(int)
    )

# 2. Define colors & ordering
introvert_color       = "#ff9999"  # กำหนดสีสำหรับกลุ่ม Introvert
extrovert_color       = "#66b3ff"  # กำหนดสีสำหรับกลุ่ม Extrovert
color_pair            = [introvert_color, extrovert_color]  # สร้างลิสต์สี
ordered_personalities = ["Introvert", "Extrovert"]           # ลำดับการแสดงผลของบุคลิกภาพ

# 3. Prepare pie-chart data
stage_fear_counts  = df["stage_fear"].value_counts().sort_index()             # นับจำนวน Yes/No ใน stage_fear แล้วจัดเรียงตามค่า
drain_counts       = df["drained_after_socializing"].value_counts().sort_index()  # นับจำนวน Yes/No ใน drained_after_socializing
personality_counts = df["personality"].value_counts().sort_index()               # นับจำนวน Introvert/Extrovert

# 4. Prepare stacked-bar data
stacked_alone   = df.groupby(["time_spent_alone",      "personality"]).size().unstack(fill_value=0)
#   - จัดกลุ่มข้อมูลตามชั่วโมงที่อยู่คนเดียวและบุคลิกภาพ แล้วนับขนาดกลุ่ม
stacked_social  = df.groupby(["social_event_attendance","personality"]).size().unstack(fill_value=0)
#   - จัดกลุ่มตามความถี่เข้าร่วมกิจกรรมสังคมและบุคลิกภาพ
stacked_outside = df.groupby(["going_outside",         "personality"]).size().unstack(fill_value=0)
#   - จัดกลุ่มตามความถี่ออกไปข้างนอกและบุคลิกภาพ
stacked_friends = df.groupby(["friends_circle_size",   "personality"]).size().unstack(fill_value=0)
#   - จัดกลุ่มตามจำนวนเพื่อนสนิทและบุคลิกภาพ
stacked_post    = df.groupby(["post_frequency",        "personality"]).size().unstack(fill_value=0)
#   - จัดกลุ่มตามความถี่โพสต์โซเชียลมีเดียและบุคลิกภาพ

# 5. Plot dashboard
fig = plt.figure(figsize=(16, 12))                 # สร้างหน้ากราฟขนาด 16x12 นิ้ว
gs  = gridspec.GridSpec(3, 3,                       # กำหนด GridSpec 3 แถว 3 คอลัมน์
                       height_ratios=[1, 1, 1.2],   # ความสูงแต่ละแถว (แถวล่างใหญ่ขึ้นเล็กน้อย)
                       hspace=0.4)                  # ระยะห่างแนวตั้งระหว่างแถว

# Pie charts
for idx, (data, title, colors) in enumerate([
    (stage_fear_counts,   "Stage Fear",                [extrovert_color, introvert_color]),
    (drain_counts,        "Drained After Socializing", [extrovert_color, introvert_color]),
    (personality_counts,  "Personality",               color_pair),
]):
    ax = fig.add_subplot(gs[0, idx])                 # วาง subplot ในแถวที่ 0 และคอลัมน์ idx
    ax.pie(
        data,                                        # ข้อมูลให้ pie chart
        labels=data.index,                           # ป้ายชื่อชิ้นส่วนคือค่าดัชนี
        autopct="%1.1f%%",                           # แสดงเปอร์เซ็นต์ 1 ตำแหน่งทศนิยม
        startangle=90,                               # เริ่มต้นวาดที่มุม 90 องศา
        colors=colors,                               # กำหนดสีของแต่ละชิ้น
        textprops={"fontsize": 8}                    # ขนาดฟอนต์ของข้อความในกราฟ
    )
    ax.set_title(title, fontsize=10)                 # ตั้งชื่อกราฟย่อย

# Helper to plot stacked bars with proper labels
def plot_stacked(ax, df_stacked, xlabel, title):
    """
    ฟังก์ชันช่วยวาดกราฟแท่งซ้อน (stacked bar)
    ax         : แกนกราฟที่ต้องการวาด
    df_stacked : DataFrame ที่จัดกลุ่มและนับไว้แล้ว
    xlabel     : ชื่อแกน X
    title      : ชื่อกราฟ
    """
    df_stacked[ordered_personalities].plot(
        kind="bar", stacked=True,                    # สร้างกราฟแท่งซ้อน
        color=color_pair, ax=ax                      # ใช้คู่สีที่กำหนด
    )
    ax.set_title(title, fontsize=10)                  # ตั้งชื่อกราฟย่อย
    ax.set_xlabel(xlabel, fontsize=9)                 # ตั้งชื่อแกน X
    ax.set_ylabel("Number of people", fontsize=9)     # ตั้งชื่อแกน Y
    ax.tick_params(axis="x", rotation=45, labelsize=8)  # หมุนป้ายแกน X 45 องศา
    ax.legend(
        title="Personality",                          # ชื่อเลเจนด์
        labels=ordered_personalities,                 # ป้ายเลเจนด์
        loc="upper right",                            # ตำแหน่งเลเจนด์
        fontsize=8, title_fontsize=9                  # ขนาดฟอนต์เลเจนด์
    )

# Middle row of stacked-bar charts
plot_stacked(
    fig.add_subplot(gs[1, 0]),                        # แถวที่ 1 คอลัมน์ 0
    stacked_alone,                                     # ข้อมูลแท่งซ้อนสำหรับเวลาที่อยู่คนเดียว
    "Hours spent alone daily (0–11)",                  # ชื่อแกน X
    "Time Spent Alone"                                 # ชื่อกราฟ
)
plot_stacked(
    fig.add_subplot(gs[1, 1]),                        # แถวที่ 1 คอลัมน์ 1
    stacked_social,                                    # ข้อมูลแท่งซ้อนสำหรับการเข้าร่วมกิจกรรมสังคม
    "Frequency of social events (0–10)",
    "Social Events"
)
plot_stacked(
    fig.add_subplot(gs[1, 2]),                        # แถวที่ 1 คอลัมน์ 2
    stacked_outside,                                   # ข้อมูลแท่งซ้อนสำหรับความถี่ออกไปข้างนอก
    "Frequency of going outside (0–7)",
    "Going Outside"
)

# Bottom row of stacked-bar charts
plot_stacked(
    fig.add_subplot(gs[2, 0]),                        # แถวที่ 2 คอลัมน์ 0
    stacked_friends,                                   # ข้อมูลแท่งซ้อนสำหรับจำนวนเพื่อนสนิท
    "Number of close friends (0–15)",
    "Friends Circle"
)
plot_stacked(
    fig.add_subplot(gs[2, 1]),                        # แถวที่ 2 คอลัมน์ 1
    stacked_post,                                      # ข้อมูลแท่งซ้อนสำหรับความถี่โพสต์โซเชียลมีเดีย
    "Social media post frequency (0–10)",
    "Post Frequency"
)

# Title box in bottom-right
ax = fig.add_subplot(gs[2, 2])                       # แถวที่ 2 คอลัมน์ 2
ax.axis("off")                                        # ปิดแกน ไม่แสดงกรอบใดๆ
ax.text(
    0.5, 0.5,
    "Extrovert vs. Introvert Behavioral Data Analysis",  # ข้อความแสดงในกล่อง
    fontsize=12, ha="center", va="center"               # จัดกึ่งกลางทั้งแนวนอนและแนวตั้ง
)

# Overall title and layout adjustment
fig.suptitle("Behavioral Personality Dashboard", fontsize=14)  # ตั้งชื่อกราฟหลัก
plt.tight_layout(rect=[0, 0, 1, 0.96])                         # ปรับระยะขอบให้เหมาะสม
plt.show()                                                     # แสดงกราฟทั้งหมด
