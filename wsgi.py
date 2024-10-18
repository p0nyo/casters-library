"""App entry point."""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from podcast import create_app

try:
    from podcast import test_config
    app = create_app(test_config)

except ImportError:
    app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False, debug=True)
