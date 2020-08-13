import dropbox

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx_auth = dropbox.Dropbox(dbxtoken)
dbx_auth.users_get_current_account()