# -*- encoding=utf-8 -*- 
'''
Created on Mar 15, 2014

@author: tonyzhang
'''

__all__ = ['Ahocorasick', ]

class Node(object):
    
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        
class Ahocorasick(object):
    
    def __init__(self):
        self.__root = Node()
        
    def addWord(self, word):
        '''
            @param word: add word to Tire tree 
                            添加关键词到Tire树中
        '''
        tmp = self.__root
        for i in range(0, len(word)):
            if not tmp.next.has_key(word[i]):
                tmp.next[word[i]] = Node()
            tmp = tmp.next[word[i]]
        tmp.isWord = True
    
    def make(self):
        '''
            build the fail function 
            构建自动机，失效函数
        '''
        tmpQueue = []
        tmpQueue.append(self.__root)
        while(len(tmpQueue) > 0):
            temp = tmpQueue.pop()
            p = None
            for k, v in temp.next.items():
                if temp == self.__root:
                    temp.next[k].fail = self.__root
                else:
                    p = temp.fail
                    while p is not None:
                        if p.next.has_key(k):
                            temp.next[k].fail = p.next[k]
                            break
                        p = p.fail
                    if p is None :
                        temp.next[k].fail = self.__root
                tmpQueue.append(temp.next[k])
    
    def search(self, content):
        '''
            @return: a list of tuple,the tuple contain the match start and end index
        '''
        p = self.__root
        result = []
        startWordIndex = 0
        endWordIndex = -1
        currentPosition = 0
        
        while currentPosition < len(content):
            word = content[currentPosition]
            # 检索状态机，直到匹配
            while p.next.has_key(word) == False and p != self.__root:
                p = p.fail
            
            if p.next.has_key(word):
                if p == self.__root:
                    # 若当前节点是根且存在转移状态，则说明是匹配词的开头，记录词的起始位置
                    startWordIndex = currentPosition
                # 转移状态机的状态
                p = p.next[word]
            else:
                p = self.__root
            
            if p.isWord:
                # 若状态为词的结尾，则把词放进结果集
                result.append((startWordIndex, currentPosition))
            
            currentPosition += 1
        return result
    
    def replace(self, content):
        '''
            
        '''
        replacepos = self.search(content)
        result = content
        for i in replacepos:
            result = result[0:i[0]] + (i[1] - i[0] + 1) * u'*' + content[i[1] + 1:]
        return result


if __name__ == '__main__':
    ah = Ahocorasick()
    ah.addWord(u'测试')
    ah.addWord(u"我是")
    ah.make()
    print ah.search(u'测试123我是好人')
