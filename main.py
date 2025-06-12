import random
import time

class StoryNode:
    """
    Representa um nó na árvore da história. Cada nó contém o texto da história,
    as opções para o jogador e os nós filhos que correspondem a cada escolha.
    """
    def __init__(self, text, choices=None, action=None):
        self.text = text
        self.choices = choices if choices else {}
        # A ação é uma tupla: (descrição_da_ação, limite_de_sucesso, nó_de_sucesso, nó_de_falha)
        self.action = action
        self.is_ending = not (self.choices or self.action)

def roll_dice(threshold):
    """
    Simula uma rolagem de dados para determinar o sucesso de uma ação.
    Gera um número aleatório de 0 a 100.
    Retorna True se o número for maior que o 'threshold', senão False.
    """
    roll = random.randint(0, 100)
    print(f"\n🎲 Você precisava de mais de {threshold} e rolou {roll}. 🎲")
    time.sleep(1)
    if roll > threshold:
        print("...Sucesso!")
        return True
    else:
        print("...Falha!")
        return False

# --- Finais da História ---
end_game_hero = StoryNode(
    "🎉 VOCÊ VENCEU! 🎉\nCom a gangue derrotada e o dinheiro recuperado, você retorna para TomasBurgo como um herói. O Prefeito Davi organiza uma festa em sua homenagem e sua lenda como o xerife que salvou a cidade é contada por gerações."
)

end_game_death_ambush = StoryNode(
    "GAME OVER\nA escuridão das cavernas foi a última coisa que você viu. A gangue era numerosa e estava preparada. Sua jornada termina aqui."
)

end_game_death_lookout = StoryNode(
    "GAME OVER\nO vigia foi mais rápido no gatilho. Enquanto você caía, seu último pensamento foi sobre a cidade que não conseguiu salvar. A poeira do desfiladeiro cobre seu corpo."
)

end_game_death_showdown = StoryNode(
    "GAME OVER\nApesar de sua bravura, a Gangue do Chapéu Preto era implacável. No tiroteio final, eles levaram a melhor. TomasBurgo perdeu seu xerife e sua esperança."
)

# --- Caminhos da História ---

# NÓ: Confronto Final
final_showdown_surprise = StoryNode(
    text="Você invade o esconderijo pegando a gangue de surpresa! Eles se atrapalham para pegar as armas.",
    action=("Vencer o tiroteio final.", 40, end_game_hero, end_game_death_showdown)
)

final_showdown_assault = StoryNode(
    text="A gangue já esperava por você! Tiros ecoam por todo o esconderijo assim que você entra.",
    action=("Sobreviver ao tiroteio e recuperar o dinheiro.", 65, end_game_hero, end_game_death_showdown)
)

# NÓ: Desfiladeiro
canyon_confront_lookout = StoryNode(
    text="Você encara o vigia. Ele cospe no chão e leva a mão ao coldre. 'Você não deveria estar aqui, xerife.'",
    action=("Ser mais rápido no duelo.", 50, final_showdown_assault, end_game_death_lookout)
)

canyon_sneak = StoryNode(
    text="Você tenta se mover pelas sombras, usando as rochas como cobertura para passar pelo vigia sem ser notado.",
    action=("Passar furtivamente pelo vigia.", 60, final_showdown_surprise, final_showdown_assault)
)

canyon_diversion = StoryNode(
    text="Você pega uma pedra e a joga para longe, criando um barulho que chama a atenção do vigia. Ele se afasta para investigar.",
    action=("Distrair o vigia com sucesso.", 30, final_showdown_surprise, final_showdown_assault)
)

canyon_trail = StoryNode(
    text="A trilha te leva a um desfiladeiro estreito. À frente, você avista um cavaleiro solitário, provavelmente um vigia da gangue. O resto do bando deve estar logo à frente.",
    choices={
        "1": ("Tentar passar furtivamente pelo vigia.", canyon_sneak),
        "2": ("Criar uma distração para atraí-lo para longe.", canyon_diversion),
        "3": ("Confrontar o vigia diretamente.", canyon_confront_lookout)
    }
)

# NÓ: Cavernas
whispering_caves = StoryNode(
    text="As Cavernas Sussurrantes são escuras e úmidas. Assim que você entra, ouve o som de rifles sendo engatilhados. 'Parece que o xerife caiu na nossa armadilha!', grita uma voz. É uma emboscada!",
    action=("Sobreviver à emboscada.", 70, canyon_trail, end_game_death_ambush)
)

# NÓ: Saloon (Investigação)
saloon_investigation = StoryNode(
    text="O saloon está cheio de rumores sobre o assalto. O barman, limpando um copo, menciona em voz baixa ter ouvido os bandidos falarem sobre um esconderijo nas 'Cavernas Sussurrantes'.",
    choices={
        "1": ("Acreditar no barman e ir para as Cavernas Sussurrantes.", whispering_caves),
        "2": ("Achar que é uma pista falsa e investigar o desfiladeiro a leste.", canyon_trail)
    }
)

# NÓ: Banco
bank_investigation_success = StoryNode(
    text="O ferreiro reconhece a espora imediatamente! Pertence a 'Jack Caolho', um membro conhecido da Gangue do Chapéu Preto. Ele diz que viu Jack cavalgando em direção ao desfiladeiro a leste.",
    choices={"1": ("Seguir a pista para o desfiladeiro.", canyon_trail)}
)

bank_investigation = StoryNode(
    text="No banco, o caos reina. O cofre foi arrombado e o cheiro de pólvora ainda está no ar. Você encontra uma espora incomum caída perto do cofre, provavelmente de um dos bandidos.",
    action=("Tentar identificar o dono da espora na cidade.", 40, bank_investigation_success, saloon_investigation)
)

# NÓ: Perseguição Imediata
immediate_pursuit_fail = StoryNode(
    text="O vento do deserto apagou a maioria das trilhas. Você perdeu o rastro dos bandidos. Sua melhor aposta agora é voltar à cidade e ver se consegue alguma informação no saloon.",
    choices={"1": ("Voltar ao saloon.", saloon_investigation)}
)

immediate_pursuit = StoryNode(
    text="Sem perder tempo, você monta em seu cavalo e cavalga para fora de TomasBurgo, examinando a planície em busca de rastros.",
    action=("Encontrar o rastro da gangue.", 50, canyon_trail, immediate_pursuit_fail)
)

# --- Raiz da Árvore / Início do Jogo ---
start_node = StoryNode(
    text="🤠 A Lenda do Xerife Kauan 🤠\nVocê é Kauan, o xerife da pequena e empoeirada cidade de TomasBurgo. A paz é quebrada quando o prefeito Davi invade seu escritório, pálido e ofegante. 'Xerife! A Gangue do Chapéu Preto assaltou o banco! Eles levaram tudo! Você precisa recuperar nosso dinheiro!'",
    choices={
        "1": ("'Conte comigo, prefeito. Vou começar investigando a cena do crime no banco.'", bank_investigation),
        "2": ("'Um trabalho desses requer ajuda. Vou ao saloon para ver o que descubro.'", saloon_investigation),
        "3": ("'Não há tempo a perder! Vou montar e seguir o rastro deles imediatamente.'", immediate_pursuit),
    }
)

# --- Loop Principal do Jogo ---
def play_game():
    """Função principal que executa o jogo em um loop."""
    
    while True: # Loop para permitir que o jogador jogue novamente.
        current_node = start_node
        while not current_node.is_ending:
            print("\n--------------------------------------------------------------------------")
            print(current_node.text)
            print("--------------------------------------------------------------------------")
            time.sleep(1)

            if current_node.action:
                action_desc, threshold, success_node, failure_node = current_node.action
                print(f"Sua próxima ação: {action_desc}")
                if roll_dice(threshold):
                    current_node = success_node
                else:
                    current_node = failure_node
            else:
                print("O que você faz?")
                for key, (desc, _) in current_node.choices.items():
                    print(f"[{key}] {desc}")
                
                choice = input("> ")
                if choice in current_node.choices:
                    _, next_node = current_node.choices[choice]
                    current_node = next_node
                else:
                    print("Escolha inválida. Tente novamente.")
            
            time.sleep(1)

        # Imprime a mensagem final da história
        print("\n**********************************************************")
        print(current_node.text)
        print("**********************************************************")

        # Pergunta ao jogador se ele quer jogar novamente
        while True:
            play_again = input("\nDeseja jogar novamente? (s/n): ").lower().strip()
            if play_again in ["s", "sim", "n", "nao", "não"]:
                break
            else:
                print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
        
        if play_again in ["n", "nao", "não"]:
            print("\nObrigado por jogar A Lenda do Xerife Kauan! Até a próxima, parceiro.")
            break # Encerra o loop principal e finaliza o programa.

# Inicia o Jogo
play_game()