import java.util.Scanner;


public class helloname {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		System.out.print("Please enter your name\n");
		String name = in.nextLine();
		String begin = "Hello ";
		String ending = "!! Thanks for using our language!\n";
		String output = begin + name + ending;
		System.out.print(output);

		in.close();
	}
}
