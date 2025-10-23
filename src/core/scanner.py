import os
from analyzers import detect_python_smells, detect_javascript_smells

def scan_repository(repo_path):
    """扫描仓库中的所有代码文件"""
    results = {
        "python_files": [],
        "javascript_files": [],
        "total_issues": 0
    }
    
    # 如果是GitHub URL，MVP阶段我们只做简单处理
    if repo_path.startswith(('http://', 'https://')):
        # 在实际应用中，这里应该克隆仓库到本地
        print(f"注意：在实际应用中，应该克隆仓库: {repo_path}")
        # 返回模拟数据用于演示
        return {
            "python_files": [
                {
                    "path": "example.py",
                    "issues": [
                        {"type": "long_function", "message": "示例长函数", "line": 10}
                    ]
                }
            ],
            "javascript_files": [
                {
                    "path": "example.js",
                    "issues": [
                        {"type": "long_function", "message": "示例JavaScript长函数", "line": 15}
                    ]
                }
            ],
            "total_issues": 2
        }
    
    # 扫描本地目录
    if not os.path.exists(repo_path):
        return {"error": "仓库路径不存在"}
    
    for root, dirs, files in os.walk(repo_path):
        # 跳过隐藏目录和venv等
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
        
        for file in files:
            file_path = os.path.join(root, file)
            
            if file.endswith('.py'):
                issues = detect_python_smells(file_path)
                if issues:
                    results["python_files"].append({
                        "path": file_path,
                        "issues": issues
                    })
                    results["total_issues"] += len(issues)
            
            elif file.endswith('.js'):
                issues = detect_javascript_smells(file_path)
                if issues:
                    results["javascript_files"].append({
                        "path": file_path,
                        "issues": issues
                    })
                    results["total_issues"] += len(issues)
    
    return results