"""Numatix Sales OS — shared configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CONTACTOUT_API_KEY = os.getenv("CONTACTOUT_API_KEY", "")
INSTANTLY_API_KEY = os.getenv("INSTANTLY_API_KEY", "")

MODEL = "claude-opus-4-6"
