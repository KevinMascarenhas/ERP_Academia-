# Menu de autenticação. Realiza login de usuários (Administrador, Aluno, Funcionário) na Academia Winner.

def tela_login(autenticar_uc):
    print("\n=== ACADEMIA WINNER ===")
    tentativas = 3
    while tentativas > 0:
        print("\n--- Login ---")
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        usuario = autenticar_uc.executar(email, senha)
        if usuario:
            print(f"\nBem-vindo(a), {usuario.get_nome()}! [{usuario.get_perfil()}]")
            return usuario

        tentativas -= 1
        print("Email ou senha inválidos.", end=" ")
        if tentativas > 0:
            print(f"Tentativas restantes: {tentativas}")
        else:
            print("Encerrando.")
    return None
