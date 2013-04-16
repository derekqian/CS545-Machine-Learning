import java.io.*;
import java.util.*;

class makenoisy {
    public static void usage() {
	System.out.println("makenoisy infile outfile");
    }
    public static void main(String[] args) {
	String infilename = null;
	String outfilename = null;
	if(args.length != 2) {
	    infilename = "optdigits.data";
	    outfilename = "noisy-optdigits.data";
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
	    String strline = null;
	    while((strline = br.readLine()) != null) {
		int index = strline.charAt(strline.length()-1)-'0';
		Vector<String> temp = vecarray.get(index);
		temp.add(strline);

		if(!firstline) {
		    bw.newLine();
		} else {
		    firstline = !firstline;
		}

		// randomly change the data
		int randomline = (int)(Math.random() * 20); // 5%
		if(randomline == 0) {
		    // change the digit to a random digit
		    int randomdigit = (int)(Math.random() * 10); // 0-9
		    char[] rawstr = strline.toCharArray();
		    rawstr[rawstr.length-1] = (char)((int)'0' + randomdigit);
		    System.out.println(strline);
		    strline = String.valueOf(rawstr);
		    System.out.println("to");
		    System.out.println(strline);
		}

		bw.write(strline);
	    }
	    bw.flush();
	    datain.close();
	}
	catch (Exception e) {
	    e.printStackTrace(System.out);
	}
	/*for(Vector<String> temp : vecarray) {
	    System.out.println(temp.size());
	}
	for(String temp : vecarray.get(7)) {
	    System.out.println(temp);
	    }*/
    }
}