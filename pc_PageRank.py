import numpy as np
import csv

if __name__ == '__main__':

	# 读入有向图，存储边
	f = open('follower_4.csv', 'r')
	edges = [line.strip('\n').split(',') for line in f]
	print(len(edges))
	f.close()

	# 根据边获取节点的集合
	count=0
	print('开始存储node_to_num_1.csv')
	f1 = open('node_to num_1.csv', 'a', newline='', encoding="utf-8")
	csv_write = csv.writer(f1)
	nodes = []
	for edge in edges:
		if edge[0] not in nodes:
			nodes.append(edge[0])
			csv_write.writerow([count, edge[0]])
			print([count, edge[0]])
			count+=1
		if edge[1] not in nodes:
			nodes.append(edge[1])
			csv_write.writerow([count, edge[1]])
			print([count, edge[1]])
			count += 1
	f1.close()
	print('node_to_num_1.csv存储完成')
	print('node长度：')
	print(len(nodes))


	N = len(nodes)
	print(N)
	# 将节点符号（字母），映射成阿拉伯数字，便于后面生成A矩阵/S矩阵
	i = 0
	node_to_num = {}
	for node in nodes:
		node_to_num[node] = i
		i += 1
	for edge in edges:
		edge[0] = node_to_num[edge[0]]
		edge[1] = node_to_num[edge[1]]
	print(edges)


	# 生成初步的S矩阵
	S = np.zeros([N, N])
	for edge in edges:
		S[edge[1], edge[0]] = 1
	print(S)

	# 计算比例：即一个网页对其他网页的PageRank值的贡献，即进行列的归一化处理
	for j in range(N):
		sum_of_col = sum(S[:, j])
		for i in range(N):
			if sum_of_col!=0:
			    S[i, j] /= sum_of_col
			else:
				S[i, j]=1/N
	print(S)

	# 计算矩阵A
	alpha = 0.85
	A = alpha * S + (1 - alpha) / N * np.ones([N, N])
	print(A)

	# 生成初始的PageRank值，记录在P_n中，P_n和P_n1均用于迭代
	P_n = np.ones(N) / N
	P_n1 = np.zeros(N)

	e = 100000  # 误差初始化
	k = 0  # 记录迭代次数
	print('loop...')

	while e > 0.00000001:  # 开始迭代
		P_n1 = np.dot(A, P_n)  # 迭代公式
		e = P_n1 - P_n
		e = max(map(abs, e))  # 计算误差
		P_n = P_n1
		k += 1
		print('iteration %s:' % str(k), P_n1)
	# print('final result:', P_n)
	print('开始存储')
	f2 = open('pagerank_result.csv', 'a', newline='', encoding="utf-8")
	csv_write_2 = csv.writer(f2)
	m=0
	for i in range(len(P_n)):
		csv_write_2.writerow([m,P_n[i]])
		print([m,P_n[i]])
		m+=1
	print('结束')

