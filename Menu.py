class Menu:

    Products = [[0] * 3 for i in range(100)] #Содержимое меню Название продукта/Цена продукта/Скрыт-открыт

    def __init__(self,n):
        self.name = n #Название меню
        self.numofproducts = 0 #Кол-во продуктов в меню

    def getMenuname(self): #Получить название меню
        return self.name

    def newProduct(self, name): #Новый продукт
        self.Products[self.numofproducts][0] = name #Ввод имени
        self.Products[self.numofproducts][2] = 0 #Скрыть заказ
        self.numofproducts+=1

    def setProductPrice(self, id, p): #Установить цену продукта
        self.Products[id][1] = p

    def CalculatePrice(self, id, num): #Подсчитать сумму продуктов
        return self.Products[id][1]*num

    def getProductName(self, id): #Получить название продукта
        return self.Products[id][0]

    def getNumofProduct(self): #Получить кол-во продуктов в меню
        return self.numofproducts

    def cover_uncover(self,id): #Скрыть/открыть продукт
        if self.Products[id][2] == 0:
            self.Products[id][2] = 1
        elif self.Products[id][2] == 1:
            self.Products[id][2] = 0

    def Printmenu_seller(self): #Вывести меню для продавца
        Output = "------------------------------\n"
        i = 0
        while i < self.numofproducts:
            if self.Products[i][2] == 0: #Если скрыт продукт
                Output = Output + str(i+1) + ". " + str(self.Products[i][0]) + " Цена: " + str(self.Products[i][1]) + " Скрыто\n"
            elif self.Products[i][2] == 1: #Открыт
                Output = Output + str(i + 1) + ". " + str(self.Products[i][0]) + " Цена: " + str(self.Products[i][1]) + "\n"
            i+=1
        Output = Output + "------------------------------\n"
        return Output

    def Printmenu_customer(self): #Вывести меню для покупателя
        Output = "------------------------------\n"
        i = 0
        while i < self.numofproducts:
            if self.Products[i][2] == 1: #Если продукт открыт
                Output = Output + str(i+1) + ". " + str(self.Products[i][0]) + " Цена: " + str(self.Products[i][1]) + "\n"
            i+=1
        Output = Output + "------------------------------\n"
        return Output

    def setProductname(self, id, n): #Изменить название продукта
        self.Products[id][0] = n

    def getcoverproduct(self, id): #Получить скрыт/открыт продукт
        return  self.Products[id][2]
