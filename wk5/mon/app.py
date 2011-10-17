import view

renderer = view.HTMLRenderer()
fl = open(__file__,'r')
renderer.append(['<pre>'])
renderer.append(list(map(lambda x: x[0:-1].replace('&', '&amp;')\
                                          .replace('<','&lt;'),fl)))     
renderer.append(['</pre>'])
renderer.render()
