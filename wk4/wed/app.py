import view,cgi,urllib
renderer = view.HTMLRenderer()
store = cgi.FieldStorage()
first = store.getvalue('fname','')
last = store.getvalue('lname','')
id = store.getvalue('id','').strip()
if first or last:
    text = ["Hello"];
    if first: text.append(first)
    if last: text.append(last)
    text[-1]+="!"
    text.append("Your ID is " + id)
    text.append(urllib.parse.parse_qsl('?bar=&foo=&foo=0&foo=1', True))
    renderer.append(text)
else:
    renderer.append(['''
<form action="./?id='''+id+'''" method="POST">
  First name: <input type="text" name="fname" /><br />
  Last name: <input type="text" name="lname" /><br />
  <input type="submit" value="Submit" />
</form>
'''])
renderer.render()
