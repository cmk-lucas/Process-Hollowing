# Projet Hollowing - Injection de code en Python

## 🚨 Description Ce projet implémente une technique d'injection de code appelée "Process Hollowing", où un processus légitime est suspendu, puis son code est remplacé par un shellcode ou un exécutable malveillant. Cela peut être utilisé dans des scénarios de tests de pénétration pour analyser la résistance d'un système aux attaques. Le script Python crée un processus légitime (par exemple `svchost.exe`), alloue de la mémoire dans ce processus, y injecte un payload (un fichier exécutable ou du shellcode), puis redémarre le processus avec le code injecté. ⚠️ **Avertissement :** Ce projet est à des fins éducatives uniquement. Ne l'utilisez pas pour des actions malveillantes.

## 🛠️ Prérequis Avant de commencer, assurez-vous d'avoir les outils et librairies suivants installés : - Python 3.x - `ctypes` (inclus par défaut dans Python) - Un système d'exploitation Windows (le script est conçu pour fonctionner sur Windows)

## 💻 Installation 1. Clonez ce repository : ```bash git clone https://github.com/cmk-lucas/hollowing-project.git ``` 2. Accédez au dossier du projet : ```bash cd hollowing-project ``` 3. Assurez-vous d'avoir Python installé et que vous êtes dans un environnement virtuel si nécessaire.

## 🚀 Utilisation 1. **Préparez votre payload** (un fichier `.exe` ou du shellcode) et placez-le dans le même dossier que ce script. Le nom du fichier doit être `payload.exe` (ou changez le dans le code). 2. **Exécutez le script** : ```bash python hollowing.py ``` Le script procédera à l'injection du code dans un processus légitime suspendu (`svchost.exe`), en allouant de la mémoire, injectant le payload, et reprenant l'exécution.

## 🔒 Fonctionnement du script Le script fonctionne selon les étapes suivantes : 1. **Création du processus suspendu** : Le script démarre un processus légitime, ici `svchost.exe`, en mode suspendu. 2. **Allocation de mémoire** : De la mémoire est allouée dans le processus cible pour accueillir le code malveillant. 3. **Injection du payload** : Le payload (fichier `.exe` ou shellcode) est injecté dans la mémoire allouée du processus. 4. **Changement de l'adresse d'entrée** : L'exécution du thread est redirigée vers l'adresse du payload injecté. 5. **Reprise de l'exécution** : Le processus cible reprend son exécution avec le code injecté.

## 🧠 Code explication Le script utilise les API Windows suivantes via `ctypes` : - **CreateProcessW** : Crée un processus suspendu. - **VirtualAllocEx** : Alloue de la mémoire dans le processus cible. - **WriteProcessMemory** : Injecte le payload dans la mémoire allouée du processus. - **QueueUserAPC** : Redirige le thread vers le payload injecté. - **ResumeThread** : Reprend l'exécution du processus.

## ⚠️ Avertissement Ce script est destiné uniquement à des fins d'apprentissage et de tests de pénétration. L'utilisation malveillante de cette technique peut entraîner des conséquences légales graves. Ne l'utilisez que dans des environnements contrôlés et avec des autorisations explicites.

## 👨‍💻 Auteurs Ce projet a été développé par **cherubin manunga kiaku**.

## 📝 Licence Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
