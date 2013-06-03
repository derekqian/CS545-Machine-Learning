/*
 * Homework 2 for ML course.
 * How to run? -- 1. put the traning file "optdigit.train" and the test file "optdigit.test" in the same directory as this program.
 *                2. run by "java optdigit rate", rate is the learning rate provided to the program
 */

import java.io.*;
import java.util.*;
import java.text.*;

class optdigits {
    private double rate; // the learning rate of the perceptrons
    private double[][][] weight = new double[10][10][65]; // the weight matrix for the perceptrons, weight[i][j] is the weights for the perceptron "i" vs "j"
                                                          // this matrix is a strictly upper triangular matrix
                                                          // the perceptron[i][j] output 1 if the input is i, output -1 if the input is j

    public optdigits(double rate) {
	this.rate = rate;
    }
    public void dispWeight() {
	System.out.println("Weights:");
	for(int i=0; i<10; i++) {
	    for(int j=i+1; j<10; j++) {
		System.out.println(i+","+j+":");
		for(int k=0; k<65; k++) {
		    System.out.print(weight[i][j][k]+",");
		}
		System.out.println();
	    }
	}
    }

    // calculate the output of the perceptron befor sign
    private double calcOutput(double[] w, int[] x) {
	double res = w[0];
	for(int i=0; i<64; i++) {
	    res += w[i+1] * x[i];
	}
	return res;
    }
    private int sign(double x) {
	return x>0 ? 1 : -1;
    }

    // x is 65 elements long, x[0..63] is the data, x[64] is the result
    // i is the true number, j is the false number
    private boolean updateWeight(int d1, int d2, int[] x) {
	boolean res = false; // default to weight not changed

	int t = x[64]==d1 ? 1 : (x[64]==d2 ? -1 : 0);
	if(t == 0) {
	    throw new RuntimeException("Invalid input!");
	}

	double[] w = weight[d1][d2];
	int o = sign(calcOutput(w, x));
	double coe = rate * (t - o);

	// updating the weight
	w[0] += coe;
	for(int i=0; i<64; i++) {
	    if((t - o) * x[i] > 0) {
		res = true;
	    }
	    w[i+1] += coe * x[i];
	}

	return res;
    }

    /*
     * train a single perceptron d1 vs d2, where output 1 mean d1, -1 mean d2
     * return the epoch used
     */
    private int trainbi(int d1, int d2, int[][] traindata) {
	if(d1 >= d2) {
	    throw new RuntimeException("invalid input!");
	}

	// randomly set the weight between -1 and 1
	for(int i=0; i<65; i++) {
	    weight[d1][d2][i] = Math.random() * 2 - 1;
	    //weight[d1][d2][i] = 0;
	}

	int epoch = 0;
	while(true) {
	    int[][] con = testbi(d1, d2, traindata);
	    double oldacc = (con[0][0]+con[1][1])*1.0/(con[0][0]+con[0][1]+con[1][0]+con[1][1]);
	    for(int i=0; i<traindata.length; i++) {
		if(traindata[i][64]==d1 || traindata[i][64]==d2) {
		    updateWeight(d1, d2, traindata[i]);
		}
	    }
	    con = testbi(d1, d2, traindata);
	    double newacc = (con[0][0]+con[1][1])*1.0/(con[0][0]+con[0][1]+con[1][0]+con[1][1]);
	    //System.out.println(d1+","+d2+","+oldacc+","+newacc);
	    if(newacc<=oldacc) {
		break;
	    }
	    epoch++;
	}

	return epoch;
    }

    /*
     * train all the perceptrons with the whole trainning data
     * return the epochs used
     */
    private int[][] train(int[][] traindata) {
	int[][] epoch = new int[10][10];
	for(int i=0; i<10; i++) {
	    for(int j=i+1; j<10; j++) {
		epoch[i][j] = trainbi(i,j,traindata);
	    }
	}

	return epoch;
    }

    /*
     * test one perceptron(d1,d2) on the test data set, and return the confusion matrix.
     */
    private int[][] testbi(int d1, int d2, int[][] testdata) {
	int tp=0, fp=0, tn=0, fn=0;
	for(int i=0; i<testdata.length; i++) {
	    if(testdata[i][64]==d1) {
		double o = calcOutput(weight[d1][d2], testdata[i]);
		if(sign(o)==1) {
		    tp++;
		} else {
		    fn++;
		}
	    } else if(testdata[i][64]==d2) {
		double o = calcOutput(weight[d1][d2], testdata[i]);
		if(sign(o)==1) {
		    fp++;
		} else {
		    tn++;
		}
	    }
	}

	return new int[][]{{tp,fn},{fp,tn}};
    }

    /*
     * test all the perceptrons with the whole test data
     * return the confusion matrix
     */
    private int[][] test(int[][] testdata) {
	int[][] confusion = new int[45][4];
	int k = 0;
	for(int i=0; i<10; i++) {
	    for(int j=i+1; j<10; j++) {
		int[][] con = testbi(i,j,testdata);
		double acc = (con[0][0]+con[1][1])*1.0/(con[0][0]+con[0][1]+con[1][0]+con[1][1]);
		// System.out.println(i+","+j+","+acc);
		confusion[k][0] = con[0][0];
		confusion[k][1] = con[0][1];
		confusion[k][2] = con[1][0];
		confusion[k][3] = con[1][1];
		k++;
	    }
	}
	return confusion;
    }

    public static void usage() {
	System.out.println("optdigit rate");
    }
    public static int[][] readFile(String filename) {
	// read the data from the file
	ArrayList<String> strs = new ArrayList<String>();
	try{
	    FileInputStream instream = new FileInputStream(filename);
	    DataInputStream datain = new DataInputStream(instream);
	    BufferedReader br = new BufferedReader(new InputStreamReader(datain));

	    String strline = null;
	    while((strline = br.readLine()) != null) {
		strs.add(strline);
	    }

	    datain.close();
	}
	catch (Exception e) {
	    e.printStackTrace(System.out);
	}
	//System.out.println(strs);

	int[][] data = new int[strs.size()][65];
	for(int i=0; i<strs.size(); i++) {
	    String str = strs.get(i);
	    // System.out.println(str);
	    String[] el = str.split(",");
	    for(int j=0; j<el.length; j++) {
		data[i][j] = Integer.valueOf(el[j]);
	    }
	}
	return data;
    }
    public static void main(String[] args) {
	if(args.length != 1) {
	    usage();
	    return;
	}
	double rate = Double.valueOf(args[0]);
	optdigits od = new optdigits(rate);

	int[][] traindata = readFile("optdigits.train");
	int[][] testdata = readFile("optdigits.test");

	System.out.println("train on rate: "+rate);

	// train the perceptrons
	int[][] ep = od.train(traindata);
	int[] epoch = new int[45];
	int k = 0;
	for(int i=0; i<10; i++) {
	    for(int j=i+1; j<10; j++) {
		epoch[k++] = ep[i][j];
	    }
	}

	// od.dispWeight();

	// calculate the accuracy for the training data
	int[][] confusion = od.test(traindata);
	double[] trainacc = new double[confusion.length];
	for(int i=0; i<confusion.length; i++) {
	    trainacc[i] = (confusion[i][0] + confusion[i][3]) * 1.0 / (confusion[i][0]+confusion[i][1]+confusion[i][2]+confusion[i][3]);
	}

	// calculate the accuracy for the test data
	confusion = od.test(testdata);
	double[] testacc = new double[confusion.length];
	for(int i=0; i<confusion.length; i++) {
	    testacc[i] = (confusion[i][0] + confusion[i][3]) * 1.0 / (confusion[i][0]+confusion[i][1]+confusion[i][2]+confusion[i][3]);
	}

	// generate report
	String[] label = new String[45];
	k = 0;
	for(int i=0; i<10; i++) {
	    for(int j=i+1; j<10; j++) {
		label[k++] = new String("$<$"+i+","+j+"$>$");
	    }
	}
	DecimalFormat df = new DecimalFormat("#.##");
	for(int i=0; i<confusion.length; i++) {
	    System.out.println(label[i]+" & "+epoch[i]+" & "+df.format(trainacc[i])+" & "+df.format(testacc[i])+" & "+confusion[i][0]+" & "+confusion[i][1]+" & "+confusion[i][2]+" & "+confusion[i][3]+"\\\\");
	}
    }
}