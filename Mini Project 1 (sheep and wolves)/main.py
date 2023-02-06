from SemanticNetsAgent import SemanticNetsAgent
from tester import test_solution

def test():
    #This will test your SemanticNetsAgent
	#with seven initial test cases.
    test_agent = SemanticNetsAgent()

    # test_solution(1,1,test_agent.solve(1, 1))
    # test_solution(2,2,test_agent.solve(2, 2))
    # test_solution(3,3,test_agent.solve(3, 3))
    # test_solution(5,3,test_agent.solve(5, 3))
    # test_solution(6,3,test_agent.solve(6, 3))
    # test_solution(7,3,test_agent.solve(7, 3))
    # test_solution(5,5,test_agent.solve(5, 5))
    print(test_agent.solve(1, 1))
    print(test_agent.solve(2, 2))
    print(test_agent.solve(3, 3))
    print(test_agent.solve(5, 3))
    print(test_agent.solve(6, 3))
    print(test_agent.solve(7, 3))
    print(test_agent.solve(5, 5))


if __name__ == "__main__":
    test()