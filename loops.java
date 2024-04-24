public class loops {

	public static void main(String[] args) {
		int var1 = 0;
		int var2 = 10;
		while (var1 < var2) {
			System.out.print(var1);
			System.out.print("\n");
			var1 = var1 + 1;
		}
		System.out.print("\n");
		while (var1 > 0) {
			System.out.print(var1);
			System.out.print("\n");
			var1 = var1 - 1;
		}
		System.out.print("\nPyramid\n");
		int rows = 5;
		int i = 0;
		while (i < rows) {
			int j = 0;
			int difference = rows - i;
			while (j < difference) {
				System.out.print(" ");
				j = j + 1;
			}
			j = 0;
			int size = 2 * i;
			size = size - 1;
			while (j < size) {
				System.out.print("X");
				j = j + 1;
			}
			i = i + 1;
			System.out.print("\n");
		}
		System.out.print("\n");
		int a = 0;
		while (a < 3) {
			System.out.print("Outer loop ");
			System.out.print(a);
			System.out.print("\n");
			int b = 0;
			while (b < 3) {
				System.out.print("Inner loop ");
				System.out.print(b);
				System.out.print("\n");
				if (a < b) {
					System.out.print("a is less than b\n");
				}
				int c = 0;
				while (c < 2) {
					System.out.print("Innermost loop\n");
					c = c + 1;
				}
				b = b + 1;
			}
			a = a + 1;
		}

	}
}
