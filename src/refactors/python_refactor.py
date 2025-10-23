import ast
import os

def refactor_long_methods(file_path, max_lines=30):
    """重构长方法，将其拆分为更小的方法（简化版）"""
    if not os.path.exists(file_path):
        return {"status": "error", "message": "文件不存在"}
    
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        
        # 检测长方法并提供重构建议
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_code = ast.get_source_segment(code, node)
                if function_code:
                    lines = function_code.split('\n')
                    if len(lines) > max_lines:
                        changes.append({
                            "type": "refactor_long_method",
                            "function_name": node.name,
                            "line": node.lineno,
                            "suggestion": f"将函数 '{node.name}' 拆分为更小的辅助函数",
                            "current_lines": len(lines),
                            "max_allowed": max_lines
                        })
        
        return {
            "status": "success",
            "message": f"发现 {len(changes)} 个需要重构的长方法",
            "changes": changes
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def optimize_imports(file_path):
    """优化Python文件中的导入语句"""
    if not os.path.exists(file_path):
        return {"status": "error", "message": "文件不存在"}
    
    changes = []
    new_code = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 收集所有导入语句
        imports = {}
        import_lines = []
        non_import_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            # 跳过空行和注释
            if not stripped or stripped.startswith('#'):
                non_import_lines.append((i, line))
                continue
            
            # 检测导入语句
            if stripped.startswith(('import ', 'from ')):
                import_lines.append((i, line))
                # 简化处理：检测重复导入
                import_key = stripped.split(' ')[1].split('.')[0]
                if import_key in imports:
                    changes.append({
                        "type": "remove_duplicate_import",
                        "line": i + 1,
                        "import": import_key,
                        "message": f"移除重复导入 '{import_key}'"
                    })
                else:
                    imports[import_key] = i
            else:
                non_import_lines.append((i, line))
        
        # 生成优化后的代码
        # 保留唯一的导入语句
        seen_imports = set()
        for i, line in import_lines:
            import_key = line.strip().split(' ')[1].split('.')[0]
            if import_key not in seen_imports:
                new_code.append(line)
                seen_imports.add(import_key)
        
        # 添加其他代码行
        if new_code and non_import_lines:
            new_code.append('\n')  # 添加空行分隔导入和代码
        
        for i, line in non_import_lines:
            new_code.append(line)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_code)
        
        return {
            "status": "success",
            "message": f"成功优化 {len(changes)} 处导入语句",
            "changes": changes
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}