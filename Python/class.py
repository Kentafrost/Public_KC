class TEST:
    #コンストラクタからまず処理される。引数でselfはかならず入れる必要あり。self.～で変数指定。
    def __init__(self, num, num2):
        self.num = num
        self.num2 = num2
        
    def print_num(self):
        print("引数で渡された数字：{}".format(self.num))

        
    def AAA(self):
        print("引数で渡した数字の計算:" + str(self.num + self.num2))
        
    def __del__(self):
        print("デストラクタ")

test = TEST(10, 20) #インスタンスを生成
test.print_num()

def print_test(self):
    print("引数で渡された数字：{}".format(self))
    
    re = self * 3
    return re


test = print_test(10) 
print(test)


class TEST2(TEST):
    def print_num2_info(self):
        print("継承している")
        super().AAA() #指定した変数を親クラスのAAA()に渡す
                
        

#test.AAA()

#継承の練習
test2 = TEST2(10, 30) 
#ここまでではインスタンスを生成しただけなので、何も出力されない。この後の関数の指定がないと何も処理されない。

test2.print_num2_info()

del test

class practice:
    def __init__(self, calc_number1, calc_number2):
        self.calc_number1 = calc_number1
        self.calc_number2 = calc_number2
    
    def num(self):
        print(self.calc_number1)
        print(self.calc_number2)
    
    def __del__(self):
        print("terminated")
        

test3 = practice(100, 200)
test3.num()
del test3