# data/blogs.py
BLOGS = [
    {
        "id": 1,
        "slug": "magsafe-wireless-charger-guide",
        "title": "2026 MagSafe无线充电器选购指南：避坑+高性价比推荐",
        "description": "2026最新MagSafe无线充电器选购指南，涵盖兼容机型、快充功率、品牌推荐，帮你选到适合iPhone15/14的无线充！",
        "keywords": "MagSafe无线充电器选购,2026 MagSafe快充,iPhone无线充推荐",
        "blog_img_folder": "blog_magsafe_guide",  # 新增：单篇Blog专属图片文件夹（语义化命名，比blog1好记）
        "content_blocks": [
            {
                "type": "title2",
                "content": "一、MagSafe无线充兼容哪些iPhone机型？"
            },
            {
                "type": "paragraph",
                "content": "MagSafe无线充主要兼容iPhone12及以上机型，包括iPhone12/13/14/15系列，其中iPhone15 Pro支持最高15W快充。"
            },
            {
                "type": "paragraph",
                "content": "我们的{H301}完美兼容所有支持MagSafe的iPhone机型，快充效率提升30%。",
                "product_links": {"H301": "h301"}
            },
            {
                "type": "title2",
                "content": "二、MagSafe无线充快充功率怎么选？"
            },
            {
                "type": "paragraph",
                "content": "目前主流MagSafe无线充的快充功率为15W，低于15W的充电速度较慢，不建议选择。"
            },
            {
                "type": "image",
                "src": "magsafe-fast-charge.webp",  # 仅填文件名，路径自动拼接：images/blog_magsafe_guide/xxx.webp
                "alt": "H301 MagSafe无线充电器快充效果"
            },
            {
                "type": "image",
                "src": "magsafe-compatible-models.webp",
                "alt": "MagSafe无线充兼容机型展示"
            }
        ],
        "publish_time": "2026-01-30",
        "priority": 0.8
    },
    {
        "id": 2,
        "slug": "how-to-extend-iphone-battery-life",
        "title": "2026 iPhone电池寿命延长技巧：5个实用方法",
        "description": "2026最新iPhone电池寿命延长技巧，涵盖充电习惯、设置优化、配件选择，让你的iPhone电池更耐用！",
        "keywords": "iPhone电池寿命延长,2026 iPhone充电技巧,iPhone配件推荐",
        "blog_img_folder": "blog_battery_life",  # 第二篇Blog专属图片文件夹
        "content_blocks": [
            {
                "type": "title2",
                "content": "一、避免过度充电和过度放电"
            },
            {
                "type": "paragraph",
                "content": "iPhone电池的最佳电量范围是20%-80%，避免将电池充满到100%或放电到0%。"
            },
            {
                "type": "paragraph",
                "content": "使用{H301}可以实现智能停充，有效保护电池寿命。",
                "product_links": {"H301": "h301"}
            },
            {
                "type": "image",
                "src": "battery-protection.webp",  # 路径自动拼接：images/blog_battery_life/xxx.webp
                "alt": "H301智能停充保护电池演示"
            }
        ],
        "publish_time": "2026-02-01",
        "update_time": "2026-02-06",
        "priority": 0.7
    }
]
