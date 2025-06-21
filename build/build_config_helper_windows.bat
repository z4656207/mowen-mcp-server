@echo off
REM 配置助手 Windows 构建脚本

REM 设置控制台编码为UTF-8，避免中文乱码
chcp 65001 >nul

echo Windows 构建配置助手版本...
echo ================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Python未安装或不在PATH中
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo 成功: Python环境检查通过

REM 检查PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo 错误: PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo 成功: PyInstaller准备就绪

REM 清理旧的构建文件
if exist "dist\配置助手.exe" del "dist\配置助手.exe"
if exist "build\配置助手" rmdir /s /q "build\配置助手"

REM 开始构建 - 使用UTF-8编码的spec文件
echo 开始打包配置助手...
if exist "配置助手.spec" (
    echo 使用现有spec文件构建...
    pyinstaller --clean --noconfirm "配置助手.spec"
) else (
    echo 使用默认参数构建...
    pyinstaller --onefile --windowed --name "配置助手" --clean --noconfirm --hidden-import=encodings.utf_8 --hidden-import=encodings.gbk --hidden-import=tkinter --hidden-import=tkinter.messagebox --hidden-import=tkinter.simpledialog --hidden-import=tkinter.scrolledtext config_helper.py
)

REM 检查构建结果
echo.
echo 检查构建结果...

REM 等待一下，确保文件写入完成
timeout /t 2 /nobreak >nul

REM 检查可能的输出文件位置
set "exe_found=0"
if exist "dist\配置助手.exe" (
    set "exe_path=dist\配置助手.exe"
    set "exe_found=1"
) else if exist "dist\配置助手" (
    set "exe_path=dist\配置助手"
    set "exe_found=1"
)

if "%exe_found%"=="1" (
    echo 成功: 配置助手构建成功！
    echo 输出文件位置: dist目录
    echo 文件大小: 
    for %%A in ("%exe_path%") do echo    %%~zA 字节
    
    REM 等待确保没有进程占用文件
    echo.
    echo 等待文件释放...
    timeout /t 3 /nobreak >nul
    
    REM 强制结束可能的配置助手进程
    taskkill /f /im "配置助手.exe" >nul 2>&1
    
    REM 再等待一下
    timeout /t 1 /nobreak >nul
    
    REM 拷贝到发布目录
    echo.
    echo 拷贝到发布目录...
    
    REM 确保发布目录存在
    if not exist "..\release\windows-release\user-version" (
        echo 创建发布目录...
        mkdir "..\release\windows-release\user-version" 2>nul
    )
    
    REM 检查源文件是否存在且可访问
    if exist "%exe_path%" (
        echo 源文件确认存在: %exe_path%
        
        REM 尝试拷贝配置助手到发布目录
        copy "%exe_path%" "..\release\windows-release\user-version\配置助手.exe"
        if errorlevel 1 (
            echo 错误: 拷贝到发布目录失败
            echo 可能原因: 文件被占用或权限不足
            echo 请手动拷贝文件
        ) else (
            echo 成功: 已拷贝到发布目录
            
            REM 验证拷贝结果
            if exist "..\release\windows-release\user-version\配置助手.exe" (
                echo 验证: 目标文件存在
                for %%B in ("..\release\windows-release\user-version\配置助手.exe") do echo 目标文件大小: %%~zB 字节
            ) else (
                echo 警告: 目标文件不存在，拷贝可能失败
            )
        )
    ) else (
        echo 错误: 源文件不存在或无法访问
    )
    
    echo.
    echo 使用说明:
    echo    1. 双击运行配置助手程序
    echo    2. 输入墨问API密钥
    echo    3. 点击"生成配置"按钮
    echo    4. 复制生成的配置到Cursor等客户端
    echo.
    echo 构建完成！
) else (
    echo 错误: 构建失败，未找到输出文件
    echo 检查的位置:
    echo    - dist\配置助手.exe
    echo    - dist\配置助手
    echo.
    echo 当前dist目录内容:
    if exist "dist" (
        dir /b "dist"
    ) else (
        echo    dist目录不存在
    )
    echo.
    echo 请检查上面的错误信息
    pause
    exit /b 1
)

pause