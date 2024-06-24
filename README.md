### Istruzioni per l'installazione e l'utilizzo dell'applicazione

1) Effettuare il fork del progetto sul proprio account github;
2) Clonare il progetto all'interno del proprio ambiente di programmazione;
3) Installare tutte le librerie necessarie indicate nel file requirements.txt
3) Nel file Connection/connector.py è necessario cambiare la mail di destinazione dei report dei collaudi e inserire la propria password (all'interno del metodo send_email);
4) Nel file UI/controller.py è necessario inserire dei numeri di telefono validi all'interno dei relativi campi dei metodi handle_call se si desidera utilizzare questa funzionalità;
5) Eseguire il file main.py per lanciare l'applicazione
6) Ai fini di preservare la sicurezza dei dati aziendali è prevista una procedura di autenticazione con username e password per accedere a tutte le funzionalità dell'applicazione

Per ulteriori dettagli e approfondimenti: [Relazione tecnica](documenti/relazione_tecnica.pdf), [Video dimostrativo](https://youtu.be/1W2-TwrOiPI?si=FSwgDlUK_MQH14QA)