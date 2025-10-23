def generate_report(scan_results):
    """生成代码分析报告"""
    if "error" in scan_results:
        return f"错误: {scan_results['error']}"
    
    report = []
    report.append("=== 代码重构分析报告 ===")
    report.append(f"总问题数: {scan_results['total_issues']}")
    report.append("")
    
    # Python文件分析
    if scan_results['python_files']:
        report.append("--- Python文件分析 ---")
        report.append(f"发现问题的文件数: {len(scan_results['python_files'])}")
        report.append("")
        
        for file_info in scan_results['python_files']:
            report.append(f"文件: {file_info['path']}")
            for issue in file_info['issues']:
                report.append(f"  - 行 {issue.get('line', '?')}: [{issue.get('type', 'unknown')}] {issue.get('message', 'No message')}")
            report.append("")
    
    # JavaScript文件分析
    if scan_results['javascript_files']:
        report.append("--- JavaScript文件分析 ---")
        report.append(f"发现问题的文件数: {len(scan_results['javascript_files'])}")
        report.append("")
        
        for file_info in scan_results['javascript_files']:
            report.append(f"文件: {file_info['path']}")
            for issue in file_info['issues']:
                report.append(f"  - 行 {issue.get('line', '?')}: [{issue.get('type', 'unknown')}] {issue.get('message', 'No message')}")
            report.append("")
    
    # 总结建议
    report.append("--- 重构建议 ---")
    if scan_results['total_issues'] == 0:
        report.append("未发现明显的代码异味，代码质量良好！")
    else:
        report.append("建议优先处理以下问题:")
        report.append("1. 拆分过长的函数，每个函数保持单一职责")
        report.append("2. 移除重复的导入和变量声明")
        report.append("3. 优化复杂的条件逻辑")
    
    return "\n".join(report)