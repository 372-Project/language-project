import java.util.Scanner;

public class c {
	public static void main(String[] args) {
		int var1 = 5;
		int var2 = 7;
		int var3 = 6;
		Scanner in1 = new Scanner(System.in);
		String var70 = in1.nextLine();
		if (var1 < var2) {
			var3 = var1 + var2;
		}
		if (var1 > var2) {
			var3 = var1 + var2;
			var2 = var1 + 2;
		}
		else {
			System.out.println(false);
		}
		while (var1 < var2) {
			var3 = var3 + 2;
			var1 = var1 + 1;
		}
		var1 = 3;
		var2 = 8;
		while (var1 < var2) {
			var3 = var3 + 2;
			var1 = var1 + 1;
		}
		String var10 = "Hel";
		String var11 = "lo";
		None var12 = var10 + var11;
		Scanner in2 = new Scanner(System.in);
		String var73 = in2.nextLine();

	}
}
