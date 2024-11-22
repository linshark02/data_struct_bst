import random
from student_management import Student, BST_management

# 生成随机学生数据
def generate_random_students():
    students = []
    for _ in range(100):  # 除根节点外的19个学生
        id = int(f"2024{random.randint(100, 999)}")
        name = random.choice([
            "小明", "小红", "小刚", "小丽", "小强", "小芳", "小李", "小王", "小张", "小赵",
            "小周", "小郑", "小许", "小吴", "小沈", "小陈", "小韩", "小杨", "小胡", "小田",
            "小马", "小高", "小孙", "小何", "小蒋", "小顾", "小丁", "小林", "小欧", "小魏",
            "小方", "小翁", "小梁", "小唐", "小卢", "小叶", "小钟", "小黄", "小汪", "小申",
            "小尤", "小许", "小冯", "小曹", "小缪", "小乔", "小曾", "小施", "小葛", "小余",
            "小卜", "小元", "小单", "小谈", "小廖", "小伍", "小尹", "小鲁", "小韦", "小昝",
            "小苏", "小潘", "小董", "小戴", "小岳", "小夏", "小钟", "小甘", "小石", "小姚",
            "小邵", "小湛", "小汤", "小殷", "小罗", "小毕", "小郝", "小邬", "小安", "小常",
            "小乐", "小于", "小时", "小齐", "小伏", "小麦", "小薄", "小卓", "小蔡", "小屠",
            "小粘", "小庞", "小关", "小党", "小家", "小祁", "小褚", "小裘", "小缪", "小干",
            "小解", "小应", "小宗", "小丁", "小宣", "小贲", "小邓", "小郁", "小单", "小杭",
        ])
        age = random.randint(18, 25)
        gender = random.choice(["男", "女"])
        grades = {
            "语文": random.randint(60, 100),
            "数学": random.randint(60, 100),
            "英语": random.randint(60, 100)
        }  # 生成带科目名称的成绩字典
        students.append(Student(id, name, age, gender, grades))
    return students

# 插入学生到二叉搜索树
def insert_students_into_bst():
    bst = BST_management()

    # 插入根节点
    root_student = Student(
        2024500, "小李子", 21, "男", 
        {"语文": 90, "数学": 85, "英语": 88}
    )
    bst.insert(root_student)

    # 插入随机生成的学生
    random_students = generate_random_students()
    for student in random_students:
        bst.insert(student)

    return bst

# 主函数
if __name__ == "__main__":
    bst = insert_students_into_bst()  # 创建并填充二叉搜索树

    # 保存数据到 students.json 文件
    filename = "students.json"
    bst.save_to_file(filename)
    print(f"学生数据已保存到 {filename}")
