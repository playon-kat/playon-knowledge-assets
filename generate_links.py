import os
import csv
import subprocess

def get_github_repo_info():
    # Get the remote URL
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("Please make sure to set up the git remote first!")
        return None
    
    remote_url = result.stdout.strip()
    # Convert SSH URL to HTTPS if necessary
    if remote_url.startswith('git@github.com:'):
        remote_url = remote_url.replace('git@github.com:', 'https://github.com/')
    if remote_url.endswith('.git'):
        remote_url = remote_url[:-4]
    return remote_url

def generate_file_links():
    repo_url = get_github_repo_info()
    if not repo_url:
        return
    
    with open('file_links.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Folder', 'Filename', 'Future Public URL'])
        
        # Walk through all directories
        for root, dirs, files in os.walk('.'):
            if '.git' in root:
                continue
                
            for file in files:
                if file.startswith('.') or file == 'generate_links.py' or file == 'file_links.csv':
                    continue
                    
                relative_path = os.path.relpath(os.path.join(root, file))
                folder = os.path.dirname(relative_path)
                if folder == '.':
                    folder = 'root'
                
                # Generate the future public URL
                file_url = f"{repo_url}/blob/main/{relative_path.replace(' ', '%20')}"
                
                writer.writerow([folder, file, file_url])
                print(f"Added: {relative_path}")

if __name__ == "__main__":
    generate_file_links() 