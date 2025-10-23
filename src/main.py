import argparse
import os
from analyzers import detect_python_smells, detect_javascript_smells, analyze_python_complexity, analyze_javascript_complexity
from refactors import refactor_python_long_methods, optimize_python_imports, refactor_javascript_long_methods, optimize_javascript_variables
from integrations.github_integration import connect_to_repo, create_pull_request
from core.scanner import scan_repository
from core.report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description='代码库静默持续重构服务 - MVP版')
    parser.add_argument('--repo', type=str, required=True, help='仓库URL或本地路径')
    parser.add_argument('--token', type=str, help='GitHub访问令牌（如果是GitHub仓库）')
    parser.add_argument('--analyze-only', action='store_true', help='仅分析不重构')
    parser.add_argument('--file', type=str, help='分析单个文件（可选）')
    args = parser.parse_args()
    
    print("===== 代码重构服务启动 =====")
    
    # 1. 处理单个文件分析
    if args.file:
        print(f"\n分析文件: {args.file}")
        
        if args.file.endswith('.py'):
            issues = detect_python_smells(args.file)
            complexity = analyze_python_complexity(args.file)
            
            print(f"\n代码异味: {len(issues)} 个")
            for issue in issues:
                print(f"  - 行 {issue.get('line', '?')}: [{issue.get('type', 'unknown')}] {issue.get('message')}")
            
            print(f"\n复杂度分析:")
            print(f"  - 圈复杂度: {complexity.get('cyclomatic_complexity')}")
            print(f"  - 可维护性指数: {complexity.get('maintainability_index')}")
            print(f"  - 代码行数: {complexity.get('lines_of_code')}")
            
            if not args.analyze_only:
                print("\n执行重构...")
                refactor_result = refactor_python_long_methods(args.file)
                print(f"长方法重构: {refactor_result['message']}")
                
                optimize_result = optimize_python_imports(args.file)
                print(f"导入优化: {optimize_result['message']}")
        
        elif args.file.endswith('.js'):
            issues = detect_javascript_smells(args.file)
            complexity = analyze_javascript_complexity(args.file)
            
            print(f"\n代码异味: {len(issues)} 个")
            for issue in issues:
                print(f"  - 行 {issue.get('line', '?')}: [{issue.get('type', 'unknown')}] {issue.get('message')}")
            
            print(f"\n复杂度分析:")
            print(f"  - 圈复杂度: {complexity.get('cyclomatic_complexity')}")
            print(f"  - 可维护性指数: {complexity.get('maintainability_index')}")
            print(f"  - 代码行数: {complexity.get('lines_of_code')}")
            
            if not args.analyze_only:
                print("\n执行重构...")
                refactor_result = refactor_javascript_long_methods(args.file)
                print(f"长方法重构: {refactor_result['message']}")
                
                optimize_result = optimize_javascript_variables(args.file)
                print(f"变量优化: {optimize_result['message']}")
        
        else:
            print("不支持的文件类型，仅支持 .py 和 .js 文件")
        
        return
    
    # 2. 处理仓库分析
    if args.repo.startswith(('http://', 'https://')):
        # GitHub仓库
        if not args.token:
            print("错误: 分析GitHub仓库需要提供访问令牌 (--token)")
            return
        
        print(f"\n连接到GitHub仓库: {args.repo}")
        repo_info = connect_to_repo(args.repo, args.token)
        
        if repo_info['status'] != 'connected':
            print(f"错误: {repo_info['message']}")
            return
        
        print(f"成功连接到仓库: {repo_info['repo_info']['full_name']}")
    
    # 扫描仓库
    print("\n开始扫描仓库...")
    scan_results = scan_repository(args.repo)
    
    # 生成分析报告
    report = generate_report(scan_results)
    print(f"\n{report}")
    
    # 保存报告到文件
    report_file = "code_refactor_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {os.path.abspath(report_file)}")
    
    # 执行重构
    if not args.analyze_only:
        print("\n执行重构操作...")
        # 在MVP阶段，我们只是模拟重构操作
        changes = []
        
        # 收集所有需要重构的文件
        for file_info in scan_results.get('python_files', []):
            changes.append({"file": file_info['path'], "issues": len(file_info['issues'])})
        
        for file_info in scan_results.get('javascript_files', []):
            changes.append({"file": file_info['path'], "issues": len(file_info['issues'])})
        
        print(f"发现 {len(changes)} 个文件需要重构")
        
        # 如果是GitHub仓库，创建PR
        if args.repo.startswith(('http://', 'https://')):
            pr_result = create_pull_request(
                args.repo, 
                args.token, 
                changes, 
                "代码自动重构建议", 
                "基于代码质量分析的自动重构建议\n\n请查看附件报告获取详细信息。"
            )
            
            if pr_result['status'] == 'created':
                print(f"\n✅ 拉取请求已创建")
                print(f"📋 PR URL: {pr_result['pr_url']}")
                print(f"🔍 包含 {pr_result['changes_count']} 个文件的重构建议")
            else:
                print(f"\n❌ 创建PR失败: {pr_result['message']}")
    
    print("\n===== 分析完成 =====")

if __name__ == "__main__":
    main()