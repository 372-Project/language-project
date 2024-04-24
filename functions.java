public class functions {

	public static int square(int input){
		int var = input * input;
		return var;
	}
	public static int cube(int input){
		int cubed = input * input * input;
		return cubed;
	}
	public static void even_or_odd(int input){
		int result = input % 2;
		if (result == 0) {
			System.out.print(input + " is odd\n");
		}
		else {
			System.out.print(input + " is even\n");
		}
	}
	public static void main(String[] args) {
		int num = 5;
		int squared = square(num);
		System.out.print(num + " squared is: " + squared + "\n");
		int cubed = cube(num);
		System.out.print(num + " cubed is: " + cubed + "\n");
		int n1 = 1;
		int n2 = 2;
		even_or_odd(n1);
		even_or_odd(n2);

	}
}
