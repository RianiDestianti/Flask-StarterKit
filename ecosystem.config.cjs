module.exports = {
  apps: [
    {
      name: "flask-skeleton",
      script: "venv/bin/gunicorn",
      args: "app:app -c gunicorn.conf.py",
      interpreter: "none",
      watch: false,
      autorestart: true,
      max_memory_restart: "500M"
    }
  ]
}
