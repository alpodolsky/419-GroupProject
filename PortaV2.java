/**
 * 
 */
package sec;

/**
 * @author Will
 *
 */
public class Porta {

	/**
	 * @param args
	 */
	
	public char[][] table(){
		String firstHalf = "abcdefghijklm";
		String secondHalf = "nopqrstuvwxyz";
		char[][] table = new char[13][26];
		int index = 0;
		int index4 = 0;
		for(int x=0; x<13; x++) {
			int index2 = index;
			for(int y=0; y<13; y++) {
				char letter = secondHalf.charAt(index2);
				table[x][y] = letter;
				System.out.print(table[x][y] + " ");
				if(index2+1 == 13)
					index2 = 0;
				else
					index2++;
			}
			int index3 = index4;
			for(int y=0; y<13; y++) {
				char letter = firstHalf.charAt(index3);
				table[x][y+13] = letter;
				System.out.print(table[x][y+13] + " ");
				if(index3+1 == 13)
					index3 = 0;
				else
					index3++;
			}
			System.out.println();
			if(index+1 == 13)
				index = 0;
			else
				index++;
			if(index4 == 0)
				index4 = 12;
			else
				index4--;
		}
		return table;
	}
	
	public String encrypt(String plain, String key) {
		
		String encrypted="";
		char[][] tab = table();
		String plainNoSpace = plain.replace(" ", "");
		String keytext = new String();
		int index = 0;
		for(int x=0; x<plainNoSpace.length(); x++) {
			keytext+=key.substring(index, index+1);
			if(index == key.length()-1)
				index = 0;
			else
				index++;
		}
		System.out.println("Plain no space: "+plainNoSpace);
		System.out.println("Keytext: "+keytext);
		if(plainNoSpace.length() == keytext.length())
			System.out.println("Yes");
		
		int index2 = 0;
		for(int x=0; x<plain.length(); x++) {
			//System.out.println(x);
			if(plain.substring(x, x+1) == " ")
				encrypted+=" ";
			else {
				//row is repeated key word letter index
				//col is plain text index
				
				int row = (keytext.charAt(index2) - 'a')/2;
				int col = plainNoSpace.charAt(index2) - 'a';
				encrypted+=tab[row][col];
				if(index2 == keytext.length()-1)
					index2 = 0;
				else
					index2++;
			}
		}
		
		
		System.out.println(encrypted);
		return encrypted;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Porta algo = new Porta();
		String plain = "synnjshwybwpngmzlqvrzdmtnsynnj";
		String key = "fortify";
		String p = algo.encrypt(plain, key);

	}

}
