from Order import Order

class Buyer:
    numberOfOrders = 0 #Кол-во заказов у покупателя
    haveorder = 0 #Имеет ли пользователь заказ 0-нету/1-есть

    def getnumberOfOrders(self): #Получить кол-во заказов покупателя
        return self.numberOfOrders

    def addOrder(self): #Создать новый заказ или проверить на существование
        if self.haveorder == 0:
            self.numberOfOrders += 1
            self.Orders = Order()
            self.haveorder = 1
            return "Заказ создан"
        if self.haveorder == 1:
            return "Заказ уже существует"

    def getOrder(self): #Получить заказ
        return self.Orders

    def deleteOrder(self): #Удалить заказ
        del self.Orders
        self.haveorder = 0
        return "Заказ удален"

    def gethaveOrder(self): #Получить имеет ли покупатель заказ
        return self.haveorder

    def GetMenuContent(self, seller): #Получить меню
        return seller.getMenuContent()
