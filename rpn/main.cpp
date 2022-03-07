#include <stack>
#include <cctype>
#include <iostream>

using namespace std;


bool isoperator(int c) 
{
    if ('+' == c || '-' == c || '*' == c || '/' == c)
        return true;
    return false;
}

int operatorPriority(int c)
{
    if ('+' == c || '-' == c)
        return 1;

    if ('*' == c || '/' == c)
        return 2;

    return -1;
}

// 未校验括号是否配对
int infix2Rpn(const string &infix, string &rpn) 
{
    int ch, top;
    stack<int> stack;

    for (auto iter = infix.cbegin(); iter != infix.cend(); ++iter) {
        ch = *iter;

        if (isspace(ch))
            continue;

        if (isdigit(ch)) {
            rpn.push_back(ch);
            continue;
        }

        if (isoperator(ch)) {
            rpn.push_back(' ');
            while(!stack.empty()) {
                top = stack.top();
                if (operatorPriority(ch) > operatorPriority(top))
                    break;
                // 遇到低优先级操作符时才能确定前面的操作符可以生效
                stack.pop();
                rpn.push_back(top);
                rpn.push_back(' ');
            }
            // 当前运算符一定需要压栈，因为我们不能确定后面还有更高优先级的运算符
            stack.push(ch);
            continue;
        }

        if ('(' == ch) {
            stack.push(ch);
            continue;
        }

        if (')' == ch) {
            while(!stack.empty()) {
                top = stack.top();
                stack.pop();
                if(top == '(')
                    break;
                rpn.push_back(' ');
                rpn.push_back(top);
            }
        } else {
            return -1;
        }
    }

    while(!stack.empty()) {
        top = stack.top();
        rpn.push_back(' ');
        rpn.push_back(top);
        stack.pop();
    }

    return 0;
}


// 1. 遇到优先级不确定的压栈。
// 2. 栈中优先级大于等于当前优先级时，可以让栈中大于等于当前先级运的算符生效。
// 3. 当前优先级大于栈中优先级时并不能确定接下来的运算符优先级，因此不能生效。
// 4. 不考虑"()"情况下，栈底到栈顶运算符的优先级依次递增，且不存在相同的优先级，因此栈的最大长度与优先级有关。

int main() 
{
    int ret;
    string rpn;
    // 100 200 + 300 400 500 600 * - * - 700 -
    string infix = "100 + 200 - 300 * (400 - 500 * 600) -700";

    ret = infix2Rpn(infix, rpn);
    if (ret != 0) {
        return -1;
    }

    cout << rpn << endl;
    return 0;
}