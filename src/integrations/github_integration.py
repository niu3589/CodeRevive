import requests

def connect_to_repo(repo_url, access_token):
    """连接到GitHub仓库"""
    try:
        # 从URL中提取所有者和仓库名
        if 'github.com/' in repo_url:
            parts = repo_url.split('github.com/')[1]
            if '/' in parts:
                owner, repo = parts.split('/', 1)
                repo = repo.replace('.git', '')
            else:
                return {"status": "error", "message": "无效的仓库URL格式"}
        else:
            return {"status": "error", "message": "不支持的仓库URL格式"}
        
        # 调用GitHub API检查仓库
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        api_url = f'https://api.github.com/repos/{owner}/{repo}'
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            repo_info = response.json()
            return {
                "status": "connected",
                "repo_info": {
                    "owner": owner,
                    "name": repo,
                    "full_name": repo_info.get('full_name'),
                    "description": repo_info.get('description')
                }
            }
        else:
            return {
                "status": "error",
                "message": f"连接失败: {response.status_code} - {response.json().get('message', 'Unknown error')}"
            }
    
    except Exception as e:
        return {"status": "error", "message": f"连接失败: {str(e)}"}

def create_pull_request(repo_url, access_token, changes, title, description):
    """创建GitHub拉取请求提交重构建议"""
    try:
        # 解析仓库信息
        if 'github.com/' in repo_url:
            parts = repo_url.split('github.com/')[1]
            if '/' in parts:
                owner, repo = parts.split('/', 1)
                repo = repo.replace('.git', '')
            else:
                return {"status": "error", "message": "无效的仓库URL格式"}
        else:
            return {"status": "error", "message": "不支持的仓库URL格式"}
        
        # 在实际应用中，这里需要：
        # 1. Fork仓库
        # 2. Clone到本地
        # 3. 应用更改
        # 4. Push到fork的仓库
        # 5. 创建PR
        
        # MVP阶段：我们只是模拟这个过程
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # 模拟PR创建
        # 注意：在实际实现中，需要先push更改到分支
        pr_data = {
            "title": title,
            "body": description,
            "head": "refactor-branch",  # 实际应用中应该是包含更改的分支
            "base": "main"  # 目标分支
        }
        
        # 这里只是返回模拟结果，实际应用中需要调用GitHub API
        pr_url = f"https://github.com/{owner}/{repo}/pull/new/refactor-branch"
        
        return {
            "status": "created",
            "pr_url": pr_url,
            "message": f"拉取请求已创建: {title}",
            "changes_count": len(changes)
        }
    
    except Exception as e:
        return {"status": "error", "message": f"创建PR失败: {str(e)}"}