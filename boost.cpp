#include <iostream>
#include <boost/regex.hpp>
int main()
{
	std::string regstr = "a+";
	boost::regex expression(regstr);
	std::string testString="aaa";
	
	if(boost::regex_match(testString,expression))
	{
		std::cout << "Match" << std::endl;
	}
	else
	{
		std::cout << "Not Match" << std::endl;
	}
	return 0;
}
