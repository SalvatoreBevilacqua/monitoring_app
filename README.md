# System Monitoring Dashboard

Una robusta applicazione web per il monitoraggio di sistemi in tempo reale, costruita con Python Flask, MongoDB e JavaScript.

![Monitoring Dashboard](https://github.com/username/system-monitoring-dashboard/raw/main/screenshot.png)

## Tecnologie Utilizzate

- **Backend**: Python 3.11, Flask, PyMongo
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js, Bootstrap 5
- **Containerizzazione**: Docker, Docker Compose
- **Tool di Sviluppo**: Pipenv per la gestione delle dipendenze

## Architettura

L'applicazione segue un'architettura a tre livelli:

1. **Livello di Presentazione**: Frontend responsivo basato su Bootstrap con visualizzazioni dinamiche
2. **Livello di Logica**: API REST Flask per la gestione delle richieste e l'elaborazione dei dati
3. **Livello di Dati**: Database MongoDB per lo storage persistente

## Requisiti

- Python 3.11 o superiore
- MongoDB 5.0 o superiore
- Docker e Docker Compose (opzionale, per deployment containerizzato)

## Installazione

### Metodo 1: Installazione manuale

1. Clona il repository:
   ```bash
   git clone https://github.com/username/system-monitoring-dashboard.git
   cd system-monitoring-dashboard
   ```

2. Installa le dipendenze usando Pipenv:
   ```bash
   pipenv install
   ```

3. Avvia MongoDB (se non è già in esecuzione):
   ```bash
   mongod --dbpath /path/to/data/directory
   ```

4. Genera dati di test:
   ```bash
   pipenv run python generate_data.py --days 90
   ```

5. Avvia l'applicazione:
   ```bash
   pipenv run python app.py
   ```

6. Accedi all'applicazione nel browser all'indirizzo [http://localhost:5000](http://localhost:5000)

### Metodo 2: Utilizzo di Docker

1. Clona il repository:
   ```bash
   git clone https://github.com/username/system-monitoring-dashboard.git
   cd system-monitoring-dashboard
   ```

2. Costruisci e avvia i container:
   ```bash
   docker-compose up -d
   ```

3. Genera dati di test:
   ```bash
   docker-compose --profile data-generation up data-generator
   ```

4. Accedi all'applicazione nel browser all'indirizzo [http://localhost:5000](http://localhost:5000)

## Struttura del Progetto

```
system-monitoring-dashboard/
├── app.py                 # Applicazione Flask principale
├── Dockerfile             # Configurazione per Docker
├── docker-compose.yml     # Configurazione Docker Compose
├── generate_data.py       # Script per generare dati di test
├── Pipfile                # Gestione dipendenze Python
├── Pipfile.lock           # Versioni bloccate delle dipendenze
├── README.md              # Documentazione
├── static/                # Asset statici
│   └── scripts.js         # Codice JavaScript frontend
└── templates/             # Template HTML
    └── index.html         # Pagina principale dell'applicazione
```

## API Reference

### Endpoint disponibili

#### `GET /api/metrics`

Restituisce le metriche di sistema con supporto per paginazione e filtri.

**Parametri di query:**
- `page`: Numero di pagina (default: 1)
- `per_page`: Elementi per pagina (default: 10)
- `start_date`: Filtra da questa data (formato YYYY-MM-DD)
- `end_date`: Filtra fino a questa data (formato YYYY-MM-DD)
- `keyword`: Filtra per parola chiave nell'attività

**Esempio di risposta:**
```json
{
  "data": [
    {
      "timestamp": "2025-04-24 10:15:23",
      "uptime": 99.8,
      "users_connected": 42,
      "activity": "Normal"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 90,
    "pages": 9
  }
}
```

#### `GET /api/notifications`

Restituisce le notifiche di sistema con supporto per paginazione e filtri.

**Parametri di query:**
- Stessi parametri di `/api/metrics`

#### `GET /api/metrics/summary`

Restituisce un riepilogo delle metriche di sistema.

**Parametri di query:**
- `days`: Numero di giorni per il riepilogo (default: 30)

#### `GET /api/health`

Restituisce lo stato di salute del sistema e delle sue componenti.

## Caratteristiche Avanzate

### Sicurezza
- Parametri di query validati sul server
- Gestione sicura degli errori
- Logging completo degli eventi
- Variabili d'ambiente per configurazioni sensibili

### Performance
- Paginazione per gestire grandi dataset
- Ottimizzazione delle query MongoDB
- Containerizzazione per deployment scalabile

### Usabilità
- Interfaccia utente intuitiva
- Feedback visivo immediato
- Grafici interattivi per l'analisi dei dati
- Filtri avanzati per trovare rapidamente informazioni

## Punti di Forza del Progetto

1. **Architettura Robusta**: Separazione chiara tra frontend, backend e database.

2. **API RESTful**: Interfaccia ben progettata per facilitare l'integrazione.

3. **Docker-ready**: Configurazione completa per deployment containerizzato.

4. **Performance Ottimizzata**: Paginazione e filtri implementati lato server.

5. **Gestione Errori**: Sistema completo di logging e gestione degli errori.

## Sviluppi Futuri

- Implementazione di autenticazione e autorizzazione
- Esportazione dei dati in formati CSV/Excel
- Notifiche email/Slack per eventi critici
- Dashboard personalizzabili
- Integrazione con sistemi di monitoring esterni

## Licenza

MIT License. Vedi file LICENSE per maggiori dettagli.

## Autore

[Il tuo nome] - [Il tuo indirizzo email] Caratteristiche

- **Dashboard in tempo reale**: Visualizzazione dell'uptime del sistema, utenti connessi e attività sospette
- **Grafici interattivi**: Monitoraggio delle tendenze di uptime e connessioni utente
- **Filtri avanzati**: Ricerca per intervallo di date e parole chiave
- **API RESTful**: Endpoint ben documentati per l'integrazione con altri sistemi
- **Containerizzazione Docker**: Configurazione Docker Compose per un facile deployment
- **Paginazione**: Gestione efficiente di grandi volumi di dati

##