public class guessing_game {

	public static void main(String[] args) {
		int theNumber = 74;
		System.out.print("Guess a number between 1 and 100\n");
		int guessed = 0;
		while (guessed == 0) {
			String userIns = in.nextLine();
			int userIn = Integer.parseInt(userIns);
			if (userIn < theNumber) {
				System.out.print("Number too low, try again!\n");
			}
			if (userIn > theNumber) {
				System.out.print("Number too high, try again!\n");
			}
			if (userIn == theNumber) {
				guessed = 1;
				System.out.print("You got it! The number is 74!\n");
			}
		}

		in.close();
	}
}
