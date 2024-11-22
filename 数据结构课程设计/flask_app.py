from flask import Flask, request, jsonify, render_template
from student_management import BST_management, Student,Node  # 原代码在 bst_management.py 文件中
from datetime import datetime
import time
bst = BST_management()
FILENAME = "students.json"

# 在程序启动时加载数据
bst.load_from_file(FILENAME)

app = Flask(__name__)

# 首页
@app.route('/')
def index():
    return render_template('index.html')



# 插入学生数据，通过 POST 请求处理插入表单
@app.route('/insert', methods=['POST'])
def insert_student():
    data = request.form
    student_id = int(data['id'])

    # 检查学生 ID 是否已存在
    if bst.search(student_id):
        return jsonify({"error": "插入的学生 ID 已存在！，请检查并重新输入"})

    # 如果不存在，插入数据
    grades = {
        "语文": int(data['chinese']),
        "数学": int(data['math']),
        "英语": int(data['english'])
    }
    student = Student(
        id=student_id,
        name=data['name'],
        age=int(data['age']),
        gender=data['gender'],
        grades=grades
    )
    bst.insert(student)
    bst.save_to_file(FILENAME)  # 保存到文件
    return render_template('insert_result.html', message=f"学号为{student_id}的学生数据存储成功!")



@app.route('/search', methods=['GET'])
def search_student():
    student_id = request.args.get('id')  # 从查询参数中获取学生 ID
    if student_id:
        start_time = time.perf_counter()  # 记录开始时间
        try:
            student = bst.search(int(student_id))
        except Exception as e:
            student = None
        end_time = time.perf_counter()    # 记录结束时间
        elapsed_time = (end_time - start_time) * 1000  # 转换为毫秒

        if student:
            # 渲染结果页面，传递学生信息和查询时间
            return render_template('search_result.html', student=student, query_time=elapsed_time)
        else:
            # 如果未找到学生，返回错误页面和查询时间
            return render_template('search_result.html', error="未找到该学生！", query_time=elapsed_time)
    # 如果没有提供学生 ID，返回错误消息
    return render_template('search_result.html', error="未提供学生 ID！")


@app.route('/delete', methods=['POST'])
def delete_student_form():
    student_id = request.form.get('id')  # 从表单中获取学生 ID
    if student_id:
        bst.delete(int(student_id))
        bst.save_to_file(FILENAME)  # 保存到文件
        return render_template('delete_result.html', message=f"学号为{student_id}的学生数据删除成功!")
    return render_template('delete_result.html', error="没有该学生数据")



@app.route('/view', methods=['GET'])
def view_students():
    def traverse_and_collect(node):
        if not node:
            return []
        # 当前节点的学生信息
        current_student = {
            "id": node.student.id,
            "name": node.student.name,
            "age": node.student.age,
            "gender": node.student.gender,
            "grades": node.student.grades
        }
        # 合并左子树、当前节点、右子树的学生信息
        return traverse_and_collect(node.left) + [current_student] + traverse_and_collect(node.right)

    # 获取所有学生数据
    students = traverse_and_collect(bst.root)
    return jsonify(students)  # 返回 JSON 格式的学生列表



@app.route('/view_students_page', methods=['GET'])
def view_students_page():
    def traverse_and_collect(node):
        if not node:
            return []
        # 当前节点的学生信息
        current_student = {
            "id": node.student.id,
            "name": node.student.name,
            "age": node.student.age,
            "gender": node.student.gender,
            "grades": node.student.grades
        }
        # 合并左子树、当前节点、右子树的学生信息
        return traverse_and_collect(node.left) + [current_student] + traverse_and_collect(node.right)

    # 获取所有学生数据
    students = traverse_and_collect(bst.root)
    return render_template('view_students.html', students=students)

# 返回树的 JSON 数据
@app.route('/view_tree', methods=['GET'])
def view_tree():
    def build_tree(node):
        if not node:
            return None
        return {
            "id": node.student.id,
            "left": build_tree(node.left),
            "right": build_tree(node.right)
        }

    tree_data = build_tree(bst.root)
    if not tree_data:
        return jsonify({"error": "Tree is empty"}), 404
    return jsonify(tree_data)

# 返回二叉树可视化页面
@app.route('/view_tree_page', methods=['GET'])
def view_tree_page():
    return render_template('view_tree.html')

@app.route('/sync', methods=['POST'])
def sync_data():
    try:
        bst.load_from_file(FILENAME)  # 重新加载文件数据
        return jsonify({"message": "数据更新成功！"})  # 返回成功消息
    except Exception as e:
        return jsonify({"error": f"数据更新失败: {str(e)}"}), 500
    
@app.route('/traverse/<traversal_type>', methods=['GET'])
def traverse_tree(traversal_type):
    """
    根据遍历类型返回结果：前序、中序、后序
    """
    traversal_map = {
        "preorder": "前序",
        "inorder": "中序",
        "postorder": "后序"
    }
    traversal_name = traversal_map.get(traversal_type, None)
    if not traversal_name:
        return jsonify({"error": "无效的遍历类型"}), 400

    if traversal_type == "preorder":
        result = bst.preorder_traversal()
    elif traversal_type == "inorder":
        result = bst.inorder_traversal()
    elif traversal_type == "postorder":
        result = bst.poseorder_traversal()
    else:
        return jsonify({"error": "无效的遍历类型"}), 400

    return jsonify({"traversal_type": traversal_name, "result": result})



if __name__ == '__main__':
    app.run(debug=True)

