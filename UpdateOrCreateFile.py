from github import Github

def get_blob_content(repo, branch, path_name):
	# first get the branch reference
	ref = repo.get_git_ref(f'heads/{branch}')
	# then get the tree
	tree = repo.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
	# look for path in tree
	sha = [x.sha for x in tree if x.path == path_name]
	if not sha:
		# well, not found..
		return None
	# we have sha
	return repo.get_git_blob(sha[0])

def update_Data():
	g = Github("itracanalise","")

	user = g.get_user()
	repo = g.get_repo("itracanalise/analiseComentarios")

	all_files = []

	contents = repo.get_contents("")

	while contents:
		file_content = contents.pop(0)
		if file_content.type == "dir":
			contents.extend(repo.get_contents(file_content.path))
		else:
			file = file_content
			all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
		print(all_files[-1])
	with open('General_Data.csv', 'r') as file:
		content = file.read()

	# Upload to github

	git_file = 'General_Data.csv'


	if git_file in all_files:
		print("at update")
		Glob = get_blob_content(repo, 'main', git_file)
		repo.update_file(git_file, "committing files", content,Glob.sha, branch="main")
		print(git_file + ' UPDATED')
	else:
		repo.create_file(git_file, "committing files", content, branch="main")
		print(git_file + ' CREATED')