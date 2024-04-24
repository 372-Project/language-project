import java.util.Scanner;


public class add_sub_div_mult {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		System.out.print("Enter the first number\n");
		String numberOnes = in.nextLine();
		int numberOne = Integer.parseInt(numberOnes);
		System.out.print("Enter the second number\n");
		String numberTwos = in.nextLine();
		int numberTwo = Integer.parseInt(numberTwos);
		System.out.print("Enter 1 for addition, 2 for subtraction, 3 for division,\n4 for multiplication, or 5 for modulus\n");
		String operations = in.nextLine();
		int operation = Integer.parseInt(operations);
		int result = 0;
		if (operation == 1) {
			result = numberOne + numberTwo;
			System.out.print(result);
			System.out.print("\n");
		}
		if (operation == 2) {
			result = numberOne - numberTwo;
			System.out.print(result);
			System.out.print("\n");
		}
		if (operation == 3) {
			result = numberOne / numberTwo;
			System.out.print(result);
			System.out.print("\n");
		}
		if (operation == 4) {
			result = numberOne * numberTwo;
			System.out.print(result);
			System.out.print("\n");
		}
		if (operation == 5) {
			result = numberOne % numberTwo;
			System.out.print(result);
			System.out.print("\n");
		}

		in.close();
	}
}
