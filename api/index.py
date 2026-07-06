import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.main_simple import app

# This is the Vercel handler
handler = app