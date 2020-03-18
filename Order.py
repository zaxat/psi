class Order:
    Order_content = [[0] * 4 for i in range(100)] #содержимое заказа ID продукта из меню/Название продукта/Цена продукта/Кол-во продуктов
    Content = 0 #Кол-во продуктов в заказе

    def setnumFood(self, seller, id, num): #Добавить продукт
        if self.checkID(id) == 0:
            if seller.Getmenu().getProductName(id) != 0: #Если продукта нету в заказе
                self.Order_content[self.Content][0] = id
                self.Order_content[self.Content][1] = seller.Getmenu().getProductName(id)
                self.Order_content[self.Content][2] = seller.Getmenu().CalculatePrice(id, num)
                self.Order_content[self.Content][3] = num
                self.Content=self.Content+1
                return self.generateOrder()
            else:
                return 'Неправильный ввод заказа'
        else: #Если продукт есть в заказе
            self.Order_content[self.FindID(id)][0] = id
            self.Order_content[self.FindID(id)][2] = seller.Getmenu().CalculatePrice(id, num)
            self.Order_content[self.FindID(id)][3] = num
            return self.generateOrder()


    def checkID(self,id):  #Функция на проверку существование продукта в заказе
        i = 0
        c=0
        while i < self.Content:
            if self.Order_content[i][0] == id:
                c=1
                break
            i=i+1
        return c

    def FindID(self,id): #Найти ID продукта в списке Order_content
        i = 0
        while i < self.Content:
            if self.Order_content[i][0] == id:
                break
        return i

    def generateOrder(self): #Создать заказ для вывода
        Output = ""
        i = 0
        Order_price = 0
        while i < self.Content:
            if self.Order_content[i][3] > 0:
                Output = Output + str(self.Order_content[i][1]) + " кол-во:" + str(self.Order_content[i][3]) + " цена:" + str(self.Order_content[i][2]) + "\n"
                Order_price = Order_price + self.Order_content[i][2]
            i = i + 1
        Output = Output + "Полная цена: " + str(Order_price) + "\n"
        Output = Output + ""
        return Output
