public class PlayFairCipher {
	
	public static char[][] makeTable(String key){
		boolean[] alphabet = new boolean[26];
		for(int k = 0; k < 26; k++) {
			if(k == 9) {
				alphabet[k] = true;
			}else {
				alphabet[k] = false;
			}
		}
		char[][] matrix = new char[5][5];
		int spot = 0;
		int place = 0;
		boolean check = false;
		for(int k = 0; k < 5; k++) {
			for(int i = 0; i < 5; i++) {
				if(place < key.length()) {
					for(int j = place; j < key.length(); j++) {
						char c = key.charAt(j);
						int temp = (int)c;
						int tempInt = 96;
						if(temp<=122 & temp>=97) {
							if(!alphabet[temp-tempInt - 1]) {
								alphabet[temp-tempInt - 1] = true;
								matrix[k][i] = c;
								place++;
								check = true;
								break;
							}
						}
						place++;
					}
				}
				if(place >= key.length() && !check) {
					for(int j = spot; j < alphabet.length; j++) {
						if(!alphabet[j]) {
							matrix[k][i] = (char)(96 + j + 1);
							spot++;
							break;
						}
						spot++;
					}
				}
				if(check) {
					check = false;
				}
			}
		}
		return matrix;
	}
	
	public static int[] findChar(char[][] matrix, char target){
		int[] result = new int[2];
		for(int k = 0; k < 5; k++) {
			for(int i = 0; i < 5; i++) {
				if(matrix[k][i] == target) {
					result[0] = k;
					result[1] = i;
					return result;
				}
			}
		}
		return result;
	}
	
	public static int mod5(int a) {
		if(a < 0) {
			a = (a % 5) + 5;
		}else {
			a = a % 5;
		}
		return a;
	}
	
	public static char[] encrypt(char[][] matrix, String plainText) {
		char[] cipherText = new char[plainText.length()];
		char first = '0';
		char second = '0';
		char temp1 = '0';
		char temp2 = '0';
		int firstIndex = 0;
		boolean check = false;
		for(int k = 0; k < plainText.length(); k++) {
			if((plainText.charAt(k) >= 'a' && plainText.charAt(k) <= 'z'  && plainText.charAt(k) != 'j') || (plainText.charAt(k) >= 'A' && plainText.charAt(k) <= 'Z' && plainText.charAt(k) != 'J') ) {
				if(!check) {
					temp1 = plainText.charAt(k);
					first = Character.toLowerCase(temp1);
					firstIndex = k;
					check = true;
				}else {
					temp2 = plainText.charAt(k);
					second = Character.toLowerCase(temp2);
					int[] index = findChar(matrix, first);
					int row1 = index[0];
					int col1 = index[1];
					index = findChar(matrix, second);
					int row2 = index[0];
					int col2 = index[1];
					if(row1 == row2) {
						first = matrix[row1][mod5(col1 + 1)];
						second = matrix[row2][mod5(col2 + 1)];
					}else if(col1 == col2) {
						first = matrix[mod5(row1 + 1)][col1];
						second = matrix[mod5(row2 + 1)][col2];
					}else {
						first = matrix[row1][col2];
						second = matrix[row2][col1];
					}
					if(temp1 >= 'A' && temp1 <= 'Z') {
						first = Character.toUpperCase(first);
					}
					if(temp2 >= 'A' && temp2 <= 'Z') {
						second = Character.toUpperCase(second);
					}
					cipherText[firstIndex] = first;
					cipherText[k] = second;
					check = false;
				}
			}else {
				cipherText[k] = plainText.charAt(k);
			}
		}
		if(check && plainText.length() != 0) {
			cipherText[cipherText.length - 1] = '$';
		}
		return cipherText;
	}
	
	public static char[] decrypt(char[][] matrix, String cipherText) {
		char[] plainText = new char[cipherText.length()];
		char first = '0';
		char second = '0';
		char temp1 = '0';
		char temp2 = '0';
		int firstIndex = 0;
		boolean check = false;
		for(int k = 0; k < cipherText.length(); k++) {
			if((cipherText.charAt(k) >= 'a' && cipherText.charAt(k) <= 'z'  && cipherText.charAt(k) != 'j') || (cipherText.charAt(k) >= 'A' && cipherText.charAt(k) <= 'Z' && cipherText.charAt(k) != 'J')) {
				if(!check) {
					temp1 = cipherText.charAt(k);
					first = Character.toLowerCase(temp1);
					firstIndex = k;
					check = true;
				}else {
					temp2 = cipherText.charAt(k);
					second = Character.toLowerCase(temp2);
					int[] index = findChar(matrix, first);
					int row1 = index[0];
					int col1 = index[1];
					index = findChar(matrix, second);
					int row2 = index[0];
					int col2 = index[1];
					if(row1 == row2) {
						first = matrix[row1][mod5(col1 - 1)];
						second = matrix[row2][mod5(col2 - 1)];
					}else if(col1 == col2) {
						first = matrix[mod5(row1 - 1)][col1];
						second = matrix[mod5(row2 - 1)][col2];
					}else {
						first = matrix[row1][col2];
						second = matrix[row2][col1];
					}
					if(temp1 >= 'A' && temp1 <= 'Z') {
						first = Character.toUpperCase(first);
					}
					if(temp2 >= 'A' && temp2 <= 'Z') {
						second = Character.toUpperCase(second);
					}
					plainText[firstIndex] = first;
					plainText[k] = second;
					check = false;
				}
			}else {
				plainText[k] = cipherText.charAt(k);
			}
		}
		return plainText;
	}
	
	public static String PLEncrypt(String plainText, String key) {
		String newKey = key.toLowerCase();
		char[][] matrix = makeTable(newKey);
		String text = plainText;
		int count = 0;
		for(int k = 0; k < plainText.length(); k++) {
			if((plainText.charAt(k) >= 'a' && plainText.charAt(k) <= 'z') || (plainText.charAt(k) >= 'A' && plainText.charAt(k) <= 'Z')) {
				count++;
			}
		}
		if(count%2 != 0) {
			text = text + "Q";
		}
		char[] cipherText = encrypt(matrix, text);
		text = String.valueOf(cipherText);
		if(text.length() > 0) {
			if(text.charAt(text.length() - 1) == '$') {
				text = text.substring(0, text.length() - 1);
			}
		}
		return text;
	}
	
	public static String PLDecrypt(String cipherText, String key) {
		String newKey = key.toLowerCase();
		char[][] matrix = makeTable(newKey);
		char[] plainText = decrypt(matrix, cipherText);
		String text = String.valueOf(plainText);
		if(text.length() > 0) {
			if(text.charAt(text.length() - 1) == 'Q') {
				text = text.substring(0, text.length() - 1);
			}
		}
		return text;
	}
	
}
