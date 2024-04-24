import java.util.Scanner;


public class even_or_odd {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		System.out.print("Enter in 10 numbers.\n");
		String ones = in.nextLine();
		int one = Integer.parseInt(ones);
		String twos = in.nextLine();
		int two = Integer.parseInt(twos);
		String threes = in.nextLine();
		int three = Integer.parseInt(threes);
		String fours = in.nextLine();
		int four = Integer.parseInt(fours);
		String fives = in.nextLine();
		int five = Integer.parseInt(fives);
		String sixs = in.nextLine();
		int six = Integer.parseInt(sixs);
		String sevens = in.nextLine();
		int seven = Integer.parseInt(sevens);
		String eights = in.nextLine();
		int eight = Integer.parseInt(eights);
		String nines = in.nextLine();
		int nine = Integer.parseInt(nines);
		String tens = in.nextLine();
		int ten = Integer.parseInt(tens);
		System.out.print("10 numbers detected, performing even or odd checks!\n");
		System.out.print("10 numbers are: " + one + " " + two + " " + three + " " + four + " " + five + " " + six + " " + seven + " " + eight + " " + nine + " " + ten + "\n");
		String evens = "Evens: ";
		String odds = "Odds: ";
		if (one % 2 == 0) {
			evens = evens + one + " ";
		}
		else {
			odds = odds + one + " ";
		}
		if (two % 2 == 0) {
			evens = evens + two + " ";
		}
		else {
			odds = odds + two + " ";
		}
		if (three % 2 == 0) {
			evens = evens + three + " ";
		}
		else {
			odds = odds + three + " ";
		}
		if (four % 2 == 0) {
			evens = evens + four + " ";
		}
		else {
			odds = odds + four + " ";
		}
		if (five % 2 == 0) {
			evens = evens + five + " ";
		}
		else {
			odds = odds + five + " ";
		}
		if (six % 2 == 0) {
			evens = evens + six + " ";
		}
		else {
			odds = odds + six + " ";
		}
		if (seven % 2 == 0) {
			evens = evens + seven + " ";
		}
		else {
			odds = odds + seven + " ";
		}
		if (eight % 2 == 0) {
			evens = evens + eight + " ";
		}
		else {
			odds = odds + eight + " ";
		}
		if (nine % 2 == 0) {
			evens = evens + nine + " ";
		}
		else {
			odds = odds + nine + " ";
		}
		if (ten % 2 == 0) {
			evens = evens + ten + " ";
		}
		else {
			odds = odds + ten + " ";
		}
		evens = evens + "\n";
		odds = odds + "\n";
		System.out.print(evens);
		System.out.print(odds);

		in.close();
	}
}
