def scale(alist):
	tmp = []
	mi = min(alist)
	ma = max(alist)
	for entry in alist:
		tmp.append((entry - mi)/ (ma - mi))
	return tmp
