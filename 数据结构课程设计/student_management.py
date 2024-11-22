import json
#学生类
class Student:
    def __init__(self,id,name,age,gender,grades):
        self.id=id
        self.name=name
        self.age=age
        self.gender=gender
        self.grades=grades #grades为一个字典，例如 {"语文": 90, "数学": 85, "英语": 88}
 #节点类
class Node:
    def __init__(self, student):
        self.student=student
        self.left=None
        self.right=None
 

class BST_management:
    def __init__(self):
        self.root = None

    # 插入数据
    def insert(self, student):
        node = Node(student)
        if self.root is None:
            self.root = node
        else:
            self._insert(self.root, node)

    def _insert(self, current, node):
        if node.student.id < current.student.id:
            if current.left is None:
                current.left = node
            else:
                self._insert(current.left, node)
        else:
            if current.right is None:
                current.right = node
            else:
                self._insert(current.right, node)
    # 查找数据
    def search(self, id):
        return self._search(self.root, id)
    def _search(self, current, id):
        if not current:
            return None
        if id == current.student.id:
            return current.student
        elif id < current.student.id:
            return self._search(current.left, id)
        else:
            return self._search(current.right, id)

    # 删除数据
    def delete(self, id):
        self.root = self._delete(self.root, id)

    def _delete(self, current, id):
        if not current:
            return current
        if id < current.student.id:
            current.left = self._delete(current.left, id)
        elif id > current.student.id:
            current.right = self._delete(current.right, id)
        else:
            if not current.left:
                return current.right
            elif not current.right:
                return current.left
            temp = self._find_min(current.right)
            current.student = temp.student
            current.right = self._delete(current.right, temp.student.id)
        return current

    def _find_min(self, current):
        while current.left:
            current = current.left
        return current
    # 非递归中序遍历
    def inorder_traversal(self):
        stack = []
        current = self.root
        result = []
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.student.id)  # 保存节点 ID
            current = current.right
        return result

    # 非递归前序遍历
    def preorder_traversal(self):
        stack = []
        current = self.root
        result = []
        while stack or current:
            if current:
                result.append(current.student.id)  # 先存储根节点值
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                current = current.right
        return result

    # 非递归后序遍历
    def poseorder_traversal(self):
        stack = []
        current = self.root
        result = []
        while stack or current:
            while current:
                result.append(current.student.id)  # 保存节点 ID
                stack.append(current)
                current = current.right
            current = stack.pop()
            current = current.left
        return result[::-1]  # 反转结果




    # 保存二叉树到 JSON 文件
    def save_to_file(self, filename):
        def serialize(node):
            if not node:
                return None
            return {
                "id": node.student.id,
                "name": node.student.name,
                "age": node.student.age,
                "gender": node.student.gender,
                "grades": node.student.grades,
                "left": serialize(node.left),
                "right": serialize(node.right)
            }

        data = serialize(self.root)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    # 从 JSON 文件加载二叉树
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                if not content:  # 如果文件为空
                    print(f"Warning: {filename} 文件为空，初始化为空树")
                    self.root = None
                    return
                data = json.loads(content)
                self.root = self._deserialize(data)  # 使用 _deserialize 方法转换为树结构
        except FileNotFoundError:
            print(f"Warning: {filename} 文件不存在，初始化为空树")
            self.root = None
        except json.JSONDecodeError as e:
            print(f"Error: 无法解析 {filename} 文件: {e}")
            self.root = None

    def _deserialize(self, data):
        """
        将 JSON 数据反序列化为二叉树节点
        """
        if not data:  # 如果数据为空
            return None
        student = Student(
            id=data["id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            grades=data["grades"]
        )
        node = Node(student)  # 创建节点
        node.left = self._deserialize(data.get("left"))  # 递归反序列化左子树
        node.right = self._deserialize(data.get("right"))  # 递归反序列化右子树
        return node



