import java.io.*;
import java.util.*;

class makesmall {
    public static void usage() {
	System.out.println("makesmall infile outfile");
    }
    public static void main(String[] args) {
	String infilename = null;
	String outfilename = null;
	if(args.length != 2) {
	    infilename = "optdigits.data";
	    outfilename = "small-optdigits.data";
	} else {
	    infilename = args[0];
	    outfilename = args[1];
	}
	System.out.println(infilename + " to " + outfilename);
	ArrayList<Vector<String>> vecarray = new ArrayList<Vector<String>>(10);
	for(int i=0; i<10; i++) {
	    vecarray.add(i, new Vector<String>());
	}
	try{
	    FileInputStream instream = new FileInputStream(infilename);
	    DataInputStream datain = new DataInputStream(instream);
	    BufferedReader br = new BufferedReader(new InputStreamReader(datain));
	    FileOutputStream outstream = new FileOutputStream(outfilename);
	    DataOutputStream dataout = new DataOutputStream(outstream);
	    BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(dataout));
	    boolean firstline = true;
	    int[] written = new int[10];
	    String strline = null;
	    while((strline = br.readLine()) != null) {
		int index = strline.charAt(strline.length()-1)-'0';
		Vector<String> temp = vecarray.get(index);
		temp.add(strline);

		if(written[index] < 50) {
		    if(!firstline) {
			bw.newLine();
		    } else {
			firstline = !firstline;
		    }
		    bw.write(strline);
		    written[index]++;
		}
	    }
	    bw.flush();
	    datain.close();
	}
	catch (Exception e) {
	    e.printStackTrace(System.out);
	}
	for(Vector<String> temp : vecarray) {
	    System.out.println(temp.size());
	}
	for(String temp : vecarray.get(7)) {
	    System.out.println(temp);
	}
    }
}