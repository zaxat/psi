from Buyer import Buyer
from Seller import Seller


class canteen:
    buyerslst = [[0] * 4 for i in range(4000)]  #Создать список с ИД пользователя/Обращение к классу Buyer/Заказ закрепленный за пользователем/Временное число закрепленное за пользователем
    haveseller = 0 #Имеет ли столовая продавца
    temp = 0 #Временное число для продавца
    def __init__(self, n): #Конструктор
        self.canteenName = n #Имя столовой
        self.numberofbuyers = 0 #Кол-во покупателей


    def createbuyer(self, id): #Создать покупателя
        i = 0
        c = 1
        while i<self.numberofbuyers: #Проверка на существование покупателя
            if self.buyerslst[i][0] == id: #Если есть
                return "Мы тебя уже знаем"
                break
            else:
                c=1
            i+=1
        if c == 1: #Если нету
            self.buyerslst[self.numberofbuyers][0] = id
            self.buyerslst[self.numberofbuyers][1] = Buyer()
            self.numberofbuyers = self.numberofbuyers+1
            return "Успешно зарегистрирован"


    def getbuyer(self,id): #Получить покупателя
        i = 0
        while i<self.numberofbuyers:
            if self.buyerslst[i][0] == id:
                break;
            i+=1;
        return self.buyerslst[i][1]


    def createseller(self): #Создать продавца
        self.seller = Seller()
        self.haveseller = 1


    def getseller(self): #Получить продавца
        return self.seller


    def gethaveseller(self): #Получить имеет ли столовая подавца
        return self.haveseller


    def collectOrderNumber(self, id): #Создать новый номер заказа или найти существуеший
        i = 0
        y = 0
        numberoforders = 0
        while i < self.numberofbuyers:
            if self.buyerslst[i][0] == id:
                if self.buyerslst[i][1].gethaveOrder() == 0:
                    while y < self.numberofbuyers:
                        numberoforders = numberoforders + int(self.buyerslst[y][1].getnumberOfOrders())
                        y += 1
                    self.buyerslst[i][2] = numberoforders
                    break
                else:
                    numberoforders = self.buyerslst[i][2]
                    break
            i +=1
        return numberoforders

    def settemp(self, id, temp): #Установить временную переменную
        i = 0
        while i < self.numberofbuyers:
            if self.buyerslst[i][0] == id:
                self.buyerslst[i][3] = temp
                break
            i+=1

    def gettemp(self, id): #Получить временную переменную
        i = 0
        while i < self.numberofbuyers:
            if self.buyerslst[i][0] == id:
                break
            i += 1
        return self.buyerslst[i][3]

    def findBuyerbyOrder(self,o): #Найти покупателя за заказом
        i = 0
        p = 0
        while i < self.numberofbuyers:
            if self.buyerslst[i][2] == o:
                p = self.buyerslst[i][0]
                break
            i+=1
        return p

    def settempseller(self, t): #Установить временную переменную продовца
        self.temp = t

    def gettempseller(self): #Получить временную переменную продовца
        return self.temp
