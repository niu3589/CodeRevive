import ast
import os

def detect_code_smells(file_path):
    """检测Python代码中的代码异味"""
    issues = []
    
    if not os.path.exists(file_path):
        return [{"type": "error", "message": f"文件不存在: {file_path}", "line": 0}]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 解析AST
        tree = ast.parse(code)
        
        # 1. 检测长函数
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lines = len(ast.get_source_segment(code, node).split('\n')) if ast.get_source_segment(code, node) else 0
                if lines > 30:
                    issues.append({
                        "type": "long_function",
                        "message": f"函数 '{node.name}' 过长 ({lines} 行)",
                        "line": node.lineno,
                        "function": node.name
                    })
        
        # 2. 检测重复导入
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in imports:
                        issues.append({
                            "type": "duplicate_import",
                            "message": f"重复导入: {alias.name}",
                            "line": node.lineno,
                            "import": alias.name
                        })
                    imports[alias.name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for alias in node.names:
                    full_name = f"{module}.{alias.name}"
                    if full_name in imports:
                        issues.append({
                            "type": "duplicate_import",
                            "message": f"重复导入: {full_name}",
                            "line": node.lineno,
                            "import": full_name
                        })
                    imports[full_name] = node.lineno
        
    except Exception as e:
        issues.append({"type": "error", "message": f"分析失败: {str(e)}", "line": 0})
    
    return issues

def analyze_complexity(file_path):
    """分析代码复杂度"""
    if not os.path.exists(file_path):
        return {"error": "文件不存在"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        
        # 计算圈复杂度
        def calculate_cyclomatic_complexity(node):
            complexity = 1  # 基础复杂度为1
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.AsyncFor, 
                                      ast.With, ast.AsyncWith, ast.Try, ast.ExceptHandler, 
                                      ast.BoolOp, ast.BinOp)):
                    complexity += 1
                complexity += calculate_cyclomatic_complexity(child)
            
            return complexity
        
        cyclomatic_complexity = calculate_cyclomatic_complexity(tree)
        
        # 简单的可维护性指数计算
        lines_of_code = len(code.split('\n'))
        maintainability_index = max(0, 100 - (cyclomatic_complexity * 2 + lines_of_code * 0.1))
        
        return {
            "cyclomatic_complexity": cyclomatic_complexity,
            "maintainability_index": round(maintainability_index, 2),
            "lines_of_code": lines_of_code
        }
    
    except Exception as e:
        return {"error": str(e)}