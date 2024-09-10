#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   build.py
@Time    :   2024/07/05 11:19:32
@Author  :   KmBase
@Version :   1.0
@License :   (C)Copyright 2022, KmBase
@Desc    :   使用前需要先安装InnoSetup,应用更新时请不要修改app_id,password自行修改
"""
import shutil
import subprocess
import os, sys
from pathlib import Path
import uuid
from src.app import AppConfig


def generate_new_id(mode):
    if mode:
        print(str(uuid.uuid4()).upper())
    else:
        return "D78D1C24-34B0-437F-BDEB-F1815B5D56D4"


iss_compiler = "D:\\Program Files (x86)\\Inno Setup 6\\Compil32.exe"
# subprocess.call(['pip', 'install', '-U', 'nuitka'])
# subprocess.call(['pip', 'install', '-r', 'requirements.txt'])


class PerfectBuild:
    def __init__(self, app_id, mode="--e"):
        """
        初始化变量
        """
        self.app_id = app_id
        self.mode = mode.replace("--", "")
        self.dist = f"{AppConfig.app_exec}.dist"
        self.build_dir = Path.joinpath(Path(AppConfig.app_home), "build")
        if not self.build_dir.exists():
            self.build_dir.mkdir()
        self.release_dir = Path.joinpath(
            Path(AppConfig.app_home), "release", f"{AppConfig.app_ver}{self.mode}"
        )
        if not self.release_dir.exists():
            if not self.release_dir.parent.exists():
                self.release_dir.parent.mkdir()
            self.release_dir.mkdir()

    def ebuild(self, password):
        """
        embedded build
        """
        output_dir = Path.joinpath(
            Path(AppConfig.app_home), "build", f"{AppConfig.system}-{AppConfig.arch}"
        )
        embedded_dir = Path.joinpath(Path(AppConfig.app_home), "embedded")
        # ## 7zip部分
        import py7zr

        # 要压缩的文件或文件夹路径
        source_path = f"{AppConfig.app_home}\\src\\app.py"
        # 压缩后的7z文件名
        archive_name = f"{AppConfig.app_home}\\embedded\\src\\.app.egg"
        # 设置密码
        # 创建压缩文件并设置密码
        with py7zr.SevenZipFile(archive_name, "w", password=password) as archive:
            archive.writeall(source_path)
        print(f"Archive {archive_name} created with password.")
        for module in [f"{AppConfig.app_home.__str__()}\\src\\entry.py",f"{AppConfig.app_home.__str__()}\\src\\app.py"]:
            ## Nuitka部分
            cmd_args = [
                "nuitka",
                "--module",
                "--remove-output",
                "--no-pyi-file",
                f"{module}",
                f"--output-dir={embedded_dir.__str__()}\\src",
            ]
            process = subprocess.run(cmd_args, shell=True)
            if process.returncode != 0:
                raise ChildProcessError("Module building failed.")
        ## 复制到build
        self.copy_directory(embedded_dir, Path.joinpath(output_dir, "embedded"))
        self.dist = "embedded"
        print("Embedded Building done.")

    def copy_directory(self, src: Path, dest: Path):
        if dest.exists():
            shutil.rmtree(dest)
        try:
            dest.mkdir(parents=True)
            for item in src.iterdir():
                if item.is_dir():
                    shutil.copytree(item, dest / item.name)
                else:
                    shutil.copy2(item, dest / item.name)
            return "文件夹复制成功"
        except Exception as e:
            return f"复制文件夹时发生错误: {e}"

    def update_iss(self):
        settings = {
            "AppId": self.app_id,
            "AppName": AppConfig.app_name,
            "AppVersion": AppConfig.app_ver,
            "AppMode": self.mode,
            "System": AppConfig.system,
            "Arch": AppConfig.arch,
            "AppPublisher": AppConfig.app_publisher,
            "AppURL": AppConfig.app_url,
            "AppIcon": AppConfig.app_icon,
            "AppExeName": AppConfig.app_exec + ".exe",
            "ProjectDir": str(AppConfig.app_home),
            "BuildDir": str(self.build_dir),
            "ReleaseDir": str(self.release_dir),
            "Dist": str(self.dist),
            "ARCH_MODE": (
                "ArchitecturesInstallIn64BitMode=x64" if AppConfig.arch == "64" else ""
            ),
        }

        iss_template = f"setup-template.iss"
        iss_work = Path.joinpath(
            self.build_dir, f"{AppConfig.app_name}-{AppConfig.arch}-{self.mode}.iss"
        )
        with open(iss_template) as template:
            iss_script = template.read()

        for key in settings:
            iss_script = iss_script.replace(f"%%{key}%%", settings.get(key))

        with open(iss_work, "w") as iss:
            iss.write(iss_script)
        return iss_work

    def create_setup(self):
        iss_work = self.update_iss()
        if Path(iss_compiler).exists:
            print("Creating Windows Installer...", end="")
            compiler_cmd = [str(iss_compiler), "/cc", str(iss_work)]
            process = subprocess.run(compiler_cmd)
            if process.returncode != 0:
                raise ChildProcessError("Creating Windows installer failed.")
            print("done")


def main(args):
    """
    :param args:
        --g:Generate new id
        --p:Pyinstaller building
    :return:
    """
    app_path = os.path.abspath(__file__)
    AppConfig.initialize(app_path)
    if len(args) < 2:
        mode = "--e"
    else:
        mode = args[1]
        if mode == "--g":
            generate_new_id(True)
            return
    password = str(input("请输入加密密码:"))
    app_id = generate_new_id(False)
    pb = PerfectBuild(app_id, mode)
    pb.ebuild(password)
    pb.dist = "embedded"
    # if AppConfig.system == "Windows":
    #     pb.create_setup()


if __name__ == "__main__":
    main(sys.argv)
