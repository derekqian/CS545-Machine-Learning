import os, sys
import random
import math
from numpy import *
from matplotlib import *

def testonly():
    data = array([map(int,line.strip().split(',')) for line in open("optdigits.train", 'r')])
    cls = data[:,-1]
    datas = [[] for i in xrange(10)]
    for digit in xrange(10):
        datas[digit] = data[where(cls==digit)]
    f = open('optdigits.train.temp','w')
    for digit in xrange(10):
        for i in xrange(2):
            for j in xrange(4):
                f.write('%d,'%datas[digit][i][j]);
            f.write('%d\n'%datas[digit][i][-1]);
    f.close()
    data = array([map(int,line.strip().split(',')) for line in open("optdigits.test", 'r')])
    cls = data[:,-1]
    datas = [[] for i in xrange(10)]
    for digit in xrange(10):
        datas[digit] = data[where(cls==digit)]
    f = open('optdigits.test.temp','w')
    for digit in xrange(10):
        for i in xrange(3):
            for j in xrange(4):
                f.write('%d,'%datas[digit][i][j]);
            f.write('%d\n'%datas[digit][i][-1]);
    f.close()
    (P,Pc) = train(10,17)
    (confusion,accuracy) = test(P,Pc)

def train(base,level):
    train = array([map(int,line.strip().split(',')) for line in open("optdigits.train.temp", 'r')])
    total = len(train)
    cls = train[:,-1]
    P = zeros(base)
    for digit in xrange(base):
        P[digit] = sum(where(cls==digit,1,0))*1.0/total
    for digit in xrange(base):
        print 'P(\'%d\')=%.1f'%(digit,P[digit]*100) + '%'
    trains = [[] for i in xrange(base)]
    for digit in xrange(base):
        trains[digit] = train[where(cls==digit)]
    Pc = zeros((base,len(train[0])-1,level))
    for digit in xrange(base):
        total = len(trains[digit])
        for attr in xrange(len(train[0])-1):
            a = trains[digit][:,attr]
            for val in xrange(level):
                Pc[digit][attr][val] = sum(where(a==val,1,0))*1.0/total;
                #print 'Pc(Attribute%d=%d|\'%d\')=%.2f'%(attr,val,digit,Pc[digit][attr][val]*100) + '%'
    for digit in xrange(base):
        total = len(trains[digit])
        for attr in xrange(len(train[0])-1):
            a = trains[digit][:,attr]
            for val in xrange(level):
                Pc[digit][attr][val] = (sum(where(a==val,1,0))*1.0+1)/(total+level);
                #print 'Pc(Attribute%d=%d|\'%d\')=%.2f'%(attr,val,digit,Pc[digit][attr][val]*100) + '%'
    return (P,Pc)

def test(P,Pc):
    base = len(P)
    level = len(Pc[0][0])
    test = array([map(int,line.strip().split(',')) for line in open("optdigits.test.temp", 'r')])
    #print test
    act_cls = test[:,-1]
    #print act_cls
    posteriori = array([zeros(base) for ele in test])
    #print posteriori
    for digit in xrange(base):
        prob = [log(P[digit]) for ele in test]
        for attr in xrange(len(test[0])-1):
            prob = add(prob, [log(Pc[digit][attr][ele[attr]]) for ele in test])
        posteriori[:,digit] = prob
    #print posteriori
    pred_cls = posteriori.argmax(axis=1)
    #print pred_cls
    accuracy = sum(where(pred_cls==act_cls,1,0))*1.0/len(act_cls)
    print accuracy
    confusion = [zeros(10,dtype=int) for digit in xrange(base)]
    for i in xrange(base):
        for j in xrange(base):
            index = where(act_cls==i)
            confusion[i][j] = sum(where(pred_cls[index]==j,1,0))
    print confusion
    return(confusion,accuracy)

def experiment1():
    print 'Experiment 1:'
    os.system('cp optdigits.train optdigits.train.temp')
    os.system('cp optdigits.test optdigits.test.temp')
    (P,Pc) = train(10,17)
    (confusion,accuracy) = test(P,Pc)

def experiment2():
    print 'Experiment 2:'
    data = array([map(int,line.strip().split(',')) for line in open("optdigits.train", 'r')])
    f = open('optdigits.train.temp','w')
    for i in xrange(len(data)):
        for j in xrange(len(data[0])-1):
            a = where(data[i][j]==0,1,data[i][j])
            a = (a-1)/4
            f.write('%d,'%a);
        f.write('%d\n'%data[i][-1]);
    f.close()
    data = array([map(int,line.strip().split(',')) for line in open("optdigits.test", 'r')])
    f = open('optdigits.test.temp','w')
    for i in xrange(len(data)):
        for j in xrange(len(data[0])-1):
            a = where(data[i][j]==0,1,data[i][j])
            a = (a-1)/4
            f.write('%d,'%a);
        f.write('%d\n'%data[i][-1]);
    f.close()
    (P,Pc) = train(10,17)
    (confusion,accuracy) = test(P,Pc)

if __name__ == "__main__":
    params = sys.argv
    if len(params)==2 and params[1]=='1':
        experiment1()
    elif len(params)==2 and params[1]=='2':
        experiment2()
    else:
        print 'testonly:'
        testonly()

