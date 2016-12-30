import settings

def readTraj(m_ID):
	infile = settings.rs_d_file
	pos = []
	type_list = []
	num_atoms = 4*m_ID
	with open(infile,'r') as f:
        	for line in f:
			if '<position num="{0}">'.format(str(num_atoms)) in line.strip():
				break
		for line in f:
			if '</position>' in line.strip():
				break
			templine = line.split()		
			pos.append(templine)	
                for line in f:
                        if '<type num="784">'.format(str(num_atoms)) in line.strip():
                                break
                for line in f:
                        if '</type>' in line.strip():
                                break
                        templine = line.strip()
                        type_list.append(templine)
	f.close()
	all_pos = [[0 for y_t in xrange(4)] for x_t in xrange(len(pos)/4)]
	x = 0
	k=0
	for j in xrange(len(pos)):
		if type_list[j] == '4' or type_list[j] == '5':
			all_pos[k][0] = type_list[j]
			all_pos[k][1] = pos[j][0]
			all_pos[k][2] = pos[j][1]
			all_pos[k][3] = pos[j][2]
			k+=1
			x+=1
	return all_pos

