import pygit2
import os

print ("Save Game Version Control")

token = 'REMOVED'
auth_method = 'x-access-token'
callbacks = pygit2.RemoteCallbacks(pygit2.UserPass(auth_method, token))
repo_url = "https://github.com/gabrieldnlc/SaveGameVault"
repo_path = os.getcwd() + "\\aaaaa"
repo = pygit2.clone_repository(repo_url, repo_path, callbacks=callbacks)