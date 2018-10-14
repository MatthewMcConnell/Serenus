def listscale(alist):
	tmp = []
	mi = min(alist)
	ma = max(alist)
	for entry in alist:
		tmp.append(scale(entry, mi, ma))
	return tmp

def scale(value, min, max):
	return (value - min) / (max - min)

def rgbify(value):
	if (value < 0.33):
		return [scale(entry, 0, 0.33), 1, 0]
	elif (value >= 0.33 and value < 0.66):
		return [1, 1, scale(value, 0.33, 0.67)]
	else:
		return [1, 1 - scale(value, 0.67, 1)]

def rgbscale(alist):
	print(alist)
	tmp = []
	mi = min(alist)
	ma = max(alist)
	for entry in alist:
		if entry < 0.30:
			tmp.append([0,1,0])
		elif (entry >= 0.30 and entry < 0.60):
			tmp.append(rgbify(scale(entry, mi, ma)))
		else:
			tmp.append([1,1,0])
	return tmp

