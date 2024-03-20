import pytest
class Test:
    @pytest.fixture(scope='class',autouse=True)
    def test_meth(self):
        print("my fixture is called")
    def test_method1(self):

        print("1st is called")

    def test_method2(self):
        print("2nd is called")


#obj1 = Test()