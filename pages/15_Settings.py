"""
Settings — Jumuia — Parish Community
Spec §5 Settings Matrix: full user/parish configuration.
"""
import streamlit as st
try:
    from services.theme import inject
    inject()
except Exception:
    pass
from services.settings import settings_page
settings_page()
