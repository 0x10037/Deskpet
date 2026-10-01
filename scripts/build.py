#!/usr/bin/env python3
import os
import subprocess
import sys


def run_pyinstaller():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_script = os.path.join(project_root, "src", "deskpet", "main.py")
    resources_dir = os.path.join(project_root, "resources")
    icon_path = os.path.join(resources_dir, "icon.ico")

    # 检查入口文件是否存在
    if not os.path.isfile(main_script):
        print(f"❌ 错误：入口文件不存在: {main_script}", file=sys.stderr)
        sys.exit(1)

    # 检查图标文件是否存在
    if not os.path.isfile(icon_path):
        print(f"❌ 错误：图标文件不存在: {icon_path}", file=sys.stderr)
        sys.exit(1)

    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 单文件可执行
        f"--add-data={resources_dir}{os.pathsep}resources",
        f"--icon={icon_path}",  # 可执行文件图标
        f"--distpath={project_root}/DeskPet_MiTsuHo",
        "--windowed",  # 隐藏控制台
        "--exclude-module=numpy",
        "--exclude-module=PIL",
        "--exclude-module=matplotlib",
        "--exclude-module=cv2",
        "--exclude-module=unittest",
        "--exclude-module=pygame.tests",
        main_script
    ]

    print("🚀 执行 PyInstaller 命令：")
    print(" ".join(cmd))
    print()

    try:
        subprocess.check_call(cmd, cwd=project_root)
        exe_path = os.path.join(project_root, "DeskPet_MiTsuHo/main.exe")
        if os.path.isfile(exe_path):
            print(f"\n✅ 打包成功！可执行文件位于: {exe_path}")
            print("程序已自动运行")
            os.system(exe_path)
        else:
            print("\n⚠️ 打包完成，但未找到 main.exe，请检查是否生成了其他名称。")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败，错误码: {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)


if __name__ == "__main__":
    run_pyinstaller()
