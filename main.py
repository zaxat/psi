from Canteen import canteen
import telebot
import qrcode
import os

bot = telebot.TeleBot('1136875517:AAF1IUfabbUhFgin8lDFYWVqVmE8Mu46ors') #Токен телеграм бота
mria = canteen("Mria") #Создать столовую при запуске

Menukeyboard = telebot.types.ReplyKeyboardMarkup() #Создать клавиатуру
Menukeyboard.row('Создать заказ') #Создать строчку в клавиатуре
Menukeyboard.row('Посмотреть меню', 'Выбрать еду')
Menukeyboard.row('Вывод заказа')
Menukeyboard.row('Удалить заказ')
Menukeyboard.row('Отправить заказ')

Ordermenu = telebot.types.ReplyKeyboardMarkup()
Ordermenu.row('Изменить кол-во кол')
Ordermenu.row('Изменить кол-во бургеров')
Ordermenu.row('Изменить кол-во борщей')
Ordermenu.row('Назад')

Sendmenu_client = telebot.types.ReplyKeyboardMarkup()
Sendmenu_client.row('Отменить заказ')
Sendmenu_client.row('Вернуться в меню')

Sendmenu_seller = telebot.types.ReplyKeyboardMarkup()
Sendmenu_seller.row('Завершить заказ')
Sendmenu_seller.row('Отменить заказ')
Sendmenu_seller.row('Назад')

Seller_menu = telebot.types.ReplyKeyboardMarkup()
Seller_menu.row('Изменить меню')
Seller_menu.row('Работать с заказами')

Seller_workwithmenu = telebot.types.ReplyKeyboardMarkup()
Seller_workwithmenu.row('Добавить продукт')
Seller_workwithmenu.row('Изменить цену продукта', 'Изменить имя продукта')
Seller_workwithmenu.row('Скрыть/открыть продукт')
Seller_workwithmenu.row('Вывести меню')
Seller_workwithmenu.row('Назад')


@bot.message_handler(commands=['start']) #При начале работы с ботом
def start_message(message):
    if message.chat.id == 542778255: #Проверка на продавца
        mria.createseller()  # Создать продавца
        mria.getseller().Createmenu("Standart")  # Созлать меню
        bot.send_message(message.chat.id, 'Выберайте пункт меню:', reply_markup=Seller_menu) #Отправить сообщение и включить клавиатуру
        bot.register_next_step_handler(message, seller_menu) #Перейти к меню продавца
    else:
        bot.send_message(message.chat.id, '' + str(mria.createbuyer(message.chat.id)))
        bot.send_message(message.chat.id, 'Выберайте пункт меню:', reply_markup=Menukeyboard)
        bot.register_next_step_handler(message, menu)


def menu(message): #Меню покупателя
    temp_message = message.text
    if temp_message == 'Создать заказ':
        add_order(message)
    elif temp_message == 'Посмотреть меню':
        if mria.gethaveseller() == 1:
            bot.send_message(message.chat.id, mria.getbuyer(message.chat.id).GetMenuContent(mria.getseller()))
        else:
            bot.send_message(message.chat.id, "Меню не создано")
        bot.register_next_step_handler(message, menu)
    elif temp_message == 'Выбрать еду':
        if mria.gethaveseller() == 1:
            bot.send_message(message.chat.id, mria.getbuyer(message.chat.id).GetMenuContent(mria.getseller()))
        else:
            bot.send_message(message.chat.id, "Меню не создано")
        choose_food(message)
    elif temp_message == 'Вывод заказа':
        output(message)
    elif temp_message == 'Удалить заказ':
        delete_order(message)
    elif temp_message == 'Отправить заказ':
        send_order(message)
    else:
        bot.send_message(message.chat.id, "Неправильный ввод" ,reply_markup=Menukeyboard)
        bot.register_next_step_handler(message, menu)


def seller_menu_order(message): #Меню для работы с заказами продавца
    temp_message = message.text
    if temp_message == 'Завершить заказ':
        complete_order(message)
    elif temp_message == 'Отменить заказ':
        delete_order_by_seller(message)
    elif temp_message == 'Назад':
        bot.send_message(message.chat.id, "Выберайте пункт меню", reply_markup=Seller_menu)
        bot.register_next_step_handler(message, seller_menu)
    else:
        bot.register_next_step_handler(message, seller_menu_order)


def seller_menu(message): #Меню продавца
    temp_message = message.text
    if temp_message == 'Изменить меню':
        bot.send_message(message.chat.id, "Выберайте пункт меню", reply_markup=Seller_workwithmenu)
        bot.register_next_step_handler(message, seller_menu_workwithmenu)
    elif temp_message == 'Работать с заказами':
        bot.send_message(message.chat.id, "Выберайте пункт меню", reply_markup=Sendmenu_seller)
        bot.register_next_step_handler(message, seller_menu_order)
    else:
        bot.register_next_step_handler(message, seller_menu)


def seller_menu_workwithmenu(message): #Меню продавца для работы с меню
    temp_message = message.text
    if temp_message == 'Добавить продукт':
        bot.send_message(message.chat.id, 'Введите название продукта')
        bot.register_next_step_handler(message, getFoodname)
    elif temp_message == 'Изменить цену продукта':
        bot.send_message(message.chat.id, 'Введите номер продукта')
        bot.register_next_step_handler(message, getFoodID)
    elif temp_message == 'Вывести меню':
        bot.send_message(message.chat.id, mria.getseller().Getmenu().Printmenu_seller())
        bot.send_message(message.chat.id, "Выберайте пункт меню")
        bot.register_next_step_handler(message, seller_menu_workwithmenu)
    elif temp_message == 'Скрыть/открыть продукт':
        bot.send_message(message.chat.id, 'Введите номер продукта')
        bot.register_next_step_handler(message, getFoodIDforHide)
    elif temp_message == 'Изменить имя продукта':
        bot.send_message(message.chat.id, 'Введите номер продукта')
        bot.register_next_step_handler(message, getFoodIDforChangename)
    elif temp_message == 'Назад':
        bot.send_message(message.chat.id, "Выберайте пункт меню", reply_markup=Seller_menu)
        bot.register_next_step_handler(message, seller_menu)
    else:
        bot.register_next_step_handler(message, seller_menu_workwithmenu)


def client_send_menu(message): #Меню покупателя при отправленном заказе
    temp_message = message.text
    if temp_message == 'Отменить заказ':
        bot.send_message(message.chat.id, 'Выберайте пункт меню:', reply_markup=Menukeyboard)
        if mria.getbuyer(message.chat.id).gethaveOrder() == 1:
            bot.send_message(542778255, 'Заказ номер: ' + str(mria.collectOrderNumber(message.chat.id)) + ' отменен')
        delete_order(message)
    elif temp_message == 'Вернуться в меню':
        if mria.getbuyer(message.chat.id).gethaveOrder() == 0:
            bot.send_message(message.chat.id, 'Выберайте пункт меню:', reply_markup=Menukeyboard)
            bot.register_next_step_handler(message, menu)
        else:
            bot.send_message(message.chat.id, 'Надо что-бы заказ удалили или завершили')
            bot.register_next_step_handler(message, client_send_menu)
    else:
        bot.register_next_step_handler(message, client_send_menu)


def add_order(message): #Создать заказ
    if mria.getbuyer(message.chat.id).gethaveOrder() == 0:
        bot.send_message(message.chat.id,
                         'Номер заказа: ' + str(mria.collectOrderNumber(message.chat.id)) + "\n"
                         + mria.getbuyer(message.chat.id).addOrder())
    else:
        bot.send_message(message.chat.id, "У вас уже есть заказ!")
    bot.register_next_step_handler(message, menu)


def output(message): #Вывод заказа
    if mria.getbuyer(message.chat.id).gethaveOrder() == 1:
        bot.send_message(message.chat.id,
                         'Номер заказа: ' + str(mria.collectOrderNumber(message.chat.id)) + "\n"
                         + mria.getbuyer(message.chat.id).getOrder().generateOrder())
    else:
        bot.send_message(message.chat.id, "Заказ не создан")
    bot.register_next_step_handler(message, menu)


def delete_order(message): #Удалить заказ
    if mria.getbuyer(message.chat.id).gethaveOrder() == 1:
        bot.send_message(message.chat.id, '' + str(mria.getbuyer(message.chat.id).deleteOrder()))
    else:
        bot.send_message(message.chat.id, 'У вас нет заказа')
    bot.register_next_step_handler(message, menu)


def send_order(message): #Отправить заказ
    if mria.getbuyer(message.chat.id).gethaveOrder() == 1:
        bot.send_message(message.chat.id,
                         'Номер заказа: ' + str(mria.collectOrderNumber(message.chat.id)) + "\n" + mria.getbuyer(
                             message.chat.id).getOrder().generateOrder())
        bot.send_message(542778255,
                         'Номер заказа: ' + str(mria.collectOrderNumber(message.chat.id)) + "\n" + mria.getbuyer(
                             message.chat.id).getOrder().generateOrder())
        bot.send_message(message.chat.id, 'Заказ отправлен. Ожидайте подтверждения=)', reply_markup=Sendmenu_client)
        bot.register_next_step_handler(message, client_send_menu)
    else:
        bot.send_message(message.chat.id, "Заказ не создан")
        bot.register_next_step_handler(message, menu)


def complete_order(message): #Завершить заказ покупателем
    bot.send_message(542778255, "Введите номер завершонного заказа")
    bot.register_next_step_handler(message, getCompletenumber)


def delete_order_by_seller(message): #Удалить заказ покупателем
    bot.send_message(542778255, "Введите номер отмененного заказа")
    bot.register_next_step_handler(message, getcancelnumber)


def getCompletenumber(message): #Получить номер для завершение заказа
    try:
        temp_number = int(message.text)
        print(mria.findBuyerbyOrder(temp_number))
        if mria.findBuyerbyOrder(temp_number) != 0:
            if mria.getbuyer(mria.findBuyerbyOrder(temp_number)).gethaveOrder() == 1:

                qr = qrcode.QRCode(version=1, box_size=10, border=4) #Создание QR кода
                qr.add_data('Номер заказа: ' + str(mria.collectOrderNumber(mria.findBuyerbyOrder(temp_number))) +
                            "\n" + mria.getbuyer(mria.findBuyerbyOrder(temp_number)).getOrder().generateOrder())

                qr.make(fit=True)
                x = qr.make_image()

                qr_file = os.path.join('', "QR" + ".jpg")
                img_file = open(qr_file, 'wb')
                x.save(img_file, 'JPEG')
                img_file.close()
                img_file2 = open('QR.jpg', 'rb')
                bot.send_photo(mria.findBuyerbyOrder(temp_number), img_file2)  #Отправка QR кода
                img_file2.close()

                mria.getbuyer(mria.findBuyerbyOrder(temp_number)).deleteOrder()
                bot.send_message(message.chat.id, 'Заказ завершён')
                bot.send_message(mria.findBuyerbyOrder(temp_number), 'Заказ завершён')
            else:
                bot.send_message(message.chat.id, 'Данный заказ не существует')
            bot.register_next_step_handler(message, seller_menu_order)
        else:
            bot.send_message(message.chat.id, 'Данный заказ не существует')
            bot.register_next_step_handler(message, seller_menu_order)
    except:
        bot.send_message(message.chat.id, 'Неправильный ввод')
        bot.register_next_step_handler(message, seller_menu_order)


def getcancelnumber(message): #Получить номер для отменение заказа
    try:
        temp_number = int(message.text)
        if mria.findBuyerbyOrder(temp_number) != 0:
            if mria.getbuyer(mria.findBuyerbyOrder(temp_number)).gethaveOrder() == 1:
                mria.getbuyer(mria.findBuyerbyOrder(temp_number)).deleteOrder()
                bot.send_message(message.chat.id, 'Заказ отменен')
                bot.send_message(mria.findBuyerbyOrder(temp_number), 'Заказ отменен')
            else:
                bot.send_message(message.chat.id, 'Данный заказ не существует')
            bot.register_next_step_handler(message, seller_menu_order)
        else:
            bot.send_message(message.chat.id, 'Данный заказ не существует')
            bot.register_next_step_handler(message, seller_menu_order)
    except:
        bot.send_message(message.chat.id, 'Неправильный ввод')
        bot.register_next_step_handler(message, seller_menu_order)


def choose_food(message): #Выбрать продукт
    if mria.getbuyer(message.chat.id).gethaveOrder() == 1:
        if mria.gethaveseller() == 1:
            if mria.getseller().Getmenu().getNumofProduct() != 0:
                bot.send_message(message.chat.id, 'Введите ID еды:')
                bot.register_next_step_handler(message, getID)
            else:
                bot.send_message(message.chat.id, "Меню не создано")
                bot.register_next_step_handler(message, menu)
        else:
            bot.send_message(message.chat.id, "Меню не создано")
            bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.chat.id, "Заказ не создан")
        bot.register_next_step_handler(message, menu)


def getID(message): #Получить продукт
    try:
        temp_number = int(message.text)-1
        if temp_number >= 0:
            mria.settemp(message.chat.id, temp_number)
            bot.send_message(message.chat.id, 'Введите кол-во еды: ')
            bot.register_next_step_handler(message, getnumFood)
        else:
            bot.send_message(message.from_user.id, 'Неправильное значение, введите ещё раз')
            bot.register_next_step_handler(message, getID)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getID)


def getnumFood(message): #Ввести кол-во продуктов
    try:
        temp_number = int(message.text)
        if temp_number >= 0:
            if mria.getbuyer(message.chat.id).getOrder().setnumFood(mria.getseller(), int(mria.gettemp(message.chat.id)), temp_number) == 'Неправильный ввод заказа':
                bot.send_message(message.chat.id, 'Неправильный ввод заказа')
            else:
                bot.send_message(message.chat.id,
                                 'Номер заказа: ' + str(mria.collectOrderNumber(message.chat.id)) + "\n"
                                 + mria.getbuyer(message.chat.id).getOrder().generateOrder())
            bot.register_next_step_handler(message, menu)
        else:
            bot.send_message(message.from_user.id, 'Неправильное значение, введите ещё раз')
            bot.register_next_step_handler(message, getnumFood)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getnumFood)


def getFoodname(message): #Получить название продукта
    temp = message.text
    mria.getseller().Getmenu().newProduct(temp)
    bot.send_message(message.chat.id, mria.getseller().Getmenu().Printmenu_seller())
    bot.send_message(message.chat.id, 'Выберайте пункт меню')
    bot.register_next_step_handler(message, seller_menu_workwithmenu)


def getFoodID(message): #Получить ID продукта
    try:
        temp_number = int(message.text)
        if temp_number >= 0:
            mria.settempseller(temp_number - 1)
            bot.send_message(message.chat.id, 'Введите цену: ')
            bot.register_next_step_handler(message, getFoodPrice)
        elif temp_number == 0:
            bot.send_message(message.chat.id, 'Возвращаемся в меню')
            bot.register_next_step_handler(message, menu)
        else:
            bot.send_message(message.from_user.id, 'Неправильное значение, введите ещё раз')
            bot.register_next_step_handler(message, getFoodID)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getFoodID)


def getFoodPrice(message): #Получить цену продукта
    try:
        temp_number = int(message.text)
        if temp_number >= 0:
            mria.getseller().Getmenu().setProductPrice(mria.gettempseller(), temp_number)
            bot.send_message(message.chat.id, mria.getseller().Getmenu().Printmenu_seller())
            bot.send_message(message.chat.id, 'Выберайте пункт меню')
            bot.register_next_step_handler(message, seller_menu_workwithmenu)
        else:
            bot.send_message(message.from_user.id, 'Неправильное значение, введите ещё раз')
            bot.register_next_step_handler(message, getFoodPrice)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getFoodPrice)


def getFoodIDforHide(message): #Получить ID продукта что бы его скрыть/открыть
    try:
        temp_number = int(message.text)
        if temp_number > 0:
            mria.getseller().Getmenu().cover_uncover(temp_number - 1)
            bot.send_message(message.chat.id, 'Возвращаемся в меню')
            bot.register_next_step_handler(message, seller_menu_workwithmenu)
        elif temp_number == 0:
            bot.send_message(message.chat.id, 'Возвращаемся в меню')
            bot.register_next_step_handler(message, seller_menu_workwithmenu)
        else:
            bot.send_message(message.chat.id, 'Неправильное значение, введите ещё раз')
            bot.register_next_step_handler(message, getFoodIDforHide)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getFoodIDforHide)


def getFoodIDforChangename(message): #Получить ID продукта что бы изменить имя
    try:
        temp_number = int(message.text)
        if temp_number >= 0:
            mria.settempseller(temp_number - 1)
            bot.send_message(message.chat.id, 'Введите название: ')
            bot.register_next_step_handler(message, getFoodNameforChange)
        elif temp_number == 0:
            bot.send_message(message.chat.id, 'Возвращаемся в меню')
            bot.register_next_step_handler(message, seller_menu_order)
        else:
            bot.send_message(message.from_user.id, 'Неправильное значение, введите ещё раз')
            bot.register_next_step_handler(message, getFoodIDforChangename)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getFoodIDforChangename)


def getFoodNameforChange(message): #Получить продукт что бы поменять название
    try:
        temp_text = message.text
        mria.getseller().Getmenu().setProductname(mria.gettempseller(), temp_text)
        bot.send_message(message.chat.id, mria.getseller().Getmenu().Printmenu_seller())
        bot.send_message(message.chat.id, 'Выберайте пункт меню')
        bot.register_next_step_handler(message, seller_menu_workwithmenu)
    except Exception:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, getFoodNameforChange)


bot.polling(none_stop=True, interval=0)
