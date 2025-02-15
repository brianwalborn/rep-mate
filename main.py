import os
import repmate

if __name__ == '__main__':
  app = repmate.create_app()

  app.run(host = '0.0.0.0', port = int(os.environ.get("PORT", 5000)))
