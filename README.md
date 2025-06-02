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

4. Configurer le fichier `.env`:
    - Créer un fichier `.env` à la racine du projet.
    - Ajouter les variables d'environnement nécessaires (voir `.env.example` pour les exemples).

5. démarrer une instance de Redis:
    - Si vous avez Docker installé, vous pouvez lancer Redis avec la commande suivante:
      ```bash
      docker run -d --name redis -p 6379:6379 redis
      ```
    - Sinon, installez Redis local selon votre système d'exploitation.

6. Lancer le bot:
    ```bash
    python main.py # lancement en production
    jurriged main.py # lancement development avec hot reload
    ```
