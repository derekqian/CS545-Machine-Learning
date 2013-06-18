import os, sys
import random
import math
from pylab import *
from numpy import *
from matplotlib import *

def testonly():
    train('optdigits.train',10)

def distance(sample,center):
    temp = sample - center
    d = dot(temp,temp)
    return sqrt(d)

def calcSSE(cls,cen):
    SSE = 0
    for i in xrange(len(cen)):
        for cl in cls[i]:
            temp = cl[:-1] - cen[i]
            SSE += dot(temp,temp)
    return SSE

def calcEntropy(p):
    if p!=0:
        return -p * log2(p)
    else:
        return 0

def classify(samples,cur,K):
    cls = [[] for i in xrange(K)]
    for sam in samples:
        c = 0
        d = 0
        for i in xrange(K):
            if i==0:
                c = 0
                d = distance(sam[:len(sam)-1],cur[i])
            else:
                d1 = distance(sam[:len(sam)-1],cur[i])
                if(d1<d):
                    c = i
                    d = d1
        cls[c].append(sam)
    return cls

#randomly generate centroid
def train1(filename,K):
    samples = array([map(int,line.strip().split(',')) for line in open(filename, 'r')])
    minima = samples.min(axis=0)[:-1]
    maxima = samples.max(axis=0)[:-1]
    centroid = zeros((K,len(samples[0])-1))
    clses = [[] for i in xrange(K)]
    SSE = 0
    tries = 0
    it = 0
    while True:
        if it==0:
            pre = ones((K,len(samples[0])-1)) * -1
            cur = random.rand(K,len(samples[0])-1) * (maxima - minima) + minima
            #cur = random.rand(K,len(samples[0])-1) * 16
        cls = classify(samples,cur,K)
        pre = cur.copy()
        for i in xrange(K):
            if len(cls[i])==0:
                #print '%d: empty cluster %d, try again'%(it,i)
                pre = ones((K,len(samples[0])-1)) * -1
                cur = random.rand(K,len(samples[0])-1) * (maxima - minima) + minima
                #cur = random.rand(K,len(samples[0])-1) * 16
                break
            else:
                temp = mean(cls[i],axis=0)
                #print temp
                cur[i] = temp[:len(temp)-1]
        #print pre
        #print cur
        if sum(where(cur!=pre,1,0))==0:
            if tries==0:
                centroid = cur.copy()
                clses = list(cls)
                SSE = calcSSE(cls,cur)
                #print centroid[0]
                #print SSE
            else:
                temp = calcSSE(cls,cur)
                if temp<SSE:
                    centroid = cur.copy()
                    clses = list(cls)
                    SSE = temp
                #print cur[0]
                #print temp
            pre = ones((K,len(samples[0])-1)) * -1
            cur = random.rand(K,len(samples[0])-1) * (maxima - minima) + minima
            #cur = random.rand(K,len(samples[0])-1) * 16
            tries += 1
            if tries>=5:
                #print centroid[0]
                #print SSE
                break
        it = it + 1
        if it>=256:
            print 'max iterations'
            break
    #print cls
    mat = zeros((K,10),dtype=int)
    for i in xrange(K):
        for sam in clses[i]:
            mat[i][sam[-1]] += 1
    #print mat
    maxmat = mat.max(axis=1)
    #print maxmat
    c = zeros((K,1))
    for i in xrange(K):
        c[i] = where(mat[i]==maxmat[i])[0][0]
    centroid = append(centroid,c,1)
    m = mat.sum(axis=1)
    p = zeros((K,10))
    for i in xrange(len(m)):
        p[i] = mat[i]*1.0/m[i]
    for i in xrange(len(p)):
        for j in xrange(len(p[0])):
            p[i][j] = calcEntropy(p[i][j])
    e = p.sum(1)
    print 'avg_entropy = %.4f'%(dot(e,m*1.0/sum(m)))
    return (centroid,SSE,e)

# randomly choose the data from the training set as initial centroid
def train2(filename,K):
    samples = array([map(int,line.strip().split(',')) for line in open(filename, 'r')])
    minima = samples.min(axis=0)[:-1]
    maxima = samples.max(axis=0)[:-1]
    centroid = zeros((K,len(samples[0])-1))
    clses = [[] for i in xrange(K)]
    SSE = 0
    tries = 0
    it = 0
    while True:
        if it==0:
            pre = ones((K,len(samples[0])-1)) * -1
            cur = samples[map(int,floor(random.rand(K)*len(samples)))][:,:-1]
        cls = classify(samples,cur,K)
        pre = cur.copy()
        for i in xrange(K):
            if len(cls[i])==0:
                #print '%d: empty cluster %d, try again'%(it,i)
                pre = ones((K,len(samples[0])-1)) * -1
                cur = samples[map(int,floor(random.rand(K)*len(samples)))][:,:-1]
                break
            else:
                temp = mean(cls[i],axis=0)
                #print temp
                cur[i] = temp[:len(temp)-1]
        #print pre
        #print cur
        if sum(where(cur!=pre,1,0))==0:
            if tries==0:
                centroid = cur.copy()
                clses = list(cls)
                SSE = calcSSE(cls,cur)
                #print centroid[0]
                #print SSE
            else:
                temp = calcSSE(cls,cur)
                if temp<SSE:
                    centroid = cur.copy()
                    clses = list(cls)
                    SSE = temp
                #print cur[0]
                #print temp
            pre = ones((K,len(samples[0])-1)) * -1
            cur = samples[map(int,floor(random.rand(K)*len(samples)))][:,:-1]
            tries += 1
            if tries>=5:
                #print centroid[0]
                #print SSE
                break
        it = it + 1
        if it>=256:
            print 'max iterations'
            break
    #print cls
    mat = zeros((K,10),dtype=int)
    for i in xrange(K):
        for sam in clses[i]:
            mat[i][sam[-1]] += 1
    #print mat
    maxmat = mat.max(axis=1)
    #print maxmat
    c = zeros((K,1))
    for i in xrange(K):
        c[i] = where(mat[i]==maxmat[i])[0][0]
    centroid = append(centroid,c,1)
    m = mat.sum(axis=1)
    p = zeros((K,10))
    for i in xrange(len(m)):
        p[i] = mat[i]*1.0/m[i]
    for i in xrange(len(p)):
        for j in xrange(len(p[0])):
            p[i][j] = calcEntropy(p[i][j])
    e = p.sum(1)
    print 'avg_entropy = %.4f'%(dot(e,m*1.0/sum(m)))
    return (centroid,SSE,e)

def test(filename,centroid):
    samples = array([map(int,line.strip().split(',')) for line in open(filename, 'r')])
    act_cls = samples[:,-1]
    #print act_cls
    pred_cls = zeros(len(act_cls),dtype=int)
    for i in xrange(len(samples)):
        c = 0
        d = 0
        for j in xrange(len(centroid)):
            if j==0:
                c = 0
                d = distance(samples[i][:-1],centroid[j][:-1])
            else:
                d1 = distance(samples[i][:-1],centroid[j][:-1])
                if(d1<d):
                    c = j
                    d = d1
        pred_cls[i] = centroid[c][-1]
    #print pred_cls
    accuracy = sum(where(pred_cls==act_cls,1,0))*1.0/len(act_cls)
    #print accuracy
    confusion = [zeros(10,dtype=int) for digit in xrange(10)]
    for i in xrange(10):
        for j in xrange(10):
            index = where(act_cls==i)
            confusion[i][j] = sum(where(pred_cls[index]==j,1,0))
    #print confusion
    return(confusion,accuracy)

def toPGM(centroid,filename):
    for i in xrange(len(centroid)):
        f = open('%s%02d%d.pgm'%(filename,i,centroid[i][-1]),'w')
        f.write('P2\n')
        f.write('8 8\n')
        f.write('16')
        for j in xrange(len(centroid[0])-1):
            if (j%8)==0:
                f.write('\n%d'%centroid[i][j])
            else:
                f.write(' %d'%centroid[i][j])
        f.write('\n')
        f.close()

def experiment1():
    print 'Experiment 1:'
    (centroid,SSE,entropy) = train1('optdigits.train',10)
    toPGM(centroid,'img1')
    print 'SSE = %.02f'%SSE
    s = ''
    for i in xrange(len(entropy)):
        s += '%.2f,'%entropy[i]
    print 'entropy = %s'%s
    (confusion,accuracy) = test('optdigits.test',centroid)
    print confusion
    print 'accuracy = %.4f'%accuracy

def experiment2():
    print 'Experiment 2:'
    (centroid,SSE,entropy) = train2('optdigits.train',30)
    toPGM(centroid,'img2')
    print 'SSE = %.02f'%SSE
    s = ''
    for i in xrange(len(entropy)):
        s += '%.2f,'%entropy[i]
    print 'entropy = %s'%s
    (confusion,accuracy) = test('optdigits.test',centroid)
    print confusion
    print 'accuracy = %.4f'%accuracy

if __name__ == "__main__":
    params = sys.argv
    if len(params)==2 and params[1]=='1':
        experiment1()
    elif len(params)==2 and params[1]=='2':
        experiment2()
    else:
        print 'usage:'
        print '  experiment 1: python kmeans.py 1'
        print '  experiment 2: python kmeans.py 2'


