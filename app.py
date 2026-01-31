from datetime import datetime
from flask import Flask, render_template, abort, send_file
from data.products import PRODUCTS
from data.blogs import BLOGS
import os

app = Flask(__name__)


# 新增：谷歌验证文件路由（让根目录可直接访问验证文件）
@app.route('/googlef04969ca713c673e.html')
def google_verification():
    # 拼接验证文件的完整路径（static文件夹下）
    file_path = os.path.join(app.static_folder, 'googlef04969ca713c673e.html')
    # 检查文件是否存在，避免返回500错误
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File Not Found", 404


# Flask app.py 中新增sitemap路由
from flask import send_file
import os
from flask import current_app  # 避免直接用app变量的问题


# 替换原来的sitemap路由
@app.route('/sitemap.xml')
def serve_sitemap():
    # 1. 确认文件路径是static文件夹下的sitemap.xml
    sitemap_path = os.path.join(current_app.static_folder, 'sitemap.xml')

    # 2. 检查文件是否存在
    if not os.path.exists(sitemap_path):
        return "Sitemap not found", 404

    # 3. 关键：强制设置Content-Type为application/xml（谷歌要求的格式）
    return send_file(
        sitemap_path,
        mimetype='application/xml',  # 必须是这个值，不能是text/html
        as_attachment=False  # 不允许浏览器下载，直接在页面显示
    )


# 新增：robots.txt 路由
@app.route('/robots.txt')
def robots_txt():
    # 拼接static文件夹下robots.txt的完整路径
    file_path = os.path.join(app.static_folder, 'robots.txt')
    # 检查文件是否存在，避免返回500错误
    if os.path.exists(file_path):
        # 返回txt文件，指定content-type确保蜘蛛正确解析
        return send_file(file_path, mimetype='text/plain')
    else:
        return "Robots.txt Not Found", 404


# ===== 核心：自动扫描图片文件夹的工具函数（适配PythonAnywhere + 固定文件夹顺序） =====
def scan_product_images(product):
    """
    自动扫描产品图片文件夹，返回整理后的图片结构
    :param product: 单个产品字典（来自 PRODUCTS）
    :return: 包含分类和图片列表的字典
    """
    # 1. 构建固定路径（关键：适配PythonAnywhere，补充products层 + 统一小写）
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_name = product.get("model") or product.get("name").replace(" ", "_").lower()
    model_name = model_name.lower()  # 强制转小写，解决大小写不匹配问题
    local_base_path = os.path.join(project_root, "static", "images", "products", model_name)
    frontend_image_base = "/static/images/products/" + model_name + "/"

    # 2. 检查本地图片目录是否存在（不存在直接返回空结果）
    if not os.path.exists(local_base_path):
        print(f"图片目录不存在：{local_base_path}")  # 调试信息，方便排查
        return {"base_path": frontend_image_base, "categories": {}, "main_image": None}

    # 3. 定义有效图片后缀（核心修复：添加 .webp 和 .WEBP，支持WebP格式）
    valid_image_extensions = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG", ".webp", ".WEBP")

    # 4. 初始化返回结果
    image_result = {
        "base_path": frontend_image_base,  # 前端访问路径（对应PythonAnywhere静态映射）
        "categories": {}  # 分类字典：key=文件夹名，value={name: 展示名称, images: 图片列表}
    }

    # 5. 核心：定义文件夹优先展示顺序（裸机在前，包装在后，可扩展）
    # 先展示的文件夹放在列表前面，未在列表中的文件夹后续按字母排序补充
    preferred_folder_order = ["bare_metal", "packing"]

    # 6. 扫描所有子文件夹，先收集所有有效文件夹
    all_folders = []
    for folder_name in os.listdir(local_base_path):
        folder_path = os.path.join(local_base_path, folder_name)
        if os.path.isdir(folder_path):  # 只收集文件夹
            all_folders.append(folder_name)

    # 7. 按优先顺序整理文件夹（保证bare_metal在前，packing在后）
    sorted_folders = []
    # 第一步：添加优先顺序中的文件夹（存在才添加）
    for folder in preferred_folder_order:
        if folder in all_folders:
            sorted_folders.append(folder)
            all_folders.remove(folder)  # 避免重复添加
    # 第二步：添加剩余文件夹（按字母正序排序，保证一致性）
    sorted_folders += sorted(all_folders)

    # 8. 遍历排序后的文件夹，处理图片数据
    for folder_name in sorted_folders:
        folder_path = os.path.join(local_base_path, folder_name)

        # 9. 扫描该文件夹下的所有有效图片
        image_files = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            # 筛选：是文件 + 后缀有效
            if os.path.isfile(file_path) and file_name.endswith(valid_image_extensions):
                image_files.append(file_name)

        # 10. 对图片列表按文件名排序（确保 1.jpg < 2.jpg < 3.jpg，支持WebP）
        try:
            image_files.sort(
                key=lambda x: int(''.join(filter(str.isdigit, x))) if any(str.isdigit(c) for c in x) else x
            )
        except:
            image_files.sort()  # 排序失败时默认排序，避免报错

        # 11. 整理分类信息（文件夹名转展示名称，如 bare_metal → Bare Metal）
        display_name = folder_name.replace("_", " ").title()

        # 12. 存入返回结果
        image_result["categories"][folder_name] = {
            "name": display_name,
            "images": image_files
        }

        # 13. 优先提取 main 分类的第一张图片作为主图（支持WebP格式）
        if folder_name == "main" and image_files:
            image_result["main_image"] = {
                "path": f"{image_result['base_path']}{folder_name}/{image_files[0]}",
                "alt": product.get("image_alt", {}).get("main", product.get("name", "Product Image"))
            }

    return image_result


@app.route('/version')
def version():
    return f"Latest code loaded at: {datetime.now()}"


@app.route('/')
def base():
    return render_template('base.html')


# ===== 原有路由修改（添加图片扫描逻辑） =====
@app.route("/products")
def products():
    """
    产品列表页：给每个产品添加自动扫描的图片信息
    """
    # 遍历所有产品，添加扫描后的图片数据
    products_with_images = {}
    for model, product in PRODUCTS.items():
        product_copy = product.copy()
        product_copy["scanned_images"] = scan_product_images(product)  # 新增扫描结果
        products_with_images[model] = product_copy

    return render_template(
        "products/products.html",
        products=products_with_images
    )


@app.route("/products/<model>")
def product_detail(model):
    """
    产品详情页：给产品添加自动扫描的图片信息
    """
    product = PRODUCTS.get(model)
    if not product:
        abort(404)

    # 复制产品字典，添加扫描后的图片数据（避免修改原配置）
    product_with_images = product.copy()
    product_with_images["scanned_images"] = scan_product_images(product)

    return render_template(
        "products/product_detail.html",
        product=product_with_images
    )


@app.route("/blogs")
def blog_list():
    return render_template(
        "blogs/blogs.html",
        blogs=BLOGS
    )


@app.route("/blogs/<slug>")
def blog_detail(slug):
    blog = BLOGS.get(slug)
    if not blog:
        return "Blog not found", 404

    return render_template(
        "blogs/blog_detail.html",
        blog=blog,
        slug=slug
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/oem-custom')
def oemcustom():
    return render_template('oem-custom.html')


if __name__ == '__main__':
    app.run(debug=True)
