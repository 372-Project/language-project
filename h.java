import java.util.Scanner;

public class h {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		int goodNum = 7;
		String as = in.nextLine();
		int a = Integer.parseInt(as);
		String bs = in.nextLine();
		int b = Integer.parseInt(bs);
		int max = 0;
		if (a > b) {
			max = a;
		}
		else {
			max = b;
		}
		int c = a + b;

		in.close();
	}
}
