#include <iostream>

class duck{
public:
	void quack(){
		std::cout << "quack I am a duck" << std::endl;
	}
};

int main(){
	duck d;
	for(int i=0; i<10; i++){
		d.quack();
	}
	int n;
	int i;
	for ( n=0 ; n!=3 ; n++)
	{
	   std::cout << "n:" << n << " i:" << i << ", ";
	}

	return 0;
}
