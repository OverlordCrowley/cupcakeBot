import sqlite3



    # def auth(self):
    # Проверяем, есть ли юзер в базе
    #    result = self.cursor.execute("SELECT * FROM `APC_p_20_51b_admins` WHERE `Name` = ?", (self.login,), "WHERE `Pass` = ?", (self.password,))
    #    return bool(len(result.fetchall()))






   # def get_user_id(self, user_id):
        #Достаем id юзера в базе по его user_id
   #     result = self.cursor.execute("SELECT `id` FROM `APC_p_20_51b_admins` WHERE `user_id` = ?", (user_id,))
    #    return result.fetchone()[0]

  #  def add_user(self, user_id):
        #Добавляем юзера в базу
  #      self.cursor.execute("INSERT INTO `APC_p_20_51b_admins` (`user_id`) VALUES (?)", (user_id,))
   #     return self.conn.commit()


 #   def close(self):
        #Закрываем соединение с БД
   #     self.connection.close()