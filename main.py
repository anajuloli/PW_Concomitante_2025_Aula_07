from pydantic import ValidationError
from tabulate import tabulate
from usuarios.usuario_repo import UsuarioRepo
from usuarios.usuario import Usuario

def exibir_menu():
    print("\n--- Sistema de Gerenciamento de Usuários de Academia ---")
    print("a) Cadastrar Usuário")
    print("b) Listar Usuários")
    print("c) Alterar Usuário")
    print("d) Excluir Usuário")
    print("e) Sair")
    print("--------------------------------------------------------")

def obter_entrada_usuario(mensagem, tipo=str):
    while True:
        entrada = input(mensagem)
        try:
            if tipo == float:
                return float(entrada)
            elif tipo == int:
                return int(entrada)
            else:
                return entrada.strip()
        except ValueError:
            print(f"Entrada inválida. Por favor, insira um valor do tipo '{tipo.__name__}'.")

def cadastrar_usuario(repo: UsuarioRepo):
    print("\n--- Cadastro de Novo Usuário ---")
    try:
        nome = obter_entrada_usuario("Nome: ")
        email = obter_entrada_usuario("Email: ")
        peso = obter_entrada_usuario("Peso (kg): ", float)
        altura = obter_entrada_usuario("Altura (m): ", float)
        
        print("\nNíveis de atividade disponíveis:")
        print("- sedentário\n- leve\n- moderado\n- ativo\n- muito ativo")
        nivel_atividade = obter_entrada_usuario("Nível de atividade: ")

        novo_usuario = Usuario(nome=nome, email=email, peso=peso, altura=altura, nivel_atividade=nivel_atividade)

        usuario_id = repo.adicionar(novo_usuario)

        if usuario_id:
            print(f"Usuário '{novo_usuario.nome}' cadastrado com sucesso! ID: {usuario_id}")
        else:
            print("Falha ao cadastrar o usuário.")

    except ValidationError as e:
        print("\nErro de validação ao cadastrar usuário:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao cadastrar: {e}")

def listar_usuarios(repo: UsuarioRepo):
    print("\n--- Lista de Usuários Cadastrados ---")
    usuarios = repo.obter_todos()

    if usuarios:
        tabela = [[u.id, u.nome, u.email, f"{u.peso:.1f} kg", f"{u.altura:.2f} m", u.nivel_atividade] for u in usuarios]
        cabecalhos = ["ID", "Nome", "Email", "Peso", "Altura", "Nível de Atividade"]
        print(tabulate(tabela, headers=cabecalhos, tablefmt="grid", numalign="right", stralign="left"))
    else:
        print("Nenhum usuário cadastrado.")

def alterar_usuario(repo: UsuarioRepo):
    print("\n--- Alteração de Usuário ---")
    try:
        usuario_id = obter_entrada_usuario("ID do usuário a ser alterado: ", int)
        usuario_existente = repo.obter(usuario_id)

        if usuario_existente:
            print("\nDados atuais do usuário:")
            print(f"  Nome: {usuario_existente.nome}")
            print(f"  Email: {usuario_existente.email}")
            print(f"  Peso: {usuario_existente.peso:.1f} kg")
            print(f"  Altura: {usuario_existente.altura:.2f} m")
            print(f"  Nível de Atividade: {usuario_existente.nivel_atividade}")
            print("\nDigite os novos dados (deixe em branco para manter o valor atual):")

            nome = obter_entrada_usuario(f"Novo Nome ({usuario_existente.nome}): ") or usuario_existente.nome
            email = obter_entrada_usuario(f"Novo Email ({usuario_existente.email}): ") or usuario_existente.email
            
            peso_str = obter_entrada_usuario(f"Novo Peso ({usuario_existente.peso:.1f} kg): ")
            peso = float(peso_str) if peso_str else usuario_existente.peso

            altura_str = obter_entrada_usuario(f"Nova Altura ({usuario_existente.altura:.2f} m): ")
            altura = float(altura_str) if altura_str else usuario_existente.altura

            print("\nNíveis de atividade disponíveis:")
            print("- sedentário\n- leve\n- moderado\n- ativo\n- muito ativo")
            nivel_str = obter_entrada_usuario(f"Novo Nível de Atividade ({usuario_existente.nivel_atividade}): ")
            nivel_atividade = nivel_str if nivel_str else usuario_existente.nivel_atividade

            usuario_atualizado = Usuario(id=usuario_existente.id, nome=nome, email=email, 
                                        peso=peso, altura=altura, nivel_atividade=nivel_atividade)

            if repo.atualizar(usuario_atualizado):
                print(f"Usuário ID {usuario_id} atualizado com sucesso!")
            else:
                print(f"Falha ao atualizar o usuário ID {usuario_id}.")

        else:
            print(f"Usuário com ID {usuario_id} não encontrado.")

    except ValidationError as e:
        print("\nErro de validação ao alterar usuário:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except ValueError:
        print("Entrada inválida para ID, peso ou altura. A alteração foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao alterar: {e}")

def excluir_usuario(repo: UsuarioRepo):
    print("\n--- Exclusão de Usuário ---")
    try:
        usuario_id = obter_entrada_usuario("ID do usuário a ser excluído: ", int)

        usuario = repo.obter(usuario_id)
        if not usuario:
            print(f"Usuário com ID {usuario_id} não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir o usuário '{usuario.nome}' (ID: {usuario_id})? (s/N): ").lower()

        if confirmacao == 's':
            if repo.excluir(usuario_id):
                print(f"Usuário ID {usuario_id} excluído com sucesso.")
            else:
                print(f"Falha ao excluir o usuário ID {usuario_id}.")
        else:
            print("Exclusão cancelada.")

    except ValueError:
        print("ID inválido. A exclusão foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao excluir: {e}")

def main():
    repo = UsuarioRepo()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").lower().strip()

        if opcao == 'a':
            cadastrar_usuario(repo)
        elif opcao == 'b':
            listar_usuarios(repo)
        elif opcao == 'c':
            alterar_usuario(repo)
        elif opcao == 'd':
            excluir_usuario(repo)
        elif opcao == 'e':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()