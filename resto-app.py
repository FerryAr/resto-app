############################################################################################
# Ujian Akhir Semester Praktikum Pemrograman Dasar Kelas C                                 #
# Anggota Kelompok                                                                         #
# 1. Azriel Akbar Ferry Ardiansyah KW (202351099)                                          #
# 2. Pandu Satrio Witjaksono (202351083)                                                   #
# 3. Nurul Akbar Ismail (202351103)                                                        #
############################################################################################

import json
import bcrypt

isLogin = False
activeUsername = ""

def readUserJson():
    try:
        with open('user.json') as f:
            data = json.load(f)
        return data
    except:
        return False
    
def writeUserJson(data):
    try:
        with open('user.json', 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def readProductJson():
    try:
        with open('product.json') as f:
            data = json.load(f)
        return data
    except:
        return False

def writeProductJson(data):
    try:
        with open('product.json', 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False
    
def readCartJson():
    try:
        with open('cart.json') as f:
            data = json.load(f)
        return data
    except:
        return False
    
def writeCartJson(data):
    try:
        with open('cart.json', 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def registerUser(username, password):
    data = readUserJson()
    for user in data['user']:
        if user['username'] == username:
            return False
    hashed_password = bcrypt.hashpw(bytes(password.encode('utf-8')), bcrypt.gensalt(rounds=12))
    new_user = {
        "username": username,
        "password": hashed_password.decode('utf-8')
    }
    data['user'].append(new_user)
    writeUserJson(data)
    
    cartData = readCartJson()
    cartData['cart'].append({
        "username": username,
        "list": []
    })
    writeCartJson(cartData)
    
    return True

def loginUser(username: str, password: str):
    data = readUserJson()
    for user in data['user']:
        check_password = bcrypt.checkpw(bytes(password.encode('utf-8')), user['password'].encode('utf-8'))
        if user['username'] == username and check_password:
            global isLogin
            global activeUsername
            isLogin = True
            activeUsername = username
            return True
    return False

def createProduct(name: str, price: int, supply: int, demand: int, multiplier: float):
    try:
        data = readProductJson()
        idProduct = len(data['products']) + 1
        new_product = {
            "id": idProduct,
            "name": name,
            "price": price,
            "supply": supply,
            "demand": demand,
            "multiplier": multiplier,
        }
        data['products'].append(new_product)
        writeProductJson(data)
        return True
    except:
        return False

def readProduct():
    data = readProductJson()
    return data['products']

def readProductById(idProduct: int):
    data = readProduct()
    for product in data:
        if product['id'] == idProduct:
            return product

    return False

def updateProduct(idProduct: int, name: str, price: int, supply: int, demand: int, multiplier: float):
    try:
        data = readProductJson()
        for product in data['products']:
            if product['id'] == idProduct:
                product['name'] = name
                product['price'] = price
                product['supply'] = supply
                product['demand'] = demand
                product['multiplier'] = multiplier
            else:
                continue
        writeProductJson(data)
        return True
    except:
        return False

def deleteProduct(idProduct: int):
    try:
        data = readProductJson()
        for product in data['products']:
            if product['id'] == idProduct:
                data['products'].remove(product)
            else:
                continue
        writeProductJson(data)
        return True
    except:
        return False

def countPriceBySupplyDemand(price: int, supply: int, demand: int, multiplier: float):
    price_change = (demand - supply) * multiplier
    adjusted_price = price + price_change
    return max(0, adjusted_price)

def countPriceByDemand(price: int, demand: int, multiplier: float):
    price_change = demand * multiplier
    adjusted_price = price + price_change
    return max(0, adjusted_price)

def listProduct():
    print("\033c")
    productList = readProduct()
    print("="*20)
    print("Daftar Menu")
    print("="*20)
    for product in productList:
        productPrice = countPriceBySupplyDemand(product['price'], product['supply'], product['demand'], product['multiplier'])
        percentDiff = (productPrice - product['price']) / product['price'] * 100
        red = "\033[1;31m"
        green = "\033[1;32m"
        reset = "\033[0;0m"
        if percentDiff > 0:
            percentDiff = green + "+" + str(percentDiff) + "%" + reset
        else:
            percentDiff = red + str(percentDiff) + "%" + reset
        print(f"{product['id']}. {product['name']} - {productPrice} ({percentDiff})")
    print("="*20)
    
def readCart():
    data = readCartJson()
    return data['cart']

def addToCart(idProduct: int, qty: int, username: str):
    try:
        data = readCartJson()
        for cart in data['cart']:
            if cart['username'] == username:
                for product in cart['list']:
                    if product['id'] == idProduct:
                        product['qty'] += qty
                        writeCartJson(data)
                        return True
                cart['list'].append({
                    "id": idProduct,
                    "qty": qty
                })
                writeCartJson(data)
            else:
                continue
        return True
    except:
        return False

def deleteCart(idProduct: int, username: str):
    try:
        data = readCartJson()
        for cart in data['cart']:
            if cart['username'] == username:
                for product in cart['list']:
                    if product['id'] == idProduct:
                        cart['list'].remove(product)
                        writeCartJson(data)
        return True
    except:
        return False

def listCart(username: str):
    print("\033c")
    cartList = readCart()
    productList = readProduct()
    print("="*20)
    print("Keranjang Belanja")
    print("="*20)
    total = 0
    for cart in cartList:
        if cart['username'] == username:
            for product in cart['list']:
                for p in productList:
                    if product['id'] == p['id']:
                        productPrice = countPriceBySupplyDemand(p['price'], p['supply'], p['demand'], p['multiplier'])
                        total += productPrice * product['qty']
                        print(f"{p['name']} - {productPrice} x {product['qty']}")
    print("="*20)
    print(f"Total: {total}")
    print("="*20)
    
def checkout(username: str):
    print("\033c")
    cartList = readCartJson()
    product = readProductJson()
    print("="*20)
    print("Checkout")
    print("="*20)
    listCart(username)
    confirm = input("Apakah anda yakin ingin checkout? (y/n)")
    if confirm == "y":
        print("Checkout berhasil!")
        for c in cartList['cart']:
            if c['username'] == username:
                for ca in c['list']:
                    for p in product['products']:
                        if ca['id'] == p['id']:
                            p['supply'] -= ca['qty']
                            p['demand'] += ca['qty']
                c['list'] = []
        writeCartJson(cartList)
        writeProductJson(product)
    else:
        print("Checkout dibatalkan!")
        
def adminMenu():
    while True:
        print("\033c")
        print("="*20)
        print("Admin Menu")
        print("="*20)
        print("1. Tambah Menu")
        print("2. Lihat Semua Menu")
        print("3. Keluar")
        print("="*20)
        choice = input("Pilihan: ")
        if choice == "1":
            name = input("Nama Menu: ")
            price = int(input("Harga: "))
            supply = int(input("Supply: "))
            demand = int(input("Demand: "))
            multiplier = float(input("Multiplier: "))
            createProduct(name, price, supply, demand, multiplier)
            print("Menu berhasil ditambahkan!")
        elif choice == "2":
            while True:
                listProduct()
                print("1. Edit Menu")
                print("2. Hapus Menu")
                print("3. Kembali")
                choiceList = input("Pilihan: ")
                if choiceList == "1":
                    idProduct = int(input("ID Menu: "))
                    name = input("Nama Menu: ")
                    price = int(input("Harga: "))
                    supply = int(input("Supply: "))
                    demand = int(input("Demand: "))
                    multiplier = float(input("Multiplier: "))
                    if idProduct == "":
                        print("ID Menu tidak boleh kosong!")
                        continue
                    if name == "":
                        name = readProductById(idProduct)['name']
                    if price == "":
                        price = readProductById(idProduct)['price']
                    if supply == "":
                        supply = readProductById(idProduct)['supply']
                    if demand == "":
                        demand = readProductById(idProduct)['demand']
                    if multiplier == "":
                        multiplier = readProductById(idProduct)['multiplier']
                    updateProduct(idProduct, name, price, supply, demand, multiplier)
                    print("Menu berhasil diubah!")
                elif choiceList == "2":
                    idProduct = int(input("ID Menu: "))
                    if idProduct == "":
                        print("ID Menu tidak boleh kosong!")
                        continue
                    deleteProduct(idProduct)
                    print("Menu berhasil dihapus!")
                elif choiceList == "3":
                    break
                else:
                    print("Pilihan tidak tersedia!")
        elif choice == "3":
            break
        else:
            print("Pilihan tidak tersedia!")
            
def userMenu():
    while True:
        print("\033c")
        print("="*20)
        print("User Menu")
        print("="*20)
        print("1. Lihat Semua Menu")
        print("2. Lihat Keranjang Belanja")
        print("3. Checkout")
        print("4. Keluar")
        print("="*20)
        choice = input("Pilihan: ")
        if choice == "1":
            while True:
                listProduct()
                print("1. Tambah Menu ke Keranjang")
                print("2. Kembali")
                choiceList = input("Pilihan: ")
                if choiceList == "1":
                    idProduct = int(input("ID Menu: "))
                    if idProduct == "":
                        print("ID Menu tidak boleh kosong!")
                        continue
                    qty = int(input("Jumlah: "))
                    if qty == "":
                        print("Jumlah tidak boleh kosong!")
                        continue
                    addToCart(idProduct, qty, activeUsername)
                    print("Menu berhasil ditambahkan ke keranjang!")
                elif choiceList == "2":
                    break
                else:
                    print("Pilihan tidak tersedia!")
        elif choice == "2":
            while True:
                listCart(activeUsername)
                print("1. Pilih Menu yang ingin dihapus")
                print("2. Kembali")
                choiceList = input("Pilihan: ")
                if choiceList == "1":
                    idProduct = int(input("ID Menu: "))
                    if idProduct == "":
                        print("ID Menu tidak boleh kosong!")
                        continue
                    deleteCart(idProduct, activeUsername)
                    print("Menu berhasil dihapus dari keranjang!")
                elif choiceList == "2":
                    break
                else:
                    print("Pilihan tidak tersedia!")
        elif choice == "3":
            checkout(activeUsername)
        elif choice == "4":
            break
        else:
            print("Pilihan tidak tersedia!")
            
def main():
    print("\033c")
    while True:
        print("="*20)
        print("== Resto APP ==")
        print("="*20)
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        print("="*20)
        choice = input("Pilihan: ")
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if loginUser(username, password):
                print("Login berhasil!")
                if username == "admin":
                    adminMenu()
                else:
                    userMenu()
            else:
                print("Username atau password salah!")
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            if registerUser(username, password):
                print("Register berhasil!")
            else:
                print("Username sudah terdaftar!")
        elif choice == "3":
            break
        else:
            print("Pilihan tidak tersedia!")
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program dihentikan oleh user!")