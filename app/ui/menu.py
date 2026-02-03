def mostrar_menu():
    print("\n" + "=" * 35)
    print("🤖 Email Monitor Agent - Menu")
    print("=" * 35)
    print("1️⃣  Resumo de emails recebidos hoje")
    print("2️⃣  Emails sem resposta nos últimos 7 dias")
    print("3️⃣  Status dos usuários da corporação")
    print("0️⃣  Sair")
    print("=" * 35)

    return input("👉 Escolha uma opção: ").strip()
