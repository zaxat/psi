from Menu import Menu

class Seller:

    def Createmenu(self, n): #Создать меню
        self.menu = Menu(n)

    def Getmenu(self): #Получить меню
        return self.menu

    def getMenuContent(self): #Вывод меню для пользователя
        return self.menu.Printmenu_customer()
