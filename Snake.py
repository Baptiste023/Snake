import pygame
import random

# Initialisation
pygame.init()
longeur, largeur = 630, 640
lignes, colonnes = 30, 30
taille_case = longeur // lignes
ecran = pygame.display.set_mode((longeur, largeur))
pygame.display.set_caption("Snake")

# Couleurs
bordure = (4, 102, 10)
vert_clair = (16, 220, 50)
vert_fonce = (5, 177, 33)
pomme = (229, 33, 6)
serpent = (13, 91, 190)

# Vitesse
clock = pygame.time.Clock()
vitesse = 10

# État du jeu
running = True
game_over = False
score = 0

# Serpent
serp_pos = [10 * taille_case, 10 * taille_case]
serp_corp = [list(serp_pos)]
direction = "DROITE"


def Score():
    font = pygame.font.SysFont("Arial", 24)
    texte = font.render(f"Score : {score}", True, (255, 255, 255))
    ecran.blit(texte, (10, 10))


def nourriture():
    while True:
        pos = [
            random.randint(1, colonnes - 2) * taille_case,
            random.randint(1, lignes - 2) * taille_case
        ]
        if pos not in serp_corp:
            return pos


nouri_pos = nourriture()
appa_nouri = True


def plateau():
    for lig in range(lignes):
        for col in range(colonnes):
            if lig == 0 or lig == lignes - 1 or col == 0 or col == colonnes - 1:
                couleur = bordure
            else:
                couleur = vert_clair if (lig + col) % 2 == 0 else vert_fonce
            pygame.draw.rect(
                ecran, couleur,
                (col * taille_case, lig * taille_case, taille_case, taille_case)
            )



def affichage_mort():
    font = pygame.font.SysFont("Arial", 48)
    text = font.render("GAME OVER", True, (255, 0, 0))
    sub = pygame.font.SysFont("Arial", 24).render(
        "Cliquez pour recommencer", True, (255, 255, 255)
    )
    ecran.blit(text, (longeur // 2 - 140, largeur // 2 - 60))
    ecran.blit(sub, (longeur // 2 - 150, largeur // 2))



def recommencer():
    global serp_pos, serp_corp, direction, score, nouri_pos, appa_nouri, game_over
    score = 0
    serp_pos = [10 * taille_case, 10 * taille_case]
    serp_corp = [list(serp_pos)]
    direction = "DROITE"
    nouri_pos = nourriture()
    appa_nouri = True
    game_over = False


# Boucle principale
while running:
    ecran.fill((0, 0, 0))
    plateau()
    Score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            recommencer()

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "BAS":
                direction = "HAUT"
            elif event.key == pygame.K_DOWN and direction != "HAUT":
                direction = "BAS"
            elif event.key == pygame.K_LEFT and direction != "DROITE":
                direction = "GAUCHE"
            elif event.key == pygame.K_RIGHT and direction != "GAUCHE":
                direction = "DROITE"

    if game_over:
        affichage_mort()
        pygame.display.flip()
        clock.tick(10)
        continue

    # Mouvement
    if direction == "HAUT":
        serp_pos[1] -= taille_case
    elif direction == "BAS":
        serp_pos[1] += taille_case
    elif direction == "GAUCHE":
        serp_pos[0] -= taille_case
    elif direction == "DROITE":
        serp_pos[0] += taille_case

    serp_corp.insert(0, list(serp_pos))

    if serp_pos == nouri_pos:
        score += 1
        appa_nouri = False
    else:
        serp_corp.pop()

    if not appa_nouri:
        nouri_pos = nourriture()
        appa_nouri = True

    # Dessin
    for bloc in serp_corp:
        pygame.draw.rect(ecran, serpent, (bloc[0], bloc[1], taille_case, taille_case))
    pygame.draw.rect(ecran, pomme, (nouri_pos[0], nouri_pos[1], taille_case, taille_case))

    # Collisions
    if (serp_pos[0] < taille_case or serp_pos[0] >= (colonnes - 1) * taille_case or
        serp_pos[1] < taille_case or serp_pos[1] >= (lignes - 1) * taille_case):
        game_over = True

    if serp_pos in serp_corp[1:]:
        game_over = True

    pygame.display.flip()
    clock.tick(vitesse)

pygame.quit()
