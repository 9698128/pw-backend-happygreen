# 🌱 HappyGreen Backend

API Backend per l'applicazione HappyGreen - La tua app per uno stile di vita più sostenibile.

## 🚀 Funzionalità

### ✅ Implementate
- **Autenticazione Utente**
  - Registrazione utenti
  - Login con email e password
  - Autenticazione JWT
  - Middleware di protezione delle route

### 🔧 Tecnologie Utilizzate
- **Framework**: Laravel 10
- **Database**: MySQL
- **Autenticazione**: Laravel Sanctum/JWT
- **API**: RESTful API

## 📦 Installazione

### Prerequisiti
- PHP >= 8.1
- Composer
- MySQL
- Node.js (per asset compilation)

### Setup
```bash
# Clona il repository
git clone https://github.com/tuo-username/happygreen-backend.git
cd happygreen-backend

# Installa dipendenze
composer install

# Copia file di configurazione
cp .env.example .env

# Configura database nel file .env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=happygreen
DB_USERNAME=your_username
DB_PASSWORD=your_password

# Genera chiave applicazione
php artisan key:generate

# Esegui migrazioni
php artisan migrate

# Avvia server di sviluppo
php artisan serve
```

## 🔗 API Endpoints

### Autenticazione
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout (protetta)
GET  /api/auth/profile (protetta)
```

### Esempio Request - Registrazione
```json
POST /api/auth/register
{
    "name": "Mario Rossi",
    "email": "mario@example.com",
    "password": "password",
    "password_confirmation": "password"
}
```

### Esempio Request - Login
```json
POST /api/auth/login
{
    "email": "mario@example.com",
    "password": "password"
}
```

### Esempio Response - Login Success
```json
{
    "success": true,
    "message": "Login effettuato con successo",
    "data": {
        "user": {
            "id": 1,
            "name": "Mario Rossi",
            "email": "mario@example.com"
        },
        "token": "your-jwt-token-here"
    }
}
```

## 🗄️ Struttura Database

### Tabella Users
- `id` - Primary Key
- `name` - Nome utente
- `email` - Email (unique)
- `password` - Password hashata
- `created_at` - Data creazione
- `updated_at` - Data ultimo aggiornamento

## 🚧 In Sviluppo

Le seguenti funzionalità sono in fase di sviluppo:
- Dashboard utente
- Gestione profilo
- Sistema di punteggi
- API per scanner eco-friendly

## 🔧 Configurazione CORS

Il backend è configurato per accettare richieste da:
- `http://localhost:3000` (React)
- `http://localhost:8080` (Vue)
- App Android locale

## 📝 Note per lo Sviluppo

- Il server di sviluppo gira su `http://localhost:8000`
- Per testare le API usa Postman o tools simili
- Logs disponibili in `storage/logs/laravel.log`

## 🐛 Troubleshooting

**Problema**: Errore di connessione database
**Soluzione**: Verifica credenziali nel file `.env`

**Problema**: Token JWT non valido
**Soluzione**: Rigenera il token con `php artisan jwt:secret`

