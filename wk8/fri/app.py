import view.html,cgi,os

GUESTBOOK = './guestbook.txt'
if not os.path.exists(GUESTBOOK):
   open(GUESTBOOK,'w+')
renderer = view.html.HTMLRenderer()
store = cgi.FieldStorage()
first = store.getvalue('fname','')
last = store.getvalue('lname','')
final = []
if first and last:
   import datetime
   dt = datetime.datetime.today()
   fl = open(GUESTBOOK,'a+')
   fl.write( str( view.html.HTMLCleaner(feed = "{first} {last}\t{month}/{day}/{year}"
		" {hour:02d}:{min:02d}:{sec:02d}\n".format(last=last,first=first,
                   day=dt.day,month=dt.month,year=dt.year,
                   hour=dt.hour, min=dt.minute, sec=dt.second)))+"\n")
   fl.flush()
   fl.close()
   del fl 
else:
    final += ['''
<form action="" method="GET">
  First name: <input type="text" name="fname" value="''',first,'''" /><br />
  Last name: <input type="text" name="lname" value="''',last,'''"/><br />
  <input type="submit" value="Submit" />
</form>
''']

try:
    fl = open(GUESTBOOK,'r')
    renderer.append(list(map(lambda x: x[0:-1]+'<br />',fl)))
except Exception as e:
    renderer.append([e])
renderer.append(final)
renderer.render()
