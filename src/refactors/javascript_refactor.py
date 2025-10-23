import os
import re

def refactor_long_methods(file_path, max_lines=30):
    """重构JavaScript中的长方法"""
    if not os.path.exists(file_path):
        return {"status": "error", "message": "文件不存在"}
    
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 检测长函数并提供重构建议
        function_pattern = re.compile(r'(function\s+([\w$]+)\s*\([^)]*\)\s*{)|(const|let|var)\s+([\w$]+)\s*=\s*\([^)]*\)\s*=>\s*{')
        
        for match in function_pattern.finditer(code):
            if match.group(2):  # 普通函数
                function_name = match.group(2)
            else:  # 箭头函数
                function_name = match.group(4)
            
            start_pos = match.end()
            brace_count = 1
            end_pos = start_pos
            
            while end_pos < len(code) and brace_count > 0:
                if code[end_pos] == '{':
                    brace_count += 1
                elif code[end_pos] == '}':
                    brace_count -= 1
                end_pos += 1
            
            function_lines = code[match.start():end_pos].split('\n')
            if len(function_lines) > max_lines:
                line_num = code[:match.start()].count('\n') + 1
                changes.append({
                    "type": "refactor_long_method",
                    "function_name": function_name,
                    "line": line_num,
                    "suggestion": f"将函数 '{function_name}' 拆分为更小的辅助函数",
                    "current_lines": len(function_lines),
                    "max_allowed": max_lines
                })
        
        return {
            "status": "success",
            "message": f"发现 {len(changes)} 个需要重构的长方法",
            "changes": changes
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def optimize_variables(file_path):
    """优化JavaScript变量声明"""
    if not os.path.exists(file_path):
        return {"status": "error", "message": "文件不存在"}
    
    changes = []
    new_lines = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 检测并移除重复变量声明
        declared_vars = {}
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            var_match = re.search(r'(var|let|const)\s+([\w$]+)', stripped)
            
            if var_match and not stripped.startswith('//'):
                var_type = var_match.group(1)
                var_name = var_match.group(2)
                
                if var_name in declared_vars:
                    # 这是一个重复声明
                    changes.append({
                        "type": "remove_duplicate_variable",
                        "line": i + 1,
                        "variable": var_name,
                        "message": f"移除重复声明的变量 '{var_name}'"
                    })
                    # 只保留第一次声明
                    continue
                
                declared_vars[var_name] = i
            
            new_lines.append(line)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return {
            "status": "success",
            "message": f"成功优化 {len(changes)} 个变量声明",
            "changes": changes
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}