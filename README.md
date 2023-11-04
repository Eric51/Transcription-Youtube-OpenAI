# Transcription-Youtube-Open-AI

# transcript.py
Ce programme est une application de transcription automatique de vidéos YouTube en utilisant l'API OpenAI. Voici un résumé des principales fonctionnalités :

1. Le programme utilise la bibliothèque PyQt5 pour créer une interface utilisateur graphique.
2. L'application dispose d'un champ de saisie où vous pouvez entrer l'URL de la vidéo YouTube que vous souhaitez transcrire.
3. Il y a un bouton "Transcrire" qui déclenche le processus de transcription de la vidéo.
4. Lorsque vous appuyez sur le bouton "Transcrire", le programme télécharge la vidéo depuis YouTube et la divise en segments de durée spécifiée (par défaut 90 secondes).
5. Chaque segment audio est ensuite transcrit en utilisant l'API OpenAI. La transcription est obtenue en utilisant le modèle "whisper-1" par défaut.
6. Après avoir transcrit chaque segment, le programme pose une question à OpenAI en utilisant le modèle spécifié (par défaut "gpt-4").
7. Les réponses obtenues sont stockées et ajoutées à un document Word (.docx) contenant la transcription complète de la vidéo.
8. Le document de transcription est ensuite enregistré sur le disque avec un nom spécifié par l'utilisateur ou par défaut.
9. L'application dispose également d'une fonction de configuration où vous pouvez spécifier la clé API OpenAI, le modèle à utiliser, la question à poser et la durée de segmentation.
10. Les valeurs de configuration sont sauvegardées dans un fichier JSON pour une utilisation ultérieure.

En résumé, ce programme permet de transcrire automatiquement des vidéos YouTube en utilisant l'API OpenAI.

# transcript2.py
Idem mais sans questions à chaque segment.
