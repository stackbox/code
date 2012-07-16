package Bean;


public class Counter {
	public Counter() {
	}
	
	private int Counter=0;

	public int getCounter() {
		this.Counter++;
		return this.Counter;
	}

	public void setCounter(int counter) {
		Counter = counter;
	}
}
