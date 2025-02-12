import fitness
import os

if __name__ == '__main__':
  app = fitness.create_app()

  app.run(host = '0.0.0.0', port = int(os.environ.get("PORT", 5000)))
