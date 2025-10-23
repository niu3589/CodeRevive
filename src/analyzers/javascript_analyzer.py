import os
import re

def detect_code_smells(file_path):
    """检测JavaScript代码中的代码异味"""
    issues = []
    
    if not os.path.exists(file_path):
        return [{"type": "error", "message": f"文件不存在: {file_path}", "line": 0}]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            code = ''.join(lines)
        
        # 1. 检测长函数
        function_pattern = re.compile(r'function\s+([\w$]+)\s*\([^)]*\)\s*{')
        for match in function_pattern.finditer(code):
            function_name = match.group(1)
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
            if len(function_lines) > 30:
                # 找出函数所在的行号
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    "type": "long_function",
                    "message": f"函数 '{function_name}' 过长 ({len(function_lines)} 行)",
                    "line": line_num,
                    "function": function_name
                })
        
        # 2. 检测重复变量声明
        var_declarations = {}
        var_pattern = re.compile(r'(var|let|const)\s+([\w$]+)\s*=?')
        for i, line in enumerate(lines, 1):
            for match in var_pattern.finditer(line):
                var_name = match.group(2)
                if var_name in var_declarations:
                    issues.append({
                        "type": "duplicate_variable",
                        "message": f"重复声明变量: {var_name}",
                        "line": i,
                        "previous_line": var_declarations[var_name]
                    })
                var_declarations[var_name] = i
        
    except Exception as e:
        issues.append({"type": "error", "message": f"分析失败: {str(e)}", "line": 0})
    
    return issues

def analyze_complexity(file_path):
    """分析JavaScript代码复杂度"""
    if not os.path.exists(file_path):
        return {"error": "文件不存在"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            lines = code.split('\n')
        
        # 计算圈复杂度（简化版）
        complexity = 1  # 基础复杂度
        complexity_keywords = ['if', 'for', 'while', 'case', 'catch', '&&', '||']
        
        for line in lines:
            stripped_line = line.strip()
            # 跳过注释和空行
            if stripped_line.startswith('//') or stripped_line.startswith('/*') or not stripped_line:
                continue
            
            for keyword in complexity_keywords:
                # 避免在字符串中计算
                if keyword in stripped_line and not ("'" in stripped_line and stripped_line.index(keyword) > stripped_line.index("'")):
                    complexity += 1
        
        lines_of_code = len(lines)
        maintainability_index = max(0, 100 - (complexity * 2 + lines_of_code * 0.1))
        
        return {
            "cyclomatic_complexity": complexity,
            "maintainability_index": round(maintainability_index, 2),
            "lines_of_code": lines_of_code
        }
    
    except Exception as e:
        return {"error": str(e)}