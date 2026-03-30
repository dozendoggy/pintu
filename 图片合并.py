import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import time


class ImageMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("图片合并工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 存储选中的图片路径
        self.image_paths = []

        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建标题
        self.title_label = tk.Label(self.main_frame, text="图片合并工具", font=("微软雅黑", 16, "bold"))
        self.title_label.pack(pady=10)

        # 创建按钮框架（顶部）
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # 添加图片按钮
        self.add_button = tk.Button(self.button_frame, text="添加图片", command=self.add_images, width=15, height=2)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # 删除选中图片按钮
        self.remove_button = tk.Button(self.button_frame, text="删除选中", command=self.remove_selected, width=15,
                                       height=2)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        # 清空按钮
        self.clear_button = tk.Button(self.button_frame, text="清空列表", command=self.clear_list, width=15, height=2)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # 创建图片列表框
        self.list_frame = tk.Frame(self.main_frame, height=200)
        self.list_frame.pack(fill=tk.BOTH, pady=10)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_listbox = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set, width=80, height=10)
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.image_listbox.yview)

        # 网格布局设置
        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.pack(pady=10)

        self.grid_frame_label = tk.Label(self.grid_frame, text="网格布局设置:")
        self.grid_frame_label.pack(side=tk.LEFT, padx=10)

        self.row_label = tk.Label(self.grid_frame, text="横排数量:")
        self.row_label.pack(side=tk.LEFT, padx=5)

        self.row_var = tk.StringVar(value="1")
        self.row_entry = tk.Entry(self.grid_frame, textvariable=self.row_var, width=5)
        self.row_entry.pack(side=tk.LEFT, padx=5)

        self.col_label = tk.Label(self.grid_frame, text="竖排数量:")
        self.col_label.pack(side=tk.LEFT, padx=5)

        self.col_var = tk.StringVar(value="2")
        self.col_entry = tk.Entry(self.grid_frame, textvariable=self.col_var, width=5)
        self.col_entry.pack(side=tk.LEFT, padx=5)

        # 输出路径设置
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(pady=10, fill=tk.X)

        self.output_label = tk.Label(self.output_frame, text="输出路径:")
        self.output_label.pack(side=tk.LEFT, padx=10)

        self.output_var = tk.StringVar(value=os.getcwd())
        self.output_entry = tk.Entry(self.output_frame, textvariable=self.output_var, width=50)
        self.output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.browse_button = tk.Button(self.output_frame, text="浏览", command=self.browse_output_path, width=10)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # 合并按钮
        self.merge_button = tk.Button(self.main_frame, text="合并图片", command=self.merge_images, width=30, height=3,
                                      bg="#4CAF50", fg="white", font=("微软雅黑", 12, "bold"))
        self.merge_button.pack(pady=20)

    def add_images(self):
        """添加图片"""
        filetypes = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("所有文件", "*.*")
        ]

        paths = filedialog.askopenfilenames(title="选择图片", filetypes=filetypes)
        if paths:
            for path in paths:
                if path not in self.image_paths:
                    self.image_paths.append(path)
                    self.image_listbox.insert(tk.END, os.path.basename(path))

    def remove_selected(self):
        """删除选中的图片"""
        selected_indices = self.image_listbox.curselection()
        if selected_indices:
            # 倒序删除，避免索引混乱
            for index in sorted(selected_indices, reverse=True):
                self.image_listbox.delete(index)
                self.image_paths.pop(index)

    def clear_list(self):
        """清空图片列表"""
        self.image_listbox.delete(0, tk.END)
        self.image_paths.clear()

    def browse_output_path(self):
        """浏览输出路径"""
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_var.set(folder)

    def merge_images(self):
        """合并图片"""
        if len(self.image_paths) < 2:
            messagebox.showwarning("警告", "至少需要选择2张图片")
            return

        try:
            # 获取网格布局参数
            try:
                rows = int(self.row_var.get())
                cols = int(self.col_var.get())
                if rows <= 0 or cols <= 0:
                    messagebox.showwarning("警告", "横排和竖排数量必须大于0")
                    return
            except ValueError:
                messagebox.showwarning("警告", "请输入有效的数字")
                return

            # 打开所有图片
            images = []
            for path in self.image_paths:
                img = Image.open(path)
                images.append(img)

            # 计算网格大小
            grid_size = rows * cols
            if len(images) > grid_size:
                messagebox.showwarning("警告", f"图片数量({len(images)})超过网格容量({grid_size})，多余的图片将被忽略")
                images = images[:grid_size]
            elif len(images) < grid_size:
                messagebox.showwarning("警告", f"图片数量({len(images)})少于网格容量({grid_size})，将用空白填充")

            # 找到所有图片的最大宽和高
            max_width = max(img.width for img in images)
            max_height = max(img.height for img in images)

            # 计算实际需要的行数
            actual_rows = (len(images) + cols - 1) // cols
            # 确保不超过用户指定的行数
            actual_rows = min(actual_rows, rows)

            # 计算总宽度和总高度
            total_width = max_width * cols
            total_height = max_height * actual_rows

            # 创建新图片
            result = Image.new('RGB', (total_width, total_height), (255, 255, 255))

            # 拼接图片到网格（保持原始比例，不拉伸）
            for i, img in enumerate(images):
                if i >= rows * cols:
                    break  # 超出网格容量的图片忽略
                
                row = i // cols
                col = i % cols
                
                # 计算图片在网格中的位置（居中放置，保留空白）
                x = col * max_width + (max_width - img.width) // 2
                y = row * max_height + (max_height - img.height) // 2
                
                result.paste(img, (x, y))

            # 使用时间戳生成文件名
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_var.get(), f"merged_{timestamp}.jpg")

            # 保存结果
            result.save(save_path)
            messagebox.showinfo("成功", f"图片合并成功，已保存到：{save_path}")

            # 询问是否打开图片
            if messagebox.askyesno("打开图片", "是否打开合并后的图片？"):
                os.startfile(save_path)

        except Exception as e:
            messagebox.showerror("错误", f"合并失败：{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageMerger(root)
    root.mainloop()