import cmd
import shlex # 用于更好地解析带参数的命令
import board

tempList = [1,4,1,1,5,4,8,9,12,6,10,14,15,7,11,13]
PBoard = board.PlayP(tempList)
PBoard.printBoard()

class MyCalculator(cmd.Cmd):
    """一个简单的交互式计算器"""
    intro = "欢迎使用高级计算器。输入 help 或 ? 查看命令列表。\n"
    prompt = "(calc) "

    def do_add(self, arg):
        """执行加法运算，例如: add 10 20.5"""
        try:
            # shlex.split 可以正确处理带空格的参数
            args = shlex.split(arg)
            if len(args) != 2:
                print("错误：add 命令需要两个数字参数。")
                return
            a, b = map(float, args)
            print(f"结果: {a + b}")
        except ValueError:
            print("错误：请输入有效的数字。")

    def do_sub(self, arg):
        """执行减法运算，例如: sub 50 20"""
        # ... 类似的实现 ...
        print("减法功能待实现")

    def do_quit(self, arg):
        """退出程序"""
        print("再见！")
        return True # 返回 True 会终止 cmdloop

    # 默认处理未知命令
    def default(self, line):
        print(f"未知命令: {line}")
        
class PlayBoard(cmd.Cmd):
    intro = "欢迎使用2048试验田。\n"
    prompt = "(move) "
    def do_l(self,arg):
        tempBool = PBoard.goLeft()
        if(not tempBool):
            print("无法向左移动\n")
        else:
            print("向左移动成功\n")
            PBoard.printBoard()
            
    def do_r(self,arg):
        tempBool = PBoard.goRight()
        if(not tempBool):
            print("无法向右移动\n")
        else:
            print("向右移动成功\n")
            PBoard.printBoard()
    
    def do_u(self,arg):
        tempBool = PBoard.goUp()
        if(not tempBool):
            print("无法向上移动\n")
        else:
            print("向上移动成功\n")
            PBoard.printBoard()

    def do_d(self,arg):
        tempBool = PBoard.goDown()
        if(not tempBool):
            print("无法向下移动\n")
        else:
            print("向下移动成功\n")
            PBoard.printBoard()
    
    def do_quit(self, arg):
        """退出程序"""
        print("谢谢你的使用！")
        return True # 返回 True 会终止 cmdloop

    # 默认处理未知命令
    def default(self, line):
        print(f"未知命令: {line}")       
            
    
    

if __name__ == '__main__':
    #tempList = [0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0]
    #PBoard = board.PlayP(tempList)
    PlayBoard().cmdloop()
