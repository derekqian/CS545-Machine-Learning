import os, sys
import random
import math
from numpy import *
try:
    import pylab
except:
    print "error:\tcan't import pylab module, you must install the module:\n"
    print "\tmatplotlib to plot charts!'\n"

def plot_roc(data):
    """ Function to plot ROC
    Parameters:
    data: The data
    Return:
    """

    data = sorted(data,lambda x,y: cmp(y[1],x[1]))
    # print data

    #Convert to points in a ROC
    interval = (data[0][1]-data[-1][1])/20
    threshold = data[0][1]
    total_n = len([x for x in data if x[0] == -1])
    total_p = len(data) - total_n
    previous_df = -1000000.0
    current_index = 0
    points = []
    tp_count, fp_count = 0.0 , 0.0
    tpr, fpr = 0, 0
    while current_index < len(data):
        if data[current_index][1] < threshold:
            points.append((fpr,tpr))
            threshold = threshold - interval
        if data[current_index][0] == -1:
            fp_count +=1
        elif data[current_index][0] == 1:
            tp_count +=1
        fpr = fp_count/total_n
        tpr = tp_count/total_p
        current_index +=1
    points.append((fpr,tpr)) #Add last point
    points.sort(key=lambda i: (i[0],i[1]))
    print points

    pylab.figure()
    pylab.plot([x[0] for x in points], [y[1] for y in points], 'rx-')
    #pylab.plot([0.0,1.0], [0.0,1.0],'k-.')
    pylab.ylim((0,1))
    pylab.xlim((0,1))
    pylab.xticks(pylab.arange(0,1.1,.1))
    pylab.yticks(pylab.arange(0,1.1,.1))
    pylab.grid(True)
    #cax = pylab.gca()
    #cax.set_aspect('equal')
    pylab.xlabel('FPR')
    pylab.ylabel('TPR')
    pylab.title('ROC')
    #pylab.show()
    return

def experiment1():

    print 'Experiment 1:'

    # train svm model
    print ''
    cmd='./svm_learn -t 0 spam.train spam.model'
    print cmd
    os.system(cmd)

    # test train svm model
    print ''
    cmd='./svm_classify spam.test spam.model spam.predictions'
    print cmd
    os.system(cmd)

    actual_class = [int(float(line_act.strip().split()[0])) for line_act in open("spam.test", 'r')]
    # print actual_class
    score = [float(line_score.strip()) for line_score in open('spam.predictions', 'r')]
    # print score
    data = zip(actual_class, score)
    plot_roc(data)
    return

def boost_train(T):
    print ''
    print 'function: boost_train'
    train_org = [line for line in open('spam.train', 'r')]
    N = len(train_org)
    #print 'N = ', N
    w = ones((N,T+1),dtype=float)/N
    #print 'w = ', w
    index = ones((N,T))
    #print 'index = ', index
    e = zeros(T)
    #print 'e = ', e
    alpha = zeros(T)
    #print 'alpha = ', alpha
    for t in range(T):
        # generate new train file
        wtemp = list(w[:,t])
        #print 'wtemp = ', wtemp
        for i in range(len(wtemp)-1):
            wtemp[i+1] = wtemp[i+1] + wtemp[i]
        #print 'wtemp = ', wtemp
        datarand = random.rand(N)
        #print 'datarand = ', datarand
        dataindex = zeros(N,dtype=int) + len(wtemp)
        for i in range(len(wtemp)):
            itemp = where(datarand < wtemp[i])
            dataindex[itemp] = dataindex[itemp] - 1
        #print 'dataindex = ', dataindex
        f = open('spam.train.%02d'%t, 'w')
        for i in dataindex:
            f.write("%s" % train_org[i])
        f.close()

        print ''
        cmd='./svm_learn -t 0 spam.train.%02d spam.model.%02d'%(t,t)
        print cmd
        os.system(cmd)
        print ''
        cmd='./svm_classify spam.train spam.model.%02d spam.train.predictions.%02d'%(t,t)
        print cmd
        os.system(cmd)

        actual_class = array([int(float(line_act.strip().split()[0])) for line_act in open("spam.train", 'r')])
        #print 'actual_class = ', actual_class
        score = array([float(line_score.strip()) for line_score in open('spam.train.predictions.%02d'%t, 'r')])
        #print 'score = ', score
        predict_class = where((score>0),1,-1)
        #print 'predict_class = ', predict_class
        errors = where((actual_class!=predict_class),1,0)
        #print 'errors = ', errors
        index[:,t] = errors
        #print 'index = ', index
        #print "index: ", index[:,t]
        #print "e: ", w[:,t] * index[:,t]
        e[t] = sum(w[:,t]*index[:,t])/sum(w[:,t])
        #print 'e = ', e
        if e[t]==0:
            alpha = alpha[:t]
            break
        #print "e: ",e[t]
        alpha[t] = log((1-e[t])/e[t])/2
        #print 'alpha = ', alpha
        #print "alpha: ", alpha[t]
        w[:,t+1] = w[:,t]* exp(-1*alpha[t]*actual_class*predict_class)
        #print 'w = ', w
        w[:,t+1] = w[:,t+1]/sum(w[:,t+1])
        #print 'w = ', w

    return alpha

def boost_test(alpha):
    print ''
    print 'function: boost_test'
    if len(alpha)==0:
        print ''
        cmd='./svm_classify spam.test spam.model.00 spam.predictions'
        print cmd
        os.system(cmd)
    else:
        N = len([line for line in open('spam.test', 'r')])
        final_score = array(zeros(N))
        for i in range(len(alpha)):
            print ''
            cmd='./svm_classify spam.test spam.model.%02d spam.predictions.%02d'%(i,i)
            print cmd
            os.system(cmd)
            
            score = array([float(line_score.strip()) for line_score in open('spam.predictions.%02d'%i, 'r')])
            #print 'score = ', score
            predict_class = where((score>0),1,-1)
            #print 'predict_class = ', predict_class
            final_score = final_score + alpha[i] * predict_class
        f = open('spam.predictions','w+')
        for i in range(len(final_score)):
            f.write('%.8f\n'%final_score[i])
        f.close()

    print ''
    print 'In summary:'
    actual_class = array([int(float(line_act.strip().split()[0])) for line_act in open("spam.test", 'r')])
    #print 'actual_class = ', actual_class
    score = array([float(line_score.strip()) for line_score in open('spam.predictions', 'r')])
    #print 'score = ', score
    predict_class = where((score>0),1,-1)
    #print 'predict_class = ', predict_class
    errors = where((actual_class!=predict_class),1,0)
    #print 'errors = ', errors
    print 'Accuracy on test set: %.2f'%(100.0*(len(errors)-sum(errors))/len(errors))+'% '+'(%d correct, %d incorrect, %d total)'%(len(errors)-sum(errors),sum(errors),len(errors))
    return

def experiment2():

    print 'Experiment 2:'

    T = 10

    # train svm model
    alpha = boost_train(T)
    print ''
    print 'function: experiment2'
    print 'alpha = ', alpha
    if T!=len(alpha):
        print 'Trainning terminate earlier'

    # test train svm model
    boost_test(alpha)

    actual_class = [int(float(line_act.strip().split()[0])) for line_act in open("spam.test", 'r')]
    # print actual_class
    score = [float(line_score.strip()) for line_score in open('spam.predictions', 'r')]
    # print score
    data = zip(actual_class, score)
    plot_roc(data)
    return

def experiment3():

    print 'Experiment 3:'

    T = 20

    # train svm model
    alpha = boost_train(T)
    print ''
    print 'function: experiment3'
    print 'alpha = ', alpha
    if T!=len(alpha):
        print 'Trainning terminate earlier'

    # test train svm model
    boost_test(alpha)

    actual_class = [int(float(line_act.strip().split()[0])) for line_act in open("spam.test", 'r')]
    # print actual_class
    score = [float(line_score.strip()) for line_score in open('spam.predictions', 'r')]
    # print score
    data = zip(actual_class, score)
    plot_roc(data)
    return


experiment1()
#experiment2()
#experiment3()
pylab.show()

