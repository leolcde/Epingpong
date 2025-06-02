🏓 **Epingpong Bot** – Amuse toi et grimpe dans le classement !

Ce bot enregistre les résultats de chaque match et met à jour le **classement des joueurs** en fonction des victoires et défaites. Plus tu gagnes, plus tu montes dans le ranking ! 📊

🔹 **Comment ça marche ?**

➤ **`!join`** → Rejoins la file d'attente 

➤ **`!leave`** → Quitte la file d'attente

➤ **`!match @joueur1 @joueur2 score`** → Enregistre un match

➤ **`!ranking`** → Affiche le classement actuel

➤ **`!stats @joueur`** → Consulte tes performances

Prêt à devenir le champion d’Epitech ? 🏆🔥

🔹 **Installation**
1. Ajouter d'un environnement virtuel:
   ```bash
    python -m venv .venv
   ```
2. Activer l'environnement virtuel:
    - Sur Windows:
      ```bash
        .venv\Scripts\activate
      ```
    - Sur macOS/Linux:
      ```bash
        source .venv/bin/activate # bash
        source .venv/bin/activate.fish # fish
        source .venv/bin/activate.csh # csh
      ```
3. Installer les dépendances:
    ```bash
    pip install -r requirements.txt
    ```
4. Lancer le bot:
    ```bash
    python main.py # lancement en production
    jurriged main.py # lancement development avec hot reload
    ```
