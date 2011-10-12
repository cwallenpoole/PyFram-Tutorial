import view,cgi
renderer = view.HTMLRenderer()
store = cgi.FieldStorage()
first = store.getvalue('fname','')
last = store.getvalue('lname','')
if first or last:
    # start with hello
    l = ["Hello"];
    # if they entered a first name, add it.
    if first: l.append(first)
    # if they entered a last name, add it.
    if last: l.append(last)
    # add an exclamation point to the *last* item in the list
    # (this can be either first or last)
    l[-1]+="!"
    # Send everything to the renderer!
    renderer.append(l)
else:
    renderer.append(['''
<form action="./">
  First name: <input type="text" name="fname" /><br />
  Last name: <input type="text" name="lname" /><br />
  <input type="submit" value="Submit" />
</form>
'''])
renderer.render()